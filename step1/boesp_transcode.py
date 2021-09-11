#-*- coding:utf-8 -*-
"""boesp_transcode.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

slp1chars = {}
def update_slp1chars(x,y,tranin,tranout):
 if not ((tranin == 'roman') and (tranout == 'slp1')):
  return
 m = re.search(r"^[a-zA-Z|~/\\^— √°'+.,;=?\[\]\(\)!-]*$",y)
 if m == None:
  print(iline+1,x,y)
 return

def print_unicode(x,u):
 """ Sample output:
x= a/MSa—BU/
0905 | अ | DEVANAGARI LETTER A
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
0902 | ं | DEVANAGARI SIGN ANUSVARA
0936 | श | DEVANAGARI LETTER SHA
2014 | — | EM DASH
092D | भ | DEVANAGARI LETTER BHA
0942 | ू | DEVANAGARI VOWEL SIGN UU
0951 | ॑ | DEVANAGARI STRESS SIGN UDATTA
 """
 import unicodedata
 outarr = []
 for c in u:
  name = unicodedata.name(c)
  icode = ord(c)
  a = f"{icode:04X} | {c} | {name}"
  outarr.append(a)
 print('x=',x)
 for out in outarr:
  print(out)
 print()

def generate_groups(lines):
 iline = 0 # start at first line
 nlines = len(lines)
 ngroup = 0
 # ignore blank lines
 dbg = False
 while iline < nlines:
  group = []
  while (lines[iline].strip() == ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    break
   
  if group != []:
   # group of blank lines
   ngroup = ngroup + 1
   if dbg: print('A',ngroup,group[0])
   yield(group)
   #continue
  # gather block of non-blank lines
  group = []
  while (lines[iline].strip() != ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    break
  ngroup = ngroup + 1
  if dbg: print('B',ngroup,group[0])
  yield group
  if dbg: 
   if ngroup > 10:
    print('debug exit')
    return
   
def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 return y

def transcode_S(group,tranin,tranout):
 lines = [] # transcoded lines
 newlines = []
 for iline,line in enumerate(group):
  # avoid the parts that should not be transcoded
  parts = re.split(r'(<S>)|(\[Seite.*?\])',line)
  newparts = []
  for part in parts:
   if part == None:
    continue
   elif part.startswith(('<S>','[Seite')):
    newpart = part
    #if part.startswith('[Seite1.54]'):
    # print('part=',part)
   else:
    # transcode
    newpart = transcode(part,tranin,tranout)
   newparts.append(newpart)
  newline = ''.join(newparts)
  newlines.append(newline)
 return newlines

def transcode_other(group,tranin,tranout):
 text = '\n'.join(group)
 def f(m):
  x = m.group(1)
  y =   transcode(x,tranin,tranout)
  return '{#%s#}'%y
 # the 0 before re.DOTALL is count.
 newtext = re.sub(r'{#(.*?)#}',f,text,0,re.DOTALL)
 # reconstitute lines
 if False and ('{#' in text):  # dbg
  print('OLD',text)
  print('NEW',newtext)
  exit(1)
 newlines = newtext.split('\n')
 return newlines

def transcode_groups(lines,tranin,tranout):
 ngroup = 0
 firstfound = False
 nlines = 0
 newgroups = []
 dbg = False
 for group in generate_groups(lines):
  ngroup = ngroup+1
  nlines = nlines + len(group)
  # skip the groups until a condition is met
  if firstfound:
   if group[0].startswith('<S>'):
    newgroup = transcode_S(group,tranin,tranout)
    if dbg:
     temp1 = '\n'.join(group)
     if '[Seite' in temp1:
      print('old:\n',temp1)
      temp = '\n'.join(newgroup)
      print('new:\n',temp)
      dbg = False
   elif group[0].strip() == '':
    # empty group
    newgroup = group
   else:
    newgroup = transcode_other(group,tranin,tranout)
  elif group[0].startswith('<H> Boehtlingk'):
   firstfound = True
   newgroup = group
  else: # before first found
   newgroup = group
  newgroups.append(newgroup)
 # reconstruct array of lines
 newlines = []
 for group in newgroups:
  for line in group:
   newlines.append(line)
 return newlines

def read(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"lines read from",filein)
 return lines

def write(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')
 print(len(lines),'written to',fileout)

def test():
 tranin = 'hk'
 tranout = 'slp1'
 text = 'hello {#abhi\nazva#}'
 def f(m):
  x = m.group(1)
  y =   transcode(x,tranin,tranout)
  return '{#%s#}'%y
 newtext = re.sub(r'{#(.*?)#}',f,text,0,re.DOTALL)
 print(newtext)
 
 exit(1)
if __name__=="__main__":
 #test()
 tranin = sys.argv[1]
 tranout = sys.argv[2]
 #test()
 filein = sys.argv[3] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[4] # 
 lines = read(filein)
 newlines = transcode_groups(lines,tranin,tranout)
 write(fileout,newlines)
 

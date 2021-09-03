# coding=utf-8
""" sanchars.py
 
"""
from __future__ import print_function
import sys, re,codecs

def generate_groups(lines):
 iline = 0 # start at first line
 nlines = len(lines)
 # ignore blank lines
 while iline < nlines:
  group = []
  while (lines[iline].strip() == ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    #return []  # yield [] gives error
    break
  if group != []:
   # group of blank lines
   yield(group)  
  # gather block of non-blank lines
  group = []
  while (lines[iline].strip() != ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    break
  yield group

def update_chars(line,chars):
 # modify chars
 for c in line:
  if c in (' ','\n'):
   continue
  if c not in chars:
   chars[c] = 0
  chars[c] = chars[c] + 1
 

def transcode_S(group,chars):
 lines = [] # transcoded lines
 for iline,line in enumerate(group):
  # avoid the parts that should not be transcoded
  parts = re.split(r'(<S>)|(\[Seite.*?\])',line)
  newparts = []
  for part in parts:
   if part == None:
    continue
   elif part.startswith(('<S>','[Seite')):
    newparts.append(part)
   else:
    # transcode
    update_chars(part,chars)
    newpart = part
    if '.' in part:
     print('Transcode_S anomaly:',part)
     print(iline,line)
    newparts.append(newpart)
  newline = ''.join(newparts)
  assert newline == line

def transcode_other(group,chars):
 ## There are problems here.  For now, ignore these problems.
 ## write them to fdbg
 text = '\n'.join(group)
 #text = text.replace('.#}','#}.')  # since '.' is special in slp1
 texts = re.findall(r'{#.*?#}',text,re.DOTALL)
 # recode [Seite]
 for t in texts:
  t0 = t
  #t0 = t.replace('.#}','#}.')  # since '.' is special in slp1
  t1 = t0.replace('{#','')
  t2 = t1.replace('#}','')
  if ('.' in t2) and False:  # for later debugging?
   print('unexpected "."')
   print(t)
   print()
  update_chars(t2,chars)
  
def transcode_groups(lines):
 ngroup = 0
 firstfound = False
 page = '1.1'
 chars = {} # distribution of characters to transcode in <S>
 chars1 = {} # in {#X#}
 nlines = 0
 #groups = list(generate_groups(lines))
 #print(len(groups),"groups generated")
 newgroups = []
 for group in generate_groups(lines):
  ngroup = ngroup+1
  nlines = nlines + len(group)
  # skip the groups until a condition is met
  if firstfound:
   if group[0].startswith('<S>'):
    newgroup = transcode_S(group,chars)
   elif group[0].strip() == '':
    # empty group
    newgroup = group
   else:
    newgroup = transcode_other(group,chars1)
  elif group[0].startswith('<H> Boehtlingk'):
   firstfound = True
   newgroup = group
  else: # before first found
   newgroup = group
  newgroups.append(group)
 return chars,chars1

def read(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"lines read from",filein)
 return lines

def write_chars(f,chars,title):
 outarr = []
 outarr.append(title)
 keys = sorted(chars.keys())
 for key in keys:
  outarr.append('%s %s' %(key,chars[key]))
 
 outarr.append('---------------------------------------------------')
 outarr.append('')
 for out in outarr:
  f.write(out+'\n')

if __name__=="__main__":
 filein = sys.argv[1] # boesp-1_utf8.txt
 fileout = sys.argv[2] # stats on transcoded characters
 filedbg = 'allgroups_dbg.txt'
 fdbg = codecs.open(filedbg,'w','utf-8') 
 lines = read(filein)
 chars,chars1 = transcode_groups(lines)
 with codecs.open(fileout,"w","utf-8") as f:
  write_chars(f,chars,'Characters in <S>')
  write_chars(f,chars1,'Characters in {#..#}')
 print('Sanskrit character frequency written to',fileout)
 
 
 

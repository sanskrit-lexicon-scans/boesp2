# coding=utf-8
""" xml_invert
 
"""
from __future__ import print_function
import sys, re,codecs

class Entry(object):
 def __init__(self,lines):
  self.lines = lines
 
def generate_entries(lines):
 inentry = False
 for iline,line in enumerate(lines):
  if line.startswith('<entry>'):
   entry = []
   inentry = True
  elif line.startswith('</entry>'):
   yield Entry(entry)
   inentry = False
   entry = []
  elif inentry:
   entry.append(line)
  else:
   entry = []
   
def adjust_group_D(group,tag):
 # first line is opening xml with attributes.
 elt = group[0]
 m = re.search(r' n="(.*?)"',elt)
 Ls = m.group(1).split(',')
 m = re.search(r' a="(.*?)"',elt)
 if m == None:
  As = []
 else:
  As = m.group(1).split(',')
 group1 = group[1:]
 # adjust first line.
 # <b>3.</b> (<b>1.</b>) xxxxx
 line0 = group1[0]
 #line0 = re.sub(r'\(<b>[0-9]+\.</b>\)','',line0)
 line0 = re.sub(r'<b>[0-9]+\.</b>','',line0)
 line0 = re.sub(r'\( *\)','',line0)  # parens around A group
 line0 = line0.lstrip()
 Ds = ''.join(['<D%s>' % L for L in Ls])
 As = ''.join(['<A%s>' % L for L in As])
 line0 = Ds + As + ' ' + line0
 group1[0] = line0
 # two slightly different forms
 return group1

def adjust_group_S(group,tag):
 # first line is opening xml with attributes.
 # For these, ignore the attribute.
 group1 = group[1:]
 line0 = group1[0]
 if line0.startswith('<lg>'):
  group1[0] = '<S>' + line0
 else:
  # extra space
  group1[0] = '<S> ' + line0
 return group1

def adjust_group_HS(group,tag):
 # first line is opening xml with attributes.
 group1 = group[1:]
 fulltag = '<%s>' %tag
 group1[0] = fulltag + ' ' + group1[0]
 return group1

def adjust_group_FV(group,tag):
 # first line is opening xml with attributes.
 # For these, ignore the attribute.
 group1 = group[1:]
 fulltag = '<%s>' %tag
 group1[0] = fulltag + group1[0]
 return group1

def adjust_group_FDUMMY(group,tag):
 # first line is opening xml with attributes.
 # For these, ignore the attribute.
 group1 = group[1:]
 fulltag = '<F>'
 group1[0] = fulltag + group1[0]
 if False: # dbg
  print('group lines:')
  for line in group:
   print(line)
  print('group1 lines:')
  for line in group1:
   print(line)
  exit(1)
 return group1

def adjust_group(group,tag):
 if tag == 'S':
  group1 = adjust_group_S(group,tag)
 elif tag == 'HS':
  group1 = adjust_group_HS(group,tag)
 elif tag == 'D':
  group1 = adjust_group_D(group,tag)
 elif tag in ['F','V1','V2','V3','F4.1','F4.2']:
  group1 = adjust_group_FV(group,tag)
 elif tag == 'FDUMMY':
  group1 = adjust_group_FDUMMY(group,tag)
 else:
  group1 = group
 return group1

def groups_from_entry(entry):
 # construct entry.groups
 groups = []
 # first line is info
 infoline = entry.lines[0]
 lines = entry.lines
 nlines = len(lines)
 m = re.search(r'gtypes="(.*?)"',infoline)  # "S,D,F" for instance
 gtypes = m.group(1).split(',')
 iline = 0
 for tag in gtypes:
  iline = iline + 1
  endtag = '</%s>' % tag
  if nlines <= iline:
   break
  line = lines[iline]
  group = []
  while line != endtag:
   group.append(line)
   iline = iline + 1
   if iline == nlines:
    break
   line = lines[iline]
  group1 = adjust_group(group,tag)
  groups.append(group1)
 entry.groups = groups


def read_and_clean_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  nprob = 0
  lines = []
  for iline,line in enumerate(f):
   line = line.rstrip('\r\n')
   lines.append(line)
   continue
   # cleaning <>
   if '<>' in line:
    nprob = nprob + 1
    line = line.replace('<>','')
   # remove middledot+space at end of lines.
   line = re.sub(r'· $','',line)
   if '·' in line:
    print('malformed use of middle dot at line',iline+1)
    nprob = nprob + 1
   lines.append(line)
   
 print(len(lines),"lines read from",filein)
 
 if nprob != 0:
  print('read_and_clean_lines:',nprob,'problems need to be fixed')
  exit(1)
 return lines

def s_to_curly(text):
 text = text.replace('<s>','{#')
 text = text.replace('</s>','#}')
 return text

def i_to_curly(text):
 text = text.replace('<i>', '{%')
 text = text.replace('</i>', '%}')
 return text

def wide_to_curly(text):
 text = text.replace('<wide>', '{|')
 text = text.replace('</wide>', '|}')
 return text

def xml_to_curly(text):
 text = s_to_curly(text)
 text = i_to_curly(text)
 text = wide_to_curly(text)
 # also, change <pb n="X"/> to [SeiteX] 
 text = re.sub(r'<pb n="(.*?)"/>',r'[Seite\1]',text)
 # also, change <pb1 n="X"/> to [pageX] 
 text = re.sub(r'<pb1 n="(.*?)"/>',r'[Page\1]',text)
 text = text + '· ' # temporary form of boesp_utf
 return text

if __name__=="__main__":
 filein = sys.argv[1] # boesp-hk.xml
 fileout = sys.argv[2] # version of boesp_utf8.txt
 xmlroot = 'boesp'
 lines = read_and_clean_lines(filein)
    
 #head = xml_header(xmlroot)
 entries = list(generate_entries(lines))
 print(len(entries),'entries found in',filein)
 for entry in entries:
  groups_from_entry(entry)
  
 with codecs.open(fileout,"w","utf-8") as f:
  nlines = 0
  for entry in entries:
   for group in entry.groups:
    for line in group:
     line = xml_to_curly(line)
     f.write(line+'\n')
     nlines = nlines + 1
    f.write(' \n') # blank line between groups
    nlines = nlines + 1
 print(nlines,'lines written to',fileout)
 

 

# coding=utf-8
""" extractsan.py
 
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys, re,codecs

def out_info(e):
 info = e.attrib['n']
 # 'L=11: S,D,F 1.2'
 m = re.search(r'=(.*?):',info)
 L = m.group(1)
 m = re.search(r' ([1-3][.][0-9]+)$',info)
 page = m.group(1)
 outarr = []
 outarr.append('; %s : page %s' %(L,page))
 return outarr

def adjust_underscore(x):
 if '_' not in x:
  return x
 y = x.replace('_</s>','</s>.')
 if '_' in y:
  print('WARNING: found _',x)
 return y

def out_S(e):
 outarr = []
 text = e.text
 textlines = text.split('\n')
 for line in textlines:
  if line.strip() != '':
   line = adjust_underscore(line)
   if '@' not in line:
    outarr.append(line)
    continue
   # special handling for lines with @
   lines1 = re.split(r' @ ',line)
   if len(lines1) != 2:
    print('ERROR @:',lines1)
    exit(1)
   assert lines1[0].startswith('    ')
   outarr.append(lines1[0])
   outarr.append('      '+lines1[1])  # insert 6 spaces
 return outarr

def out_HS(e):
 outarr = []
 text =  ET.tostring(e,encoding="unicode")
 textlines = text.split('\n')
 for line in textlines:
  line1 = line.strip()
  if line1 == '':
   continue
  elif line1 in ['<HS>','</HS>']:
   continue
  else:
   line1 = adjust_underscore(line1)
   lineout = '+   %s'%line1
  outarr.append(lineout)
 return outarr

def write_long_lines(entries,filelong):
 # print long lines which may need to be split
 with codecs.open(filelong,"w","utf-8") as f:
  nlines = 0
  nlong = 0  # of entries with long lines
  for outentry in entries:
   longlines = []
   for line in outentry:
    nlines = nlines + 1
    if (len(line) > 100) and (not line.startswith('+')):
     longlines.append(line)
   if longlines == []:
    continue
   nlong = nlong + 1
   outarr = [outentry[1]] ## L,page
   #outarr = outarr + longlines  
   for line in outarr:
    f.write(line+'\n')
 print(nlong,"long entries written to",filelong)

if __name__=="__main__":
 tranin = sys.argv[1]
 filein = sys.argv[2] # boesp_<tranin>.xml
 fileout = sys.argv[3] # work_san_<tranin>.txt
 tree = ET.parse(filein)  # utf8?
 root = tree.getroot()
 print(root.tag)
 nentry = 0
 entries = []  # array, each element is a list of lines
 for entry in root:
  nentry = nentry + 1
  if False and (nentry == 16):
   print('quitting early')
   break
  outentry = ['; ---------------------------------------------']
  for child in entry:
   #print(child.tag,child.attrib)
   if child.tag == 'info':
    a  = out_info(child)
   elif child.tag == 'S':
    # only text node
    a = out_S(child)    
   elif child.tag == 'HS':
    a = out_HS(child)
   else:
    # skip this child
    continue
   for line in a:
    outentry.append(line)
  entries.append(outentry)
 #

 with codecs.open(fileout,"w","utf-8") as f:
  nlines = 0
  for outentry in entries:
   for line in outentry:
    f.write(line+'\n')
    nlines = nlines + 1
 #
 print('%s entries and %s lines written to %s' %(len(entries),nlines,fileout))
 if tranin == 'slp1':
  filelong = 'temp_san_slp1_long.txt'
  write_long_lines(entries,filelong)


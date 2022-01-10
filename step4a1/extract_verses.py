# coding=utf-8
"""step4a1/extract_verses.py
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step3e')
# the Entry object
from transcode import xml_header,read_entries

def write_verses(entries,vol,fileout):
 body = []
 filter = "%s." % vol
 nentry = 0 # number of extracted entries
 for entry in entries:
  if not entry.page.startswith(filter):
   continue
  nentry = nentry + 1
  lines = [] # lines extracted for this entry
  lines.append('<edit>')  # use 'edit' as tag, rather than 'entry'
  lines.append(entry.info)
  gtypes = entry.gtypes
  groups = entry.groups
  for igtype,gtype in enumerate(gtypes):
   if gtype not in ['S','HS']:
    continue
   group = groups[igtype]
   for line in group:
    lines.append(line)
  lines.append('</edit>')
  lines.append('; ------------------------------------------------')
  for line in lines:
   body.append(line)
 tail = []
 linesout = body
 with codecs.open(fileout,"w","utf-8") as f:
  for line in linesout:
   f.write(line+'\n')
 print(nentry,'entries extracted')
 print(len(linesout),"lines written to",fileout)

if __name__=="__main__":
 vol = sys.argv[1]  # 1,2 or 3
 filein = sys.argv[2]  # boesp.xml
 fileout = sys.argv[3] # extract of S and HS entries
 xmlroot = 'boesp'
 version = "1.4"  # this must agree with step0/boesp.dtd
 entries = read_entries(filein)
 
 write_verses(entries,vol,fileout)
 
 

# coding=utf-8
"""adjust_ab.py
 
"""
from __future__ import print_function
import sys, re,codecs

if __name__=="__main__":
 filein = sys.argv[1] # assumed Devanagari encoding of Sanskrit
 fileout = sys.argv[2] # 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"read from",filein)
 newlines = []
 for line in lines:
  if re.search(r'^[:;] *correction',line):
   # skip these lines
   continue
  if re.search(r'^; *comment',line):
   # skip these lines
   continue
  if re.search('^[\t ]*$',line):
   # skip blank lines
   continue
  # 
  newline = line.replace('\t//','      ')
  newlines.append(newline)

 with codecs.open(fileout,"w","utf-8") as f:
  for line in newlines:
   f.write(line+'\n')
 print(len(newlines),"written to",fileout)
 

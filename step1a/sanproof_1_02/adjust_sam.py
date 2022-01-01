# coding=utf-8
"""adjust_sam.py
 
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
  # volume 1
  if line.startswith('--'):
   newline = '; ' + line
  else:
   newline = line
  newlines.append(newline)

 with codecs.open(fileout,"w","utf-8") as f:
  for line in newlines:
   f.write(line+'\n')
 print(len(newlines),"written to",fileout)
 

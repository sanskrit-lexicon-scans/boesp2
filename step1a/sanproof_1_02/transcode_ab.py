# coding=utf-8
"""transcode_ab.py
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../')
import transcoder
transcoder.transcoder_set_dir('../transcoder')

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 return y

if __name__=="__main__":
 filein = sys.argv[1] # assumed Devanagari encoding of Sanskrit
 fileout = sys.argv[2] # 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"read from",filein)
 newlines = [transcode(line,'deva','slp1') for line in lines]
 with codecs.open(fileout,"w","utf-8") as f:
  for line in newlines:
   f.write(line+'\n')
 print(len(newlines),"written to",fileout)
 

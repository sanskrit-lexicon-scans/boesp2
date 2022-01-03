# coding=utf-8
"""step4b/transcode_ln.py
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step3e')
import transcoder
transcoder.transcoder_set_dir('./')

class Rec(object):
 def __init__(self,line):
  self.ln,self.count = re.split(r' *: *',line)
  self.iast = ln_iast(self.ln)

def ln_iast(x):
 x = x.replace('M3','M2')
 x = x.replace('m3','m2')
 y = transcoder.transcoder_processString(x,'as','roman') # as_roman.xml
 return y

def init_recs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Rec(line.rstrip('\r\n')) for line in f]
 return recs

def write_recs(recs,fileout):
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   out = '%s : %s : %s' %(rec.ln,rec.count,rec.iast)
   f.write(out+'\n')
 print(len(recs),"records written to",fileout)
 
if __name__=="__main__":
 filein = sys.argv[1] # letternums.txt
 fileout = sys.argv[2] # 
 tranin = 'as'
 tranout = 'roman'
 recs = init_recs(filein)
 write_recs(recs,fileout)
 

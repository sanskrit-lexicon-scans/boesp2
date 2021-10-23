# coding=utf-8
""" as_2.py
"""
from __future__ import print_function
import sys, re,codecs

from pwgbib_altera import read_pwgbib

class AS(object):
 def __init__(self,line):
  self.line = line.rstrip('\r\n')
  self.code,self.count = self.line.split(r' : ')
  self.pwgrec = None
  
def read_as_1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [AS(x) for x in f]
 return recs

def match_as_pwg(asrecs,pwgrecs):
 d = {}
 for pwgrec in pwgrecs:
  key = pwgrec.pwgcode1
  if key in d:
   oldrec = d[key]
   oldcode = oldrec.pwgcode
   ident = pwgrec.ident
   oldident = oldrec.ident
   print('duplicate pwgkey',key,pwgrec.pwgcode,ident,oldcode,oldident)
  d[key] = pwgrec
 #
 for asrec in asrecs:
  key = asrec.code
  if key in d:
   asrec.pwgrec = d[key]
   
def write(asrecs,fileout):
 recs = asrecs
 with codecs.open(fileout,"w","utf-8") as f:
  nfound = 0
  ncount1 = 0  # count of 'found'
  ncount2 = 0  # count of 'not found'
  for rec in recs:
   key = rec.code
   count = rec.count
   if rec.pwgrec:
    text = rec.pwgrec.tooltip
    nfound = nfound + 1
    ncount1 = ncount1 + int(count)
   else:
    text = 'NOTPWG'
    ncount2 = ncount2 + int(count)
   out = '%s : %s : %s' %(key,count,text)
   f.write(out+'\n')
 print(len(recs),"records written to",fileout)
 print(nfound,'records found in PWG')
 print(ncount1,'total count for abbreviations found in PWG')
 print(ncount2,'total count for abbreviations not found in PWG')
if __name__=="__main__":
 #test()
 filein = sys.argv[1] # as_1.txt
 filein1 = sys.argv[2] # pwgbib.txt
 fileout = sys.argv[3] # as_2.txt
 pwgrecs = read_pwgbib(filein1)
 asrecs = read_as_1(filein)
 # now match, adding field to AS objects
 match_as_pwg(asrecs,pwgrecs)
 write(asrecs,fileout)

 

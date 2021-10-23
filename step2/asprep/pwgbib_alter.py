# coding=utf-8
""" pwgbib_alter.py
"""
from __future__ import print_function
import sys, re,codecs

class PWGBIB(object):
 def __init__(self,line):
  self.line = line.rstrip('\r\n')
  m = re.search(r'([^ ]*) <HI code="(.*?)" iast="(.*?)">(.*)$',self.line)
  if m == None:
   print('PWGBIB error:',self.line)
   exit(1)
  self.ident = m.group(1)
  self.pwgcode = m.group(2)  # a variant of AS coding
  self.iast = m.group(3)
  self.tooltip = m.group(4)
  self.get_code1()
 def get_code1(self):
  changes = [
   ('10','1'),
   ('C2','S4'),
   ('M5','M3'),
   #('',''),
   #('',''),
  ]
  x = self.pwgcode
  for old,new in changes:
   x = x.replace(old,new)
  self.pwgcode1 = x
  
def read_pwgbib(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  recs = [PWGBIB(x) for x in f if not x.startswith(';')]
 return recs

def write(pwgrecs,fileout):
 recs = sorted(pwgrecs,key = lambda rec: rec.pwgcode1)
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   key = rec.pwgcode1
   text = rec.tooltip
   text = text.replace('[Cologne Addition]','[CA]')
   out = '%s : %s' %(key,text)
   f.write(out+'\n')
 print(len(recs),"records written to",fileout)
 
if __name__=="__main__":
 #test()
 filein = sys.argv[1] # pwgbib.txt
 fileout = sys.argv[2] # boesp.xml
 pwgrecs = read_pwgbib(filein)
 write(pwgrecs,fileout)

 

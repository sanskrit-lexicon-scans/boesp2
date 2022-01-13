# coding=utf-8
""" aufrecht_transcode.py
"""
import sys, re,codecs

data="""
a1 ā
n2 ṇ 
r2 ṛ
u7 ϋ
o7 ӧ
a7 ӓ
h2 ḥ
m2 ṃ
s2 ṣ 
S4 Ś
s4 ś
u1 ū
n5 ñ
n3 ṅ
t2 ṭ 
â ā
î ī
û ū
ç ś
Ç Ś
"""

class Rec(object):
 def __init__(self,auf,uni):
  self.auf = auf
  self.uni = uni
  
def init_recs():
 lines = data.splitlines()
 recs = []
 for line in lines:
  line = line.strip()
  parts = line.split(' ')
  if len(parts) != 2:
   continue
  auf,uni = parts
  recs.append(Rec(auf,uni))
 return recs

def rec_to_entrylines(rec):
 lines = []
 lines.append('<entry>')
 info = '<info L="%s" page="6.%s" gtypes="S"/>' %(rec.L2,rec.page)
 lines.append(info)
 lines.append('<S n="%s">' % rec.L2)
 lines.append('<s></s>')
 lines.append('<s></s>')
 lines.append('<s></s>')
 lines.append('<s></s>')
 lines.append('</S>')
 lines.append('<D n="%s">' % rec.L2)
 lines.append('')
 lines.append('</D>')
 lines.append('<F n="%s">' % rec.L2)
 lines.append('')
 lines.append('</F>')
 lines.append('</entry>')
 return lines

def write(fileout,linesout):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in linesout:
   f.write(line+'\n')
 print(len(linesout),"lines written to",fileout)

def transcode(line,recs):
 for rec in recs:
  line = line.replace(rec.auf,rec.uni)
 return line

if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"from",filein)
 recs = init_recs()
 print(len(recs),"transcode records")
 newlines = []
 for line in lines:
  newline = transcode(line,recs)
  newlines.append(newline)
 write(fileout,newlines)
 

# coding=utf-8
""" aufrecht.py
"""
import sys, re,codecs

data="""
7668.1 -> 7866 <s>amuM kAlakzepaM</s> page 4
7687.1 -> 7867 <s>arTA na santi</s> page 73
7690.1 -> 7868 <s>alipawalEH</s> page 63
7711.1 -> 7869 <s>asyA manoharA°</s> page 82
7738.1 -> 7870 <s>AlokavantaH</s> page 49
7756.1 -> 7871 <s>uttaMsakOtuka°</s> page 12
7785.1 -> 7872 <s>>etAsu ketaki</s> page 71
7791.1 -> 7873 <s>kaTamiha manuzyajanmA</s> page 62
7838.1 -> 7874 <s>kusumaM koSAtakyAH</s> page 17
7841.1 -> 7875 <s>kfpaRasya samfdDInAM BoktAraH</s> page 48
7845.1 -> 7876 <s>kenAtra campakataro</s> page 85
7846.1 -> 7877 <s>kokila kalamAlApEH</s> page 40
7847.1 -> 7878 <s>kva citprARiprAptam</s> page 78
"""

class Rec(object):
 def __init__(self,L1,L2,verse,page):
  self.L1 = L1
  self.L2 = L2
  self.verse = verse
  self.page = page
  
def init_recs():
 lines = data.splitlines()
 recs = []
 for line in lines:
  m = re.search(r'^(.*?) -> ([0-9]+) (<s>.*?</s>) page ([0-9]+)',line)
  if m == None:
   continue
  L1 = m.group(1)
  L2 = m.group(2)
  verse = m.group(3)
  page = m.group(4)
  recs.append(Rec(L1,L2,verse,page))
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

def write(fileout,recs):
 linesout = []
 for rec in recs:
  for line in rec.entrylines:
   linesout.append(line)
  linesout.append('') # blank line after entry
 with codecs.open(fileout,"w","utf-8") as f:
  for line in linesout:
   f.write(line+'\n')
 print(len(linesout),"lines written to",fileout)
 
if __name__=="__main__":
 fileout = sys.argv[1]  
 recs = init_recs()
 print(len(recs),"records")
 for rec in recs:
  rec.entrylines = rec_to_entrylines(rec)
 write(fileout,recs)
 

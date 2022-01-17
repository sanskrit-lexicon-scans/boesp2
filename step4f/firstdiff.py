# coding=utf-8
""" aufrecht.py
"""
import sys, re,codecs



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

def readlines(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

if __name__=="__main__":
 filein1 = sys.argv[1]
 filein2 = sys.argv[2]
 lines1 = readlines(filein1)
 lines2 = readlines(filein2)
 for iline1,line1 in enumerate(lines1):
  if line1.startswith('<info'):
   line2 = lines2[iline1]
   if line1 != line2:
    print('first info diff at line',iline1)
    print(line1,filein1)
    print(line2,filein2)
    exit(1)
    
 #fileout = sys.argv[1]  
 
 

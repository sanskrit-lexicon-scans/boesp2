# coding=utf-8
"""step4a/update_prep.py
 
"""
from __future__ import print_function
import sys, re,codecs

class Entry(object):
 def __init__(self,group):
  assert(group[0].startswith('; -------------------------------'))
  m = re.search(r'^; ([0-9,]+) :',group[1])
  self.Ls = m.group(1)
  self.HS = [line for line in group[2:] if line.startswith('+')]
  self.S =  [line for line in group[2:] if not line.startswith('+')]
  self.newEntries = []
  
class NewEntry(object):
 def __init__(self,L,lines):
  self.L = L
  self.lines = lines
  
def generate_entries(lines):
 group = None
 for iline,line in enumerate(lines):
  if line.startswith('; -------------------------------'):
   if group == None:  # first group
    group = [line]
   else:
    entry = Entry(group)
    yield entry
    group = [line]
  else:
   group.append(line)
 entry = Entry(group)
 yield entry

def get_entries(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 entries = list(generate_entries(lines))
 print(len(entries),"entries from",filein)
 return entries

def HS_entries(entry):
 Ls = entry.Ls.split(',')
 HS = entry.HS
 ans = [] # list of newEntry objects
 if len(HS) == 0:
  return ans
 Lcur = int(Ls[0])
 Lprev = Lcur - 1
 for iline,line in enumerate(HS):
  L = '%s.%s' % (Lprev,iline+1)
  newlines = []
  newlines.append('<HS>')
  # some adjustments to line
  newline = re.sub(r'^[+] *','',line)
  newline = newline.strip()
  # put space before avagraha
  newline = newline.replace("'"," '")
  # remove multiple spaces
  newline = re.sub(r'  +',' ',newline)
  # replace [SeiteX] with <pb n="X"/>
  newline = re.sub(r'\[Seite(.*?)\]',r'<pb n="\1"/>',newline)
  newlines.append(newline)
  newlines.append('</HS>')
  newEntry = NewEntry(L,newlines)
  ans.append(newEntry)
 return ans

def generate_sgroups(lines,Ls):
 # first, handle page breaks
 newlines = []
 nlines = len(lines)
 pbline = None
 for iline,line in enumerate(lines):
  if '[Seite' in line:
   if (iline+1) != nlines:
    # never occurs in volume 1 
    print('Seite anomaly 1',Ls)
    exit(1)
   m = re.search(r'^(.*)\[Seite(.*?)\] *$',line)
   if m == None:
    print('Seite anomaly 2',Ls)
    exit(1)
   newline = m.group(1)
   newlines.append(newline)
   page = m.group(2)
   pbline = '<pb n="%s"/>' % page
  else:
   newlines.append(line)
 if Ls[0] in ['1026','1027']:
  # these entries have an extra line. Groups not determined by ..
  print('update_prep special case',Ls)
  group = newlines
  if pbline != None:
   group.append(pbline)
  yield group
  return  # only one group for 1026 and 1027.
 group = []
 nlines = len(newlines)
 for iline,line in enumerate(newlines):
  # line ending in double danda (two periods for slp1) close a group
  group.append(line)
  if (iline + 1) == nlines:
   if pbline != None:
    # add pbline to the last group
    group.append(pbline)
  if line.strip().endswith('..'):
   yield group
   group = []
 if group != []:
  print('group anomaly:',Ls)
 
def S_entries(entry):
 Ls = entry.Ls.split(',')
 lines = entry.S
 ans = [] # list of newEntry objects
 assert len(lines) != 0
 ng = len(Ls)
 # break up lines into ng subgroups
 # Two anomalies: L=1026 and L=1027 have (3) lines in one group
 groups = list(generate_sgroups(lines,Ls))
 assert len(groups) == ng
 #
 for i,L in enumerate(Ls):
  group = groups[i]
  newlines = []
  newlines.append('<S n="%s">' % L)
  for line in group:   
   # some adjustments to line
   newline = line.strip()
   # put space before avagraha
   newline = newline.replace("'"," '")
   # remove multiple spaces
   newline = re.sub(r'  +',' ',newline)
   # enclose in <s>..</s>, except for page break
   if not newline.startswith('<pb'):
    newline = '<s>%s</s>' % newline
   newlines.append(newline)
  newlines.append('</S>')
  newEntry = NewEntry(entry.Ls,newlines)
  ans.append(newEntry)
  
 return ans


def adjust_entry(entry):
 a = HS_entries(entry)  # list of newEntry objects
 b = S_entries(entry)   # list of newEntry objects
 newEntries = a + b
 entry.newEntries = newEntries
  
def write_entries(fileout,entries):
 with codecs.open(fileout,"w","utf-8") as f:
  n = 0
  for entry in entries:
   for newEntry in entry.newEntries:
    n = n + 1
    f.write('<edit L="%s">\n' % newEntry.L)
    for line in newEntry.lines:
     f.write(line + '\n')
    f.write('</edit>\n')
 print(n,"sections written to",fileout)
 
if __name__=="__main__":
 filein = sys.argv[1] # corrected verses
 fileout = sys.argv[2] # easier format
 entries = get_entries(filein)
 for entry in entries:
  adjust_entry(entry)  # add additional attribute(s)
 write_entries(fileout,entries)
 
 

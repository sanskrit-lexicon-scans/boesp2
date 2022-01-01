# coding=utf-8
"""diff_verses1.py
 
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

def check1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 nprob = 0
 for iline,line in enumerate(lines):
  if re.search(r'^; [0-9]',line):
   if not lines[iline-1].startswith('; --------'):
    print('problem at line',iline+1)
    nprob = nprob + 1
 print(nprob,"problems in",filein)

def check(entries1,entries2):
 n1 = len(entries1)
 n2 = len(entries2)
 # same number of entries
 if n1 != n2:
  print('problem: different number of entries')
  exit(1)
 # same entry ids
 nprob = 0
 for ientry,entry1 in enumerate(entries1):
  entry2 = entries2[ientry]
  if entry1.Ls != entry2.Ls:
   nprob = nprob+1
   print('different Ls at entry',ientry+1)
   print('%s != %s' %(entry1.Ls,entry2.Ls))
 if nprob != 0:
  exit(1)
 # same number of sanskrit lines
 nprob = 0
 for ientry,entry1 in enumerate(entries1):
  entry2 = entries2[ientry]
  if len(entry1.S) != len(entry2.S):
   nprob = nprob+1
   print('different number of verse lines at entry',entry1.Ls)
 #if nprob != 0:
 # exit(1)

def diff_entries_S(entries1,entries2):
 ans = []
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  n = len(e1.S)
  cat = None
  if n != len(e2.S):
   cat = '# lines different'
  else:
   difflines = []
   for i,line1 in enumerate(e1.S):
    line2 = e2.S[i]
    # don't worry about spaces before/after
    line1a = line1.strip()
    line2a = line2.strip()
    if line1a != line2a:
     vl = i+1
     difflines.append('%s' %vl)
   if difflines != []:
    ndiff = len(difflines)
    diffstr = ','.join(difflines)
    if ndiff == 1:
     cat = 'difference at verse line %s' % diffstr
    else:
     cat = 'differences at verse lines %s' % diffstr
  if cat != None:
   Ls = e1.Ls
   msg = 'Verse %s: %s' %(Ls,cat)
   ans.append((ientry,msg))
 return ans

def diff_entries_S1(entries1,entries2):
 ans = []
 for ientry,e1 in enumerate(entries1):
  e2 = entries2[ientry]
  n = len(e1.S)
  cat = None
  if n != len(e2.S):
   cat = '# lines different'
   print(e1.Ls,'# lines different')
   exit(1)
  else:
   difflines = []
   for i,line1 in enumerate(e1.S):
    line2 = e2.S[i]
    # don't worry about spaces before/after
    line1a = line1.strip()
    line2a = line2.strip()
    if line1a != line2a:
     vl = i+1
     ans.append((vl,e1.Ls,line1a,line2a))
 return ans

if __name__=="__main__":
 filein1 = sys.argv[1] # first version
 filein2 = sys.argv[2] # second version
 fileout = sys.argv[3] #
 #check1(filein1)
 #check1(filein2)
 #exit(1)
 entries1 = get_entries(filein1)
 entries2 = get_entries(filein2)
 check(entries1,entries2)
 diffs = diff_entries_S1(entries1,entries2)
 print(len(diffs),'lines with differences in Sanskrit verse')
 
 with codecs.open(fileout,"w","utf-8") as f:
  for vl,Ls,line1,line2 in diffs:
   outarr = []
   outarr.append('; -------------------------------------')
   outarr.append('Verse %s: difference at line %s' %(Ls,vl))
   outarr.append('%s' % line1)
   outarr.append('%s' % line2)
   for out in outarr:
    f.write(out+'\n')
 print(len(diffs),"written to",fileout)
 

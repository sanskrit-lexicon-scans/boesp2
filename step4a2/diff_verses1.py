# coding=utf-8
"""diff_verses1.py (step4a2)
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step4a1')
# the Edit class initializer
from update_xml_verses import get_edits

def unused_check1(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 nprob = 0
 for iline,line in enumerate(lines):
  if re.search(r'^; [0-9]',line):
   if not lines[iline-1].startswith('; --------'):
    print('problem at line',iline+1)
    nprob = nprob + 1
 print(nprob,"problems in",filein)

def check(edits1,edits2):
 n1 = len(edits1)
 n2 = len(edits2)
 # same number of edits
 if n1 != n2:
  print('problem: different number of edits')
  exit(1)
 # same edit ids
 nprob = 0
 for iedit,edit1 in enumerate(edits1):
  edit2 = edits2[iedit]
  if edit1.L != edit2.L:
   nprob = nprob+1
   print('different Ls at edit',iedit+1)
   print('%s != %s' %(edit1.L,edit2.L))
  elif len(edit1.lines) != len(edit2.lines):
   nprob = nprob + 1
   print('different number of edit lines at L="%s"' %edit1.L)
 if nprob != 0:
  exit(1)

def unused_diff_edits_S(edits1,edits2):
 ans = []
 for iedit,e1 in enumerate(edits1):
  e2 = edits2[iedit]
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
   ans.append((iedit,msg))
 return ans

def diff_edits_S1(edits1,edits2):
 ans = []
 for iedit,e1 in enumerate(edits1):
  e2 = edits2[iedit]
  n = len(e1.lines) # same as e2.lines by check function
  lines1 = e1.lines
  lines2 = e2.lines
  for i,line1 in enumerate(lines1):
   line2 = lines2[i]
   # don't worry about spaces before/after
   line1a = line1.strip()
   line2a = line2.strip()
   if line1a != line2a:
    vl = i+1
    ans.append((vl,e1.L,line1a,line2a))
 return ans

if __name__=="__main__":
 filein1 = sys.argv[1] # first version
 filein2 = sys.argv[2] # second version
 fileout = sys.argv[3] #
 edits1 = get_edits(filein1)
 edits2 = get_edits(filein2)
 check(edits1,edits2)
 diffs = diff_edits_S1(edits1,edits2)
 print(len(diffs),'lines with differences in Sanskrit verse')
 
 with codecs.open(fileout,"w","utf-8") as f:
  for vl,L,line1,line2 in diffs:
   outarr = []
   outarr.append('; -------------------------------------')
   outarr.append('Verse %s: difference at line %s' %(L,vl))
   outarr.append('%s' % line1)
   outarr.append('%s' % line2)
   for out in outarr:
    f.write(out+'\n')
 print(len(diffs),"written to",fileout)
 

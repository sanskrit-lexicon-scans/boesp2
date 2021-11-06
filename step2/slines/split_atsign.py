# coding=utf-8
""" split_atsign.py
 
"""
from __future__ import print_function
import sys, re,codecs

def generate_s(lines):
 start = False
 inS = False
 group = []
 for iline,line in enumerate(lines):
  # skip 'header' lines
  if not start:
   if line.startswith('<H> Boehtlingk'):
    start = True
   continue
  if not inS:
   # look for line starting with '<S>'
   if line.startswith('<S>'):
    inS = True
    group = [(iline,line)]
   else:
    pass
  else:
   # inS. Look for 'empty' line
   if line.strip() == '':
    yield group
    inS = False
    group = []
   else:
    # continue building group
    group.append((iline,line))
 # there should be no open S-group at the end.
 assert inS == False
def changes_s(sgroup):
 # sgroup is a list of 2-tuples iline,line
 # check each line ends with middle-dot plus space
 for iline,line in sgroup:
  if not line.endswith(''):
   print('ERROR. line expected to end with "· "')
   print(lnum,line)
   exit(1)
 # Gather the lines into a text blob, without line-break
 oldlines = [x[1] for x in sgroup]
 ilines = [x[0] for x in sgroup]
 text = ' '.join(oldlines)
 # remove the middle dot
 text = text.replace('·','')
 # now make sure dandas (single or double) are at the end of lines
 # Assume dandas represented by ascii vertical bar '|'
 # and make each line end with "· "
 # Correct 3 cases with two consecutive double-dandas
 text = text.replace('|| ||','||')
 text = re.sub(r'([|]+)',r'\1· ' +'\n',text)
 # remove \n at end of text
 if text.endswith('\n'):
  text = text[:-1] # remove \n
 # remove multiple spaces
 text = re.sub(r'  +',' ',text)
 newlines = text.split('\n')
 # remove initial spaces in newlines
 for i,x in enumerate(newlines):
  newlines[i] = x.lstrip()
 nold = len(oldlines)
 nnew = len(newlines)

 changes = []
 nmax = max(nold,nnew)
 if nold <= nnew:
  for i in range(nmax):
   if i<nold:
    i1 = i
    nl = newlines[i1]
    if nl == '':
     nl = ' '
    change = (ilines[i1],'new',oldlines[i1],nl)
   else:
    x = newlines[i]
    if x.strip() == '':
     break
    change = (ilines[i1],'ins',oldlines[i1],newlines[i])
   changes.append(change)
 else: # nnew < nold
  for i in range(nmax):
   if i<nnew:
    i1 = i
    nl = newlines[i1]
    if nl == '':
     nl = ' '
    change = (ilines[i1],'new',oldlines[i1],nl)
   else:
    change = [ilines[i],'new',oldlines[i],' ']
   changes.append(change)
    
 return changes

def generate_atgroups(lines):
 group = None
 for iline,line in enumerate(lines):
  if (iline % 4) == 0:
   if group != None:
    yield group
   group = [line]
  else:
   group.append(line)
 # last group
 yield group

class Atrec(object):
 def __init__(self,atgroup):
  self.identline = atgroup[1]
  self.atline1 = atgroup[2]
  self.atline2 = atgroup[3]
  assert ' @ ' in self.atline1
  try:
   assert ' @ ' in self.atline2
  except:
   print('ERROR: @ not in line2 for',self.identline)
   exit(1)
  self.matchline1 = self.atline1.replace(' @ ',' ')
  self.matchline2 = self.atline2.replace(' @ ',' ')
  self.used = 0
  self.changes = []
  if False:
   if self.identline.startswith('; 75 : '):
    print('Atrec debug. matchline1="%s"' %self.matchline1)
   print('first Atrec')
   for x in atgroup:
    print(x)
   exit(1)
  
def init_atrecs(lines):
 """ lines are in  groups of 4 lines
 """
 atgroups = list(generate_atgroups(lines))
 print(len(atgroups),"at groups found")
 recs = [Atrec(atgroup) for atgroup in atgroups]
 d1 = {}
 d2 = {}
 for rec in recs:
  key = rec.matchline1
  if key in d1:
   print('d1 duplicate',key)
  d1[key] = rec
  key = rec.matchline2
  if key in d2:
   print('d2 duplicate',key)
  d2[key] = rec
  
 return recs,d1,d2

filetemp = 'temp_correction.txt'
ftemp = codecs.open(filetemp,'w','utf-8')
def temp_correction(x,lines):
 y = x[0:30]
 found = False
 for iline,line in enumerate(lines):
  if y in line:
   found = True
   break
 if not found:
  print('NOT FOUND:',x)
  # print a change transaction
  outarr = []
  outarr.append('; ATREC= %s'%x)
  lnum = iline+1
  outarr.append('%s old %s'% (lnum,line))
  outarr.append('%s new %s'% (lnum,line))
  outarr.append(';')
  for out in outarr:
   ftemp.write(out+'\n')

def restrict_to_at(sgroups):
 ans = []  # sublist of sgroups
 for sgroup in sgroups:
  nfound = 0
  for iline,line in sgroup:
   if ' @ ' in line:
    nfound = nfound + 1
  if nfound == 0:
   continue
  assert nfound == 2  # 2 lines with '@'
  ans.append(sgroup)
 print(len(ans),'S groups with @')
 return ans

def split_at_changes_3(sgroup,lines):
 ans = []
 ans.append('; ----------------------------------')
 iline0 = sgroup[0][0]
 try:
  assert lines[iline0+2].startswith('[Seite')
  assert lines[iline0+3] == ' '
  assert lines[iline0+4] == ' '
  assert lines[iline0+5] == ' ' # the group separator blank line
  new1,new2 = lines[iline0].split(' @ ')
  new3,new4 = lines[iline0+1].split(' @ ')
  new1 = new1 + '· '  # temporary ending of lines for Thomas and Kedit
  new3 = new3 + '. '
  new5 = lines[iline0+2] # the Seite line
  newlines = [new1,new2,new3,new4,new5]
  oldlines = lines[iline0:iline0+5]
  ilines = range(iline0,iline0+5)
  for i,iline in enumerate(ilines):
   lnum = iline+1
   old = oldlines[i]
   new = newlines[i]
   ans.append('%s old %s' %(lnum,old))
   ans.append('%s new %s' %(lnum,new))
 except:
  print('split_at_changes_3 ERROR at lnum=',iline0+1)
  exit(1)
 return ans

def split_at_changes_2(sgroup,lines):
 ans = []
 ans.append('; ----------------------------------')
 iline0 = sgroup[0][0]
 try:
  assert lines[iline0+2] == ' '
  assert lines[iline0+3] == ' '
  assert lines[iline0+4] == ' ' # the group separator blank line
 except:
  print('split_at_changes_2 ERROR at lnum=',iline0+1)
  exit(1)
  
 new1,new2 = lines[iline0].split(' @ ')
 new3,new4 = lines[iline0+1].split(' @ ')
 new1 = new1 + '· '  # temporary ending of lines for Thomas and Kedit
 new3 = new3 + '. '
 newlines = [new1,new2,new3,new4]
 oldlines = lines[iline0:iline0+4]
 ilines = range(iline0,iline0+4)
 for i,iline in enumerate(ilines):
  lnum = iline+1
  old = oldlines[i]
  new = newlines[i]
  ans.append('%s old %s' %(lnum,old))
  ans.append('%s new %s' %(lnum,new))
 return ans

def split_at_changes(sgroup,lines):
 # we know that there are 2 atlines (see restrict_to_at in sgroup
 # each of these will split into 2 lines
 # check that there are enough blank lines
 # sometimes, there is a page break line [seite..] after 2nd s-line
 # sgroup is an array of (iline,line) 2-tuples
 iline0 = sgroup[0][0]
 if len(sgroup) == 3:
  ans = split_at_changes_3(sgroup,lines)
 elif len(sgroup) == 2:
  ans = split_at_changes_2(sgroup,lines)
 else:
  print('split_at_changes ERROR:',len(sgroup),' wrong number of lines in group')
  exit(1)
 return ans
if __name__=="__main__":
 filein = sys.argv[1] # temp_boesp_N.txt
 fileout = sys.argv[2] # change transactions
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 sgroups = list(generate_s(lines))
 print(len(sgroups),"S-groups found")
 sgroups_at = restrict_to_at(sgroups)
 outrecs = []
 for sgroup in sgroups_at:
  outarr = split_at_changes(sgroup,lines)
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"S-groups changes written to",fileout)

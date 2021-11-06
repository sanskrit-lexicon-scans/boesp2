# coding=utf-8
""" match_atsign.py
 
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
 
if __name__=="__main__":
 filein = sys.argv[1] # boesp_utf8.txt
 fileinat = sys.argv[2] # work_san_hk_atsign.txt
 fileout = sys.argv[3] # change transactions
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 with codecs.open(fileinat,encoding='utf-8',mode='r') as f:
  linesat = [x.rstrip('\r\n') for x in f]
 sgroups = list(generate_s(lines))
 print(len(sgroups),"S-groups found")
 atrecs,d1,d2 = init_atrecs(linesat)
 
 outrecs = []
 nat = 0
 for sgroup in sgroups:
  if len(sgroup) != 2:
   # these groups not relevant 
   # but there are some groups with 3 elements, whose third line starts with [Seite
   if (len(sgroup) == 3) and (sgroup[2][1].startswith('[Seite')):
    pass  # continue this sgroup
   else:
    continue # skip this sgroup
  iline1,line1 = sgroup[0]
  iline2,line2 = sgroup[1]
  line1a = re.sub(r'^<S> (.*?)· ',r'\1',line1)
  if line1a not in d1:
   continue
  line2a = re.sub(r'^(.*?)· ',r'\1',line2)
  
  if line2a not in d2:  # detect changes.  These now resolved
   #print('ERROR: found line1 but not line2')
   #print('line1 ',iline1+1,line1)
   print('%s old %s' %(iline2+1,line2))
   print('%s new %s' %(iline2+1,line2))
   print(';')
   continue
   #exit(1)
  rec1 = d1[line1a]
  rec2 = d2[line2a]
  assert rec1 == rec2
  rec = rec1
  rec.used = rec.used + 1
  nat = nat + 1
  # generate outarr, which will change line1 and line2
  outarr = ['; -----------------------------------------------']
  # first, line1
  lnum = iline1 + 1
  old = line1
  new = '<S> %s· ' % rec.atline1
  outarr.append('%s old %s' %(lnum,old))
  outarr.append('%s new %s' %(lnum,new))
  # next, line2
  outarr.append(';')
  lnum = iline2 + 1
  old = line2
  new = '%s· ' % rec.atline2
  outarr.append('%s old %s' %(lnum,old))
  outarr.append('%s new %s' %(lnum,new))
  outrecs.append(outarr)
 print(nat,"matches found")
 # check for unused atrecs
 for rec in atrecs:
  if rec.used == 1:
   continue
  assert rec.used == 0
  print('unmatched:',rec.matchline1)
  #temp_correction(rec.matchline1,lines)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"S-groups written to",fileout)

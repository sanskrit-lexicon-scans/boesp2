# coding=utf-8
""" change_s.py
 
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
if __name__=="__main__":
 filein = sys.argv[1] # boesp_utf8.txt
 fileout = sys.argv[2] # boesp.xml
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 sgroups = list(generate_s(lines))
 print(len(sgroups),"S-groups found")
 outrecs = []
 for sgroup in sgroups:
  newchanges = changes_s(sgroup)
  outarr = ['; -----------------------------------------------']
  for c in newchanges:
   iline,changetype,old,new = c
   lnum = iline+1
   outarr.append('%s old %s' % (lnum,old))
   outarr.append('%s %s %s' % (lnum,changetype,new))
   if new == '':
    print('Unexpected empty string',lnum)
    exit(1)
   outarr.append(';')
  outrecs.append(outarr)
 # write outrecs
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"S-groups written to",fileout)

#-*- coding:utf-8 -*-
"""reformat_atsign.py
  
  Assumes presence of 'middledot+space' at end of non-blank lines
  Does not change number of lines
 
"""
from __future__ import print_function
import sys, re,codecs

def generate_groups(lines):
 iline = 0 # start at first line
 nlines = len(lines)
 ngroup = 0
 # ignore blank lines
 dbg = False
 while iline < nlines:
  group = []
  while (lines[iline].strip() == ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    break
   
  if group != []:
   # group of blank lines
   ngroup = ngroup + 1
   if dbg: print('A',ngroup,group[0])
   yield(group)
   #continue
  # gather block of non-blank lines
  group = []
  try:
   while ((iline<nlines) and (lines[iline].strip() != '')):
    group.append(lines[iline])
    iline = iline + 1
    if iline == nlines:
     break
  except:
   print('generate_groups ERROR. lnum=',iline+1)
   exit(1)
  ngroup = ngroup + 1
  if dbg: print('B',ngroup,group[0])
  yield group
  if dbg: 
   if ngroup > 10:
    print('debug exit')
    return

def reformat_s_group(group,group1):
 # group1 is the group of blank lines following the s-group
 # Change both groups
 mds = '· '  # each line in group should end in middle-dot + space
 ngroup = len(group)
 ngroup1 = len(group1)
 assert group[0].startswith('<S>')
 if '@' not in group[0]:
  if '@' in group[1]:
   print('\n'.join(group))
  # nothing to do
  return group,group1
 if False:  # checks
  assert ngroup in [2,3]
  assert '@' in group[1]
  if ngroup == 3:
   try:
    assert group[2].startswith('[Seite')
   except:
    print('\n'.join(group))
  return group,group1
 lines = []
 lines = lines + group[0].split('@')
 lines = lines + group[1].split('@')
 if ngroup == 3:
  lines.append(group[2]) # [Seite..]
 nlines = len(lines)
 assert (ngroup+2) == nlines
 assert 3 <= ngroup1
 lines1 = group1[2:]
 assert 1 <= len(lines1)
 # some additional editing of lines
 lines[0] = lines[0].rstrip() + ' '+mds
 lines[1] = lines[1].lstrip()
 lines[2] = lines[2].rstrip() + ' ' + mds
 lines[3] = lines[3].lstrip()
 return lines,lines1

def reformat_s_groups(lines):
 ngroup = 0
 firstfound = False
 nlines = 0
 newgroups = []
 dbg = False
 allgroups = list(generate_groups(lines))
 ngroups = len(allgroups)
 nchange = 0 # number of <S> groups changed
 print(ngroups, 'groups found')
 for igroup,group in enumerate(allgroups):
  ngroup = ngroup+1
  nlines = nlines + len(group)
  # skip the groups until a condition is met
  if firstfound:
   if len(group) == 0:
    print('Empty group found at',ngroup,nlines)
    continue
   if group[0].startswith('<S>'):
    nextgroup = allgroups[igroup+1] # blank line group 
    newgroup,newnextgroup = reformat_s_group(group,nextgroup)
    allgroups[igroup+1]=newnextgroup
    if newgroup != group:
     nchange = nchange+1
   elif group[0].strip() == '':
    # empty group
    newgroup = group
   else:
    newgroup = group
  elif group[0].startswith('<H> Boehtlingk'):
   firstfound = True
   newgroup = group
  else: # before first found
   newgroup = group
  newgroups.append(newgroup)
 print(nchange,'<S> groups changed')
 # reconstruct array of lines
 newlines = []
 for group in newgroups:
  for line in group:
   newlines.append(line)
 return newlines

def read(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"lines read from",filein)
 return lines

def write(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line+'\n')
 print('write:',len(lines),'lines written to',fileout)

if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[2] # same number of lines, but transcoded
 lines = read(filein)

 newlines = reformat_s_groups(lines)
 write(fileout,newlines)
 

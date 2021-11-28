#-*- coding:utf-8 -*-
"""merge_hs.py
  Read <HS> groups.
  If there is more than one line,  merge into one line
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

def merge_HS(group):
 mds = '· '  # each line in group should end in middle-dot + space
 ngroup = len(group)
 if ngroup == 1:
  # no merger needed
  return group
 lines = []
 for iline,line in enumerate(group):
  assert line.endswith(mds)
  # replace mds with space, except for last
  if (iline+1) == ngroup:
   lines.append(line)
  else:
   lines.append(line[0:-2])
 text = ' '.join(lines) # the merged line.
 # Set first newline to text.
 # Set additional newlines to ' '
 newlines = []
 for iline,line in enumerate(group):
  if iline == 0:
   newlines.append(text)
  else:
   newlines.append(' ')
 return newlines

def merge_hs_groups(lines):
 ngroup = 0
 firstfound = False
 nlines = 0
 newgroups = []
 dbg = False
 allgroups = list(generate_groups(lines))
 ngroups = len(allgroups)
 print(ngroups, 'groups found')
 for group in allgroups:
  ngroup = ngroup+1
  nlines = nlines + len(group)
  # skip the groups until a condition is met
  if firstfound:
   if len(group) == 0:
    print('Empty group found at',ngroup,nlines)
    continue
   if group[0].startswith('<HS>'):
    newgroup = merge_HS(group)
    if dbg:
     temp1 = '\n'.join(group)
     if '[Seite' in temp1:
      print('old:\n',temp1)
      temp = '\n'.join(newgroup)
      print('new:\n',temp)
      dbg = False
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
 newlines = merge_hs_groups(lines)
 write(fileout,newlines)
 

#-*- coding:utf-8 -*-
"""change_unbalanced.py
 
"""
import sys,re,codecs
from as_1 import generate_entries, read_and_clean_lines
sys.stdout.reconfigure(encoding='utf-8') 
class Change(object):
 def __init__(self,metaline,page,iline,old,new,reason):
  self.metaline = metaline
  self.page = page
  self.iline = iline
  self.old = old
  self.new = new
  self.reason = reason

def change1_pct(line):
 # search for unbalanced {%
 
 parts = re.split(r'(Seite[0-9][.][0-9])|(<F>[0-9.]+\))',line)
 newparts = []
 for part in parts:
  if part == None:
   continue
  if part.startswith('Seite'):
   newpart = part
  elif part.startswith('<F>'):
   newpart = part
  else:
   newpart = re.sub(r'[.]([0-9])',r'. \1',part)
  newparts.append(newpart)
 newline = ''.join(newparts)
 return newline   

def init_changes(lines):
 changes = [] # array of Change objects
 metaline = None
 page = None
 for iline,line in enumerate(lines):
  line = line.rstrip('\r\n')
  oldline = line
  # generate change
  if option == '1':
   newline = change1_pct(line)
  elif option == '2':
   newline = change1_pound(line)
  if newline == None: # error
   print('ERROR:',iline+1,"\n",line)
   exit(1)
  if newline == oldline:
   continue
  reason = None
  change = Change(metaline,page,iline,oldline,newline,reason)
  changes.append(change)
 print(len(changes),'potential changes found')
 return changes

def change_out(change,ichange):
 outarr = []
 case = ichange + 1
 #outarr.append('; TODO Case %s: (reason = %s)' % (case,change.reason))
 ident = change.metaline
 if ident == None:
  ident = change.page
 #outarr.append('; ' + ident)
 lnum = change.iline + 1
 outarr.append('%s old %s' % (lnum,change.old))
 #outarr.append(';')
 outarr.append('%s new %s' % (lnum,change.new))
 outarr.append(';')
 return outarr

def write_changes(fileout,changes):
 with codecs.open(fileout,"w","utf-8") as f:
  for ichange,change in enumerate(changes):
   outarr = change_out(change,ichange)
   for out in outarr:
    f.write(out+'\n')
 print(len(changes),"written to",fileout)


if __name__=="__main__":
 filein = sys.argv[1] #  xxx.txt (path to boesp)
 fileout = sys.argv[2] # change transactions
 lines = read_and_clean_lines(filein)
 entries = list(generate_entries(lines))
 for entry in entries:
  groups = entry.groups
  for group in groups:
   text = '\n'.join(group)
   n1 = len(re.findall(r'{%',text,re.DOTALL))
   n2 = len(re.findall(r'%}',text,re.DOTALL))
   if n1!= n2:
    print('% prob',group[0])
   n1 = len(re.findall(r'{#',text,re.DOTALL))
   n2 = len(re.findall(r'#}',text,re.DOTALL))
   if n1!= n2:
    print('# prob',group[0])
    
 exit(1)
 n = 0
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 changes = init_changes(lines,option)
 write_changes(fileout,changes)


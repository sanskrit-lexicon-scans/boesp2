"""
make_change_utf8_xml.py

   
"""
import sys,re,codecs

class Change:
 def __init__(self,old,new):
  m = re.search(r'^([^ ]+) old (.*)$',old)
  self.lnum = m.group(1)
  self.oldline = m.group(2)
  m = re.search(r'^([^ ]+) new (.*)$',new)
  if m == None:
   print('CHANGE ERROR 1')
   print(old)
   print(new)
   exit(1)
  assert m.group(1) == self.lnum
  self.newline = m.group(2)
  # adjustment for middle dot and ending space, which are absent in boesp.xml
  self.old = re.sub(r'· +','',self.oldline)
  self.new = re.sub(r'· +','',self.newline)
  self.skipthis = (self.old.rstrip() == self.new.rstrip())
  # lnum from matching line, or None
  self.lnumxml = None
  
def init_changes(filein):
 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f if not x.startswith(';')]
 changes = []
 nlines = len(lines)
 for i in range(0,nlines,2):
  a = lines[i]
  b = lines[i+1]
  change = Change(lines[i],lines[i+1])
  if change.skipthis:
   print('skipping change:')
   print('   '+a)
   print('   '+b)
  else:
   changes.append(change)
 print(len(changes),"read from",filein)
 return changes

def find_changes(lines,changes):
 # inefficient search
 for change in changes:
  old = change.old
  found = False
  for iline,line in enumerate(lines):
   if line == old:
    if found:
     print('DUPLICATE old:',old)
     continue
    change.lnumxml = iline+1
    found = True
    #break # stop for loop
  if change.lnumxml == None:
   print('not found: ',old)
 if True:
  notfound = len([c for c in changes if c.lnumxml == None])
  print(notfound,'not found')

def write_changes(fileout,changes):
 outrecs = []
 for change in changes:
  if change.skipthis:
   print('write_changes skipping ',self.oldline)
   continue
  outarr = []
  outarr.append('; -----------------------------------------------------')
  outarr.append('%s old %s' %(change.lnumxml,change.old))
  outarr.append('%s new %s' %(change.lnumxml,change.new))
  outrecs.append(outarr)
 # now to output
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for line in outarr:
    f.write(line + '\n')
 print(len(outrecs),"written to",fileout)
 
if __name__ == "__main__":
 filein = sys.argv[1]
 filechg = sys.argv[2]
 fileout = sys.argv[3]

 with codecs.open(filein,"r","utf8") as f:
  lines = [x.rstrip('\r\n') for x in f]
 changes = init_changes(filechg)
 find_changes(lines,changes)
 write_changes(fileout,changes)
 exit(1)

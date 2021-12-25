# coding=utf-8
""" hsrevise.py
 
"""
from __future__ import print_function
import sys, re,codecs


class Entry(object):
 def __init__(self,lines):
  self.lines = lines
  if lines[0] != '<entry>':
   print('Entry start error:','\n'.join(lines))
   exit(1)
  if lines[-1] != '</entry>':
   print('Entry end error:','\n'.join(lines))
   exit(1)
  self.parse_info()
  self.parse_groups()
  return
 def parse_info(self):
  if len(self.lines) < 2:
   print('entry parse_info Error 1','\n'.join(self.lines))
   exit(1)
  infoline = self.lines[1]
  m = re.search(r'<info L="(.*?)" page="(.*?)" gtypes="(.*?)"/>',infoline)
  if m == None:
   print('entry parse_info Error 2','\n'.join(self.lines))
   exit(1)
  self.L = m.group(1)
  self.page = m.group(2)
  self.gtypes = m.group(3).split(',')
  self.info = infoline
 def parse_groups(self):
  # groupelts agrees with  boesp.dtd
  groupelts = 'HS,S,D,FDUMMY,F,V1,V2,V3,V4,V5'.split(',')
  groupbegs = ['<%s' % groupelt for groupelt in groupelts]
  groupends = ['</%s>' % groupelt for groupelt in groupelts]
  groups = []
  ngroup = -1
  groupelt = None
  for iline,line in enumerate(self.lines):
   if groupelt == None:
    for i,groupbeg in enumerate(groupbegs):
     if line.startswith(groupbeg):
      groupelt = groupelts[i]
      groupend = groupends[i]
      group = [line]
      break
   elif line.startswith(groupend):
    group.append(line)
    groups.append(group)
    ngroup = ngroup + 1
    if False: #dbg
     print('ngroup=',ngroup)
     print('\n'.join(group))
     print()
    #print 
    # check agreement with gtypes
    if groupelt != self.gtypes[ngroup]:
     print('parse_groups error 1',groupelt,self.gtypes[ngroup])
     print('info=',self.info)
     exit(1)
    groupelt = None
    group = []
   else:
    group.append(line)
  self.groups = groups
  if len(groups) != len(self.gtypes):
   print('parse_groups error 2')
   print('gtypes=',self.gtypes)
   print('#groups=',len(groups))
   print('info=',self.info)
   exit(1)

  
def xml_header(xmlroot):
 # write header lines
 text = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE %s SYSTEM "%s.dtd">
<!-- <H> Boehtlingk, Indische Sprüche, 2. Auflage, St. Petersburg 1870 -->
<%s>
""" % (xmlroot,xmlroot,xmlroot)
 lines = text.splitlines()
 lines = [x.strip() for x in lines if x.strip()!='']
 return lines

def generate_entries(lines):
 # lines of xml file
 # yield array of entries
 inentry = False
 elines = []
 for iline,line in enumerate(lines):
  if not inentry:
   line = line.strip() # remove extra spaces
   if line != '<entry>':
    continue
   # start entry
   inentry = True
   elines = [line]
  else:
   # looking for closing </entry>
   line1 = line.strip()
   if line1 == '</entry>':
    elines.append(line1)
    entry = Entry(elines)
    yield entry
    inentry = False
    elines = []
   else:
    elines.append(line)
 return

def xml_body(entries,tranin):
 # generate xml header lines
 body = []
 nentry = 0
 for entry in entries:
  outarr = entrylines(entry,tranin)
  nentry = nentry + 1
  for out in outarr:
   body.append(out)
 print(nentry,'entries found')
 return body

def entry_from_group(group,L,page,gtype):
 # construct new entry 
 lines = ['<entry>']
 info = '<info L="%s" page="%s" gtypes="%s"/>' % (L,page,gtype)
 lines.append(info)
 for line in group:
  lines.append(line)
 lines.append('</entry>')
 entry = Entry(lines)
 return entry

def L_previous(L):
 if ',' in L:
  print('WARNING HS in multi-L:',L)
  Ls = L.split(',')
  L = Ls[0]
 Lint = int(L) # assume L consists just of digits
 Lprevint = Lint - 1
 Lprev = '%s' % Lprevint
 return Lprev

def HS_adjust(entry):
 """ Return a list of entries.
  If entry has one or more 'HS' groups, 
   remove then from entry and
   construct a new entry for each HS group
  return list of new HS-entries along with adjusted entry
 """
 dbg = False
 if 'HS' not in entry.gtypes:
  return [entry]  # no change
 newentries = [] # the new HS entries
 newgroups = []  # the non-HS groups
 newgtypes = []
 nhs = 0 # number of HS entries
 L = entry.L
 Lprev = L_previous(L)
 page = entry.page
 for i,gtype in enumerate(entry.gtypes):
  group = entry.groups[i] # the lines of the group
  if gtype == 'HS':
   nhs = nhs + 1
   Lnew = "%s.%s" %(Lprev,nhs)
   newentry = entry_from_group(group,Lnew,page,gtype)
   newentries.append(newentry)
  else:
   newgroups.append(group)
   newgtypes.append(gtype)
 # construct new info element
 info = '<info L="%s" page="%s" gtypes="%s"/>' % (L,page,','.join(newgtypes))
 # construct new lines attribute
 newlines = ['<entry>']
 newlines.append(info)
 for group in newgroups:
  for line in group:
   newlines.append(line)
 newlines.append('</entry>')
 newentry = Entry(newlines)
 newentries.append(newentry)
 return newentries

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  nprob = 0
  lines = []
  for iline,line in enumerate(f):
   line = line.rstrip('\r\n')
   lines.append(line)
 print(len(lines),"lines read from",filein)
 if nprob != 0:
  print('read_and_clean_lines:',nprob,'problems need to be fixed')
  exit(1)
 return lines

 
def write_entries(entries,xmlroot,fileout):
 head = xml_header(xmlroot)
 head.append('')
 body = []
 for entry in entries:
  lines = entry.lines
  for line in lines:
   body.append(line)
  body.append('')
 tail = ['</%s>'%xmlroot]
 linesout = head + body  + tail
 with codecs.open(fileout,"w","utf-8") as f:
  for line in linesout:
   f.write(line+'\n')
 print(len(linesout),"lines written to",fileout)
 
def test(filein,fileout):
 # Try this as experiment.
 # write drastically changes the file.
 # Conclusion: don't use ET
 import xml.etree.ElementTree as ET
 tree = ET.parse(filein)
 tree.write(fileout)
 
 print("test constructs",fileout)
 exit(1)
 
if __name__=="__main__":
 tranin = 'hk'

 filein = sys.argv[1] # boesp_utf8.xml
 fileout = sys.argv[2] # boesp_utf8_revised.xml
 xmlroot = 'boesp'
 lines = read_lines(filein)
    
 entries0 = list(generate_entries(lines))
 print(len(entries0),'entries found')
 entries = []
 for entry0 in entries0:
  newentries = HS_adjust(entry0)
  for entry in newentries:
   entries.append(entry)
 write_entries(entries,xmlroot,fileout)
 
 exit(1)

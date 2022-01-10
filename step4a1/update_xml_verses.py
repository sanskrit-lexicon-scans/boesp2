# coding=utf-8
"""update_xml_verses.py
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step3e')
# the Entry object
from transcode import xml_header,read_entries

class Edit(object):
 def __init__(self,lines):
  self.lines = lines
  assert lines[0] == '<edit>'
  assert lines[-1] == '</edit>'
  m = re.search(r'^<info L="(.*?)" page="(.*?)" gtypes="(.*?)"/>$',lines[1])
  assert m != None
  self.L = m.group(1)
  self.page = m.group(2)
  #self.gtypestr = m.group(3)
  #self.gtypes = self.gtypestr.split(',')
  self.parse_edit_groups()
  
 def parse_edit_groups(self):
  # based on Entry.parse_groups
  groupelts = 'HS,S,D,F,V1,V2,V3,V4,V5'.split(',')
  groupbegs = ['<%s' % groupelt for groupelt in groupelts]
  groupends = ['</%s>' % groupelt for groupelt in groupelts]
  groups = []
  ngroup = -1
  groupelt = None
  gtypes = [] # edit gtypes
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
    gtypes.append(groupelt)
    groupelt = None
    group = []
   else:
    group.append(line)
  self.groups = groups
  self.gtypes = gtypes
   
def generate_edits(lines):
 group = None
 for iline,line in enumerate(lines):
  line = line.strip()
  if line == '<edit>':
   group = [line]
  elif line == '</edit>':
   group.append(line)
   entry = Edit(group)
   yield entry
   group = None
   L = None
  elif group != None:
   group.append(line)
  else:
   pass  # outside of a group, e.g. ;---------- lines

def get_edits(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 edits = list(generate_edits(lines))
 print(len(edits),"edits from",filein)
 return edits

def entry_dict(entries):
 d = {}
 for entry in entries:
  L = entry.L
  if L in d:
   print('entry_dict: unexpected duplicate',entry.infoline)
  d[L] = entry
 return d

def edit_entry(entry,edit):
 """
 """
 newgroups = []
 found = False
 info = entry.info
 assert info == edit.lines[1]
 gtypes = entry.gtypes
 groups = entry.groups
 egroups = edit.groups
 egtypes = edit.gtypes
 for igtype,gtype in enumerate(gtypes):
  group = groups[igtype]
  if not (igtype < len(egtypes)):
   newgroups.append(group)
   continue
  egtype = egtypes[igtype]
  assert egtype == gtype
  egroup = egroups[igtype]
  newgroups.append(egroup)
 entry.newgroups = newgroups

def compute_entry_lines(entry,newgroups):
 newlines = []
 newlines.append('<entry>')
 # assume no change needed in info
 newlines.append(entry.info)
 for newgroup in newgroups:
  for newline in newgroup:
   newlines.append(newline)
 newlines.append('</entry>')
 if len(entry.lines) != len(newlines):
  print('newlines anomaly',entry.info)
  print('entry.lines:')
  for line in entry.lines:
   print('   ',line)
  print('entry.newlines:')
  for line in newlines:
   print('   ',line)
  exit(1)
 return newlines

def write_entries(entries,xmlroot,version,fileout):
 head = xml_header(xmlroot,version)
 head.append('')
 body = []
 for entry in entries:
  groups = entry.groups
  newgroups = entry.newgroups
  if newgroups == None:
   newlines = entry.lines
  else:
   newlines = compute_entry_lines(entry,newgroups)
  #lines = entry.lines
  for line in newlines:
   body.append(line)
  body.append('')
 tail = ['</%s>'%xmlroot]
 linesout = head + body  + tail
 with codecs.open(fileout,"w","utf-8") as f:
  for line in linesout:
   f.write(line+'\n')
 print(len(linesout),"lines written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1]  # old boesp.xml
 filein1 = sys.argv[2] # corrected verses
 fileout = sys.argv[3] # new boesp.xml
 xmlroot = 'boesp'
 version = "1.4"  # this must agree with step0/boesp.dtd
 entries = read_entries(filein)
 edits = get_edits(filein1)
 d = entry_dict(entries)
 # also, add 'newgroups' attribute to each entry
 # so we can tell which entries have been edited.
 for entry in entries:
  entry.newgroups = None
 for iedit,edit in enumerate(edits):
  L = edit.L
  if L not in d:
   print('edit entry not found',L)
  else:
   entry = d[L]
   edit_entry(entry,edit)  #
   if True:
    if iedit == 0:
     print(edit.L)
     for line in edit.lines:
      print(line)
 write_entries(entries,xmlroot,version,fileout)
 
 

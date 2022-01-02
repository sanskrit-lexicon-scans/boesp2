# coding=utf-8
"""step4a/update_prep.py
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step3e')
# the Entry object
from transcode import xml_header,read_entries

class Edit(object):
 def __init__(self,L,lines):
  self.L = L
  self.lines = lines
  assert L != None
  
def generate_edits(lines):
 group = None
 L = None
 for iline,line in enumerate(lines):
  m = re.search(r'^<edit L="(.*?)">$',line)
  if m != None:
   group = []
   L = m.group(1)
  elif line == '</edit>':
   entry = Edit(L,group)
   yield entry
   group = None
   L = None
  else:
   group.append(line)

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
  first edit line is either <S n="L"> or <HS>
  In either case, there is just ONE group in entry.groups whose first line
  is the same. We find that group, and replace it's lines with the edit lines.
  Add extra attribute
 """
 newgroups = []
 found = False
 for igroup,group in enumerate(entry.groups):
  if group[0] == edit.lines[0]:
   found = True
   newgroup = edit.lines
   newgroups.append(newgroup)
  else:
   newgroups.append(group)
 if not found:
  print('edit_entry anomaly',entry.L)
 else:
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
 version = "1.3"  # this must agree with step0/boesp.dtd
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
 
 

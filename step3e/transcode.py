# coding=utf-8
""" transcode.py
 
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

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
  groupelts = 'HS,S,D,F,V1,V2,V3,V4,V5'.split(',')
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

  
def xml_header(xmlroot,version):
 # write header lines
 text = """
<?xml version="%s" encoding="UTF-8"?>
<!DOCTYPE %s SYSTEM "%s.dtd">
<!-- <H> Boehtlingk, Indische Sprüche, 2. Auflage, St. Petersburg 1870 -->
<%s>
""" % (version,xmlroot,xmlroot,xmlroot)
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

def write_entries(entries,xmlroot,version,fileout):
 head = xml_header(xmlroot,version)
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

def read_entries(filein):
 lines = read_lines(filein)    
 entries = list(generate_entries(lines))
 print(len(entries),'entries found')
 return entries

if __name__=="__main__":
 tranin = sys.argv[1]
 tranout = sys.argv[2]
 filein = sys.argv[3] # boesp_utf8.txt
 fileout = sys.argv[4] # stats on transcoded characters
 xmlroot = 'boesp'
 version = "1.3"
 entries = read_entries(filein)
 newentries = []
 def transcode_sub(m):
  x = m.group(1)
  y = transcoder.transcoder_processString(x,tranin,tranout)
  return '<s>%s</s>' % y
 for entry in entries:
  text = '\n'.join(entry.lines)
  # DOTALL flag required, since our <s>X</s> instances can have '\n' in X.
  textnew = re.sub(r'<s>(.*?)</s>',transcode_sub,text,flags=re.DOTALL)
  newlines = textnew.split('\n')
  newentry = Entry(newlines)
  newentries.append(newentry)
 write_entries(newentries,xmlroot,version,fileout)

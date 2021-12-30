# coding=utf-8
""" compchars.py
 
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

  
def xml_header(xmlroot):
 # write header lines
 text = """
<?xml version="1.3" encoding="UTF-8"?>
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

def update_chars(line,chars):
 # modify chars
 for c in line:
  if c in (' ','\n'):
   # don't count space and newline characters
   continue
  if c not in chars:
   chars[c] = 0
  chars[c] = chars[c] + 1
 
def find_nonhk_chars(line):
 hkletters = 'aAiIuUReoMH' + 'kgGcjJTDNtdnpbmyrlvhzSshL' + "'" + '|' +'0123456789'
 hkall = hkletters + ' ' + '\n' + '°-' + ',;(){}=?[]!'
 ans = []
 for c in line:
  if c not in hkall:
   if c not in ans:
    if True:
     ans.append(c)
 return ans


def write_chars(f,chars,title):
 outarr = []
 outarr.append(title)
 keys = sorted(chars.keys())
 for key in keys:
  outarr.append('%s %s' %(key,chars[key]))
 
 outarr.append('---------------------------------------------------')
 outarr.append('')
 for out in outarr:
  f.write(out+'\n')

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

def read_entries(filein):
 lines = read_lines(filein)    
 entries = list(generate_entries(lines))
 print(len(entries),'entries found')
 return entries

def countchar(stext,c):
 # stext = <s>X</s>
 text = stext[3:-4]  # drop <s> and </s>
 cs = [x for x in text if x == c]
 n = len(cs)
 return n
def compchar(entryhk,entryslp1,charhk,charslp1):
 texthk = '\n'.join(entryhk.lines)
 hks = re.findall(r'<s>.*?</s>',texthk,re.DOTALL)
 textslp1 = '\n'.join(entryslp1.lines)
 slp1s = re.findall(r'<s>.*?</s>',textslp1,re.DOTALL)
 assert len(hks) == len(slp1s)
 for i,hk in enumerate(hks):
  slp1 = slp1s[i]
  nhk = countchar(hk,charhk)
  nslp1 = countchar(slp1,charslp1)
  if nhk != nslp1:
   print(entryhk.info)
   print('  hk:',hk)
   print('slp1:',slp1)
   exit(1)
  
if __name__=="__main__":
 charhk = sys.argv[1]
 charslp1 = sys.argv[2]
 fileinhk = sys.argv[3] # boesp_utf8.txt
 fileinslp1 = sys.argv[4] # boesp_slp1.txt
 fileout = sys.argv[5] # instances with differences
 xmlroot = 'boesp'
 entrieshk = read_entries(fileinhk)
 entriesslp1 = read_entries(fileinslp1)
 assert len(entrieshk) == len(entriesslp1)
 
 for ientry,entryhk in enumerate(entrieshk):
  entryslp1 = entriesslp1[ientry]
  compchar(entryhk,entryslp1,charhk,charslp1)
 exit(1)
 if True:
  text = '\n'.join(entry.lines)
  
  for m in re.finditer(r'<s>(.*?)</s>',text,re.DOTALL):
   santext = m.group(1)
   update_chars(santext,chars)
   if tranin == 'hk':
    nonhk_chars = find_nonhk_chars(santext)
    if len(nonhk_chars)!= 0:
     print(entry.info,nonhk_chars)
 with codecs.open(fileout,"w","utf-8") as f:
  write_chars(f,chars,'Characters in <s>')
 print('Sanskrit character frequency written to',fileout)


 

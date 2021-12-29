# coding=utf-8
""" improve_S.py
 
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

def S_adjust(entry):
 """ Return a list of entries.
  Add n attribute to S element, and for multiple D, 
  return adjusted entry (as a singleton list of entries)
 """
 dbg = False
 newentries = [] # 
 newgroups = []  # 
 newgtypes = []
 L = entry.L
 page = entry.page
 changed = False  # no changes to this entry
 # get the single S group:  It is the first group
 # If the first group is instead 'HS', nothing to change
 info = entry.info
 if entry.gtypes == ['HS']:
  return False,[entry]
 isgroup = 0
 sgroup = entry.groups[isgroup]
 # 
 # get list of verse numbers from info
 m = re.search(r'<info L="(.*?)"',info)
 Lstring = m.group(1)
 versenums = Lstring.split(',')
 # get list of verses, identified as sequence of lines with
 # last line ending in '||' (double danda)
 verselines = sgroup[1:-1]  # drop the <S> and </S> of the S-group
 verses = []
 verse = []
 pb = None
 for iline,line in enumerate(verselines):
  if re.search(r'<pb n=".*?"/>',line):
   pb = line
   if (iline+1) != len(verselines):
    print ('odd pb',info)  # there are none
   continue
  verse.append(line)
  if re.search(r'\|\| *$',line):
   # last line of verse. Assume danda is coded as '||'
   verses.append(verse)
   verse = []
 if len(verses) != len(versenums):
  print(info,' numverse = %s, len(verses) = %s' %(len(versenums),len(verses)))
  return False,entry
 # construct list of new 'S' groups, one for each verse
 sgroups = []
 for iverse,verse in enumerate(verses):
  versenum = versenums[iverse]
  group = []
  group.append('<S n="%s">' %versenum)
  for line in verse:
   # enclose in 's' (Sanskrit) tag
   newline = '<s>%s</s>' % line
   group.append(newline)
  if pb != None:
   group.append(pb)
  group.append('</S>')
  sgroups.append(group)
 # construct new groups
 # from sgroups and the other groups from entry
 newgroups = sgroups + entry.groups[1:]
 # construct new lines
 newlines = ['<entry>']
 # revise gtypes attribute info
 gtypes2 = entry.gtypes[1:]  # original list of types,
 gtypes1 = ['S' for i in range(len(verses))]
 newgtypes = gtypes1 + gtypes2
 newgtypestr = ','.join(newgtypes)
 newinfo = re.sub(r'gtypes=".*?"', 'gtypes="%s"' % newgtypestr,info)
 newlines.append(newinfo)
 for group in newgroups:
  for line in group:
   newlines.append(line)
 newlines.append('</entry>')
 try:
  newentry = Entry(newlines)
 except:
  print('bad newlines')
  for i,line in enumerate(newlines):
   print('newlines[%s]: %s' %(i,line))
  exit(1)
 newentries.append(newentry)
 changed = True
 return changed,newentries

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
 
if __name__=="__main__":
 tranin = 'hk'

 filein = sys.argv[1] # boesp_utf8.xml
 fileout = sys.argv[2] # boesp_utf8_revised.xml
 xmlroot = 'boesp'
 lines = read_lines(filein)
    
 entries0 = list(generate_entries(lines))
 print(len(entries0),'entries found')
 entries = []
 nadj = 0
 for entry0 in entries0:
  flag,newentries = S_adjust(entry0)
  if flag:
   nadj = nadj + 1
  for entry in newentries:
   entries.append(entry)
 print(nadj,"entries adjusted for S")
 write_entries(entries,xmlroot,fileout)

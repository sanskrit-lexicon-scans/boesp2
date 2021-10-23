# coding=utf-8
""" as_1.py 
 Each entry is a sequence of 'groups'.
 And each group has an 'identfier'
 Generate frequency list of AS 'phrases'
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys, re,codecs

class Entry(object):
 def __init__(self,grouplist,page,grouplines):
  self.groups = grouplist
  self.page = page  # page reference (1.n) where <S> starts
  #self.entrylines = entrylines(grouplist)
  # compute tags and Ls (some groups have more than 1 <Dx>
  self.Ls = []  # all D-values for the entry, aggregated over groups
  self.tags = [] # for each group, the tag for the group (D, F, , etc.)
  self.tagnums = [] # for each group, the numbers for the group (a list)
  self.grouplines = grouplines
  for group in self.groups:
   # group is a sequence of lines from boesp
   firstline = group[0]
   tag,nums = Entry.get_groupinfo(firstline)
   if tag == 'D':
    self.Ls = self.Ls + nums
   self.tags.append(tag)
   self.tagnums.append(nums)
 # class data
 group_regex = {
  'D' : r'<(D)([0-9]+)>',
  'F' : r'<(F)>([0-9.]+)\)',
  'S' : r'<(S)()>',  # no number
  'H' : r'<(HS|H)()>', # no number
  'V' : r'<(V[123])>([0-9]+)[.] '
 }
 @staticmethod
 def get_groupinfo(line):
  assert line.startswith('<')
  gtype = line[1]  # character after initial '<'
  # now logic depends on gtype
  nums = []
  tag = None
  regex = Entry.group_regex[gtype]
  for m in re.finditer(regex,line):
   tag0 = m.group(1)
   num = m.group(2)
   if tag == None:
    tag = tag0
   assert tag == tag0  # check only 1 kind of tag in this group
   nums.append(num)
  ans = (tag,nums)
  return ans
 
def generate_groups(lines):
 iline = 0 # start at first line
 nlines = len(lines)
 # ignore blank lines
 while iline < nlines:
  while (lines[iline].strip() == ''):
   iline = iline + 1
   if iline == nlines:
    return []  # yield [] gives error
  # gather block of non-blank lines
  group = []
  iline_group = iline
  while (lines[iline].strip() != ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    break
  yield group,iline_group

def entrysummary(entry):
 gtypes = ','.join(entry.tags)
 page = entry.page # page on which entry starts
 Ls = entry.Ls
 if len(Ls) == 0:
  L = '?'
 else:
  L = ','.join(Ls)
 text = 'L=%s: %s %s' %(L,gtypes,page)
 return text

 
def updatepage(entry,page):
 for group in entry:
  for line in group:
   m = re.search(r'\[Seite([0-9][.][0-9]+)\]',line)
   if m:
    newpage = m.group(1)
    return newpage
 return page # no change

def has_D(entry):
 for group in entry:
  if group[0].startswith('<D'):
   return True
 # no D-group in entry yet
 return False

def generate_entries(lines):
 ngroup = 0
 #nentry = 0
 firstfound = False
 page = '1.1'
 for group,iline_group in generate_groups(lines):
  ngroup = ngroup+1
  # skip the groups until a condition is met
  if firstfound:
   # 10-17-2021. Added HS
   # 10-19-2021. Added 'H'  (3 instances)
   if group[0].startswith(('<S>','<HS>','<H>')):  
    if (entry != []):
     if has_D(entry):
      # we're starting a new entry.
      # First, finish the prior entry
      e = Entry(entry,page,entrylines)
      page = updatepage(entry,page)  # for next entry
      yield e
      entry = [group] # start a new group
      entrylines = [iline_group]
     else:
      # an S or HS appended to entry without a D-group yet
      entry.append(group)
      entrylines.append(iline_group)
   else:
    entry.append(group)
    entrylines.append(iline_group)
  elif group[0].startswith('<H> Boehtlingk'):
   firstfound = True
   entry = []
   entrylines = []
 yield Entry(entry,page,entrylines)

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def read_words(filein):
 lines = read_lines(filein)
 words = []
 for line in lines:
  word,count,info = line.split(' : ')
  words.append(word)
 return words

def get_instances(word,entries):
 if word.endswith('.'):
  temp = word.replace('.','[.]')
  regexraw = r'\b%s' %temp
 else:
  temp = word + '[^A-Z0-9.]'
  regexraw = r'\b%s' %temp
 regex = re.compile(regexraw)
 ans = []
 for entry in entries:
  for igroup,group in enumerate(entry.groups):
   tag = entry.tags[igroup]
   if tag not in ['F','V1','V2','V3']:
    continue
   tagnum = entry.tagnums[igroup]
   iline0 = entry.grouplines[igroup] # 
   for iline,line in enumerate(group):
    m = re.search(regex,line)
    if m != None:
     lnum = iline0 + iline + 1
     ans.append((lnum,line,tag,tagnum))
 return ans

def write(outrecs,fileout):
 with codecs.open(fileout,"w","utf-8") as f:
  outarr = []
  for word,wordlines in outrecs:
   outarr.append('; --------------------------------------------')
   outarr.append('; %s (%s)' %(word,len(wordlines)))
   for lnum,line,tag,tagnum in wordlines:
    #tagnum is a list
    tagnumstr = ','.join(tagnum)
    outarr.append('; %s %s' %(tag,tagnumstr))
    outarr.append('%s old %s' %(lnum,line))
    outarr.append('%s new %s' %(lnum,line))
    outarr.append(';')
  for out in outarr:
   f.write(out+'\n')
 print(len(outrecs),'words processed in',fileout)
 
if __name__=="__main__":
 #test()
 filein = sys.argv[1] # boesp_utf8.txt
 filein1 = sys.argv[2] # notpwg.txt format 3 fields word : count : type
 fileout = sys.argv[3] # boesp.xml
 lines = read_lines(filein)
 words = read_words(filein1)
 #words = words[0:5]  # debug
 entries = list(generate_entries(lines))
 outrecs = []
 for word in words:
  wordlines = get_instances(word,entries)
  outrecs.append((word,wordlines))

 write(outrecs,fileout)

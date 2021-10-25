# coding=utf-8
""" as_4.py 
 Each entry is a sequence of 'groups'.
 And each group has an 'identfier'
 Generate frequency list of AS 'phrases'
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys, re,codecs

class Entry(object):
 def __init__(self,grouplist,page):
  self.groups = grouplist
  self.page = page  # page reference (1.n) where <S> starts
  #self.entrylines = entrylines(grouplist)
  # compute tags and Ls (some groups have more than 1 <Dx>
  self.Ls = []  # all D-values for the entry, aggregated over groups
  self.tags = [] # for each group, the tag for the group (D, F, , etc.)
  self.tagnums = [] # for each group, the numbers for the group (a list) 
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
  while (lines[iline].strip() != ''):
   group.append(lines[iline])
   iline = iline + 1
   if iline == nlines:
    break
  yield group

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
 for group in generate_groups(lines):
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
      e = Entry(entry,page)
      page = updatepage(entry,page)  # for next entry
      yield e
      entry = [group] # start a new group
     else:
      # an S or HS appended to entry without a D-group yet
      entry.append(group)
   else:
    entry.append(group)
  elif group[0].startswith('<H> Boehtlingk'):
   firstfound = True
   entry = []
 yield Entry(entry,page)

def read_and_clean_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  nprob = 0
  lines = []
  for line in f:
   line = line.rstrip('\r\n')
   # cleaning <>
   if '<>' in line:
    nprob = nprob + 1
    line = line.replace('<>','')
   # one version had each (non-blank) line end in middle dot,
   #  and often followed by space.
   # Remove these in xml
   line = re.sub(r'· *$','',line)
   lines.append(line)
 print(len(lines),"lines read from",filein)
 print("remove %s instances of '<>'"% nprob)
 return lines


def write_asfreq(fileout,asfreq):
 keys = asfreq.keys()
 keys = sorted(keys)
 outarr = []
 ntot = 0
 for key in keys:
  n = asfreq[key]
  outarr.append('%s : %s' %(key,n))
  ntot = ntot + n
  
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(keys),"records written to",fileout)
 print(ntot,"words including frequency")

def is_asword(w):
 #
 if w.startswith(('Page','Seite')):
  return False
 if re.search(r'^[AD][0-9]+$',w):  #<D1234> <A3432>
  return False
 m = re.search(r'^[A-Z][A-Z0-9]*$',w)
 return (m != None)

def update_asfreq(entry,asfreq):
 for igroup,group in enumerate(entry.groups):
  tag = entry.tags[igroup]
  if tag in ['H','S']:
   continue  # no AS here
  text = '\n'.join(group) # group is a sequence of lines
  # exclude Sanskrit text {#...#}
  text1 = re.sub(r'{#.*?#}',' ',text,re.DOTALL)
  # exclude tags
  text1 = re.sub(r'<V1>|<V2>|<V3>|<F>|<S>|<H>|<HS>',' ',text1)
  # exclude known roman numerals
  #text1 = re.sub(r'I|II|III|IV|IX|VI|XI|XIV|XVI|XVIII',' ',text1)
  #words = re.split(r'[ \n·]+',text1)
  words = re.split(r'\b',text1)
  asflag = [is_asword(w) for w in words]
  asphrases = []
  phrase = []
  for iword,word in enumerate(words):
   if asflag[iword]:
    phrase.append(word)
   elif phrase != []:
    phrasetext = ' '.join(phrase)
    if phrasetext not in asfreq:
     asfreq[phrasetext] = 0
    asfreq[phrasetext] = asfreq[phrasetext] + 1
    phrase = []
   else:
    # phrase alreaady empty
    pass
  # last phrase, if any
  if phrase != []:
   phrasetext = ' '.join(phrase)
   if phrasetext not in asfreq:
    asfreq[phrasetext] = 0
   asfreq[phrasetext] = asfreq[phrasetext] + 1

if __name__=="__main__":
 #test()
 filein = sys.argv[1] # boesp_utf8.txt
 fileout = sys.argv[2] # boesp.xml
 lines = read_and_clean_lines(filein)
    
 entries = list(generate_entries(lines))
 #test(entries,fileout)  # prints entry group info.
 asfreq = {}
 for entry in entries:
  update_asfreq(entry,asfreq)

 write_asfreq(fileout,asfreq)
 
 #entries_HS_adjust(entries)
 #body = xml_body(entries,tranin)
 #tail = ['</%s>'%xmlroot]
 #linesout = head + body  + tail
 
 #with codecs.open(fileout,"w","utf-8") as f:
 # for line in linesout:
 #  f.write(line+'\n')
 #statistics(entries)
 

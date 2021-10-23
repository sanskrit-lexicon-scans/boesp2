# coding=utf-8
""" change_j_n5.py
 change transaction generation
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys, re,codecs

class Entry(object):
 def __init__(self,grouplist,page,grouplines):
  self.groups = grouplist
  self.page = page  # page reference (1.n) where <S> starts
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
 """ parse lines X = Y and return list of (X,Y)
 """
 lines = read_lines(filein)
 words = []
 for iline,line in enumerate(lines):
  try: 
   word = line.split(' = ')
   if len(word) == 1:
    continue
   if word in words:
    print(iline+1,'duplicate',word)
   else:
    words.append(word)
  except:
   pass
 # sort by decreasing length of old
 words = sorted(words,key = lambda x : len(x[0]),reverse=True)
 return words

def get_instances(word,entries):
 old,new = word
 ans = []
 for entry in entries:
  for igroup,group in enumerate(entry.groups):
   tag = entry.tags[igroup]
   if tag not in ['F','V1','V2','V3']:
    continue
   tagnum = entry.tagnums[igroup]
   iline0 = entry.grouplines[igroup] # 
   for iline,line in enumerate(group):
    newline = line.replace(old,new)
    if newline != line:
     lnum = iline0 + iline + 1
     ans.append((lnum,line,tag,tagnum,newline))
 return ans

def get_entry_instances(words,entry):
 #old,new = word
 ans = []
 
 for igroup,group in enumerate(entry.groups):
   tag = entry.tags[igroup]
   if tag not in ['F','V1','V2','V3']:
    continue
   tagnum = entry.tagnums[igroup]
   iline0 = entry.grouplines[igroup] # 
   for iline,line in enumerate(group):
    newline = line
    for word in words:
     old,new = word
     newline1 = newline.replace(old,new)
     if newline1 != newline:
      lnum = iline0 + iline + 1
      ans.append((word,lnum,newline,tag,tagnum,newline1))
      if lnum == 102893:
       print(lnum,newline)
      newline = newline1
 return ans

def write_unused(outrecs,fileout,words):
 a = []
 words = sorted(words,key = lambda x: x[0])
 for iword,word in enumerate(words):
  recs = []
  for iout,outarr in enumerate(outrecs):
   for x in outarr:
    if x[0] == word:
     recs.append(x)
  a.append((word,recs))
 with codecs.open(fileout,"w","utf-8") as f:
  outarr = []
  for word,wordlines in a:
   outarr.append('; --------------------------------------------')
   outarr.append('; %s (%s)' %(word,len(wordlines)))
   for word1,lnum,line,tag,tagnum,newline in wordlines:
    #tagnum is a list
    tagnumstr = ','.join(tagnum)
    outarr.append('; %s %s' %(tag,tagnumstr))
    outarr.append('%s old %s' %(lnum,line))
    outarr.append('%s new %s' %(lnum,newline))
    outarr.append(';')
  for out in outarr:
   f.write(out+'\n')
 print(len(outrecs),'words processed in',fileout)

def write(outrecs,fileout,words):
 outarr = []
 for wordlines in outrecs:
  for word,lnum,line,tag,tagnum,newline in wordlines:
   #tagnum is a list
   tagnumstr = ','.join(tagnum)
   outarr.append('; %s %s' %(tag,tagnumstr))
   outarr.append('%s old %s' %(lnum,line))
   outarr.append('%s new %s' %(lnum,newline))
   outarr.append(';')
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outrecs),'words processed in',fileout)
 
if __name__=="__main__":
 #test()
 filein = sys.argv[1] # boesp_nn.txt
 filein1 = sys.argv[2] # as_j_n5_words.txt
 fileout = sys.argv[3] # change_kk.txt
 lines = read_lines(filein)
 words = read_words(filein1)
 #words = words[0:5]  # debug
 #print('dbg: words=',words)
 entries = list(generate_entries(lines))
 outrecs = []
 for entry in entries:
  wordlines = get_entry_instances(words,entry)
  if len(wordlines)!= 0:
   outrecs.append(wordlines)
 #for word in words:
 # wordlines = get_instances(word,entries)
 # outrecs.append((word,wordlines))

 write(outrecs,fileout,words)

# coding=utf-8
"""step4b/extractwords
 
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

def write_words(d,fileout):
 words = sorted(d.keys())
 with codecs.open(fileout,"w","utf-8") as f:
  tot = 0
  for word in words:
   c = d[word]
   tot = tot + c
   line = '%s : %s' % (word,c)
   f.write(line+'\n')
 print(len(words),"distinct words written to",fileout)
 print(tot,'Total number of instances of the words')

def entry_words_cap(entry,d,wordregex):
 """ cap: full words composed of capital letters and digits
          with initial capital letter.
        exclude <s>
 """
 for i,gtype in enumerate(entry.gtypes):
  if gtype == 'S':
   continue
  dbg = False
  #dbg = (entry.L == '4156') and (gtype == 'F')
  if dbg: print(entry.info)
  # skip first/last lines 
  group = entry.groups[i] # list of lines
  text = '\n'.join(group[1:-1])  # skip first/last lines e.g. <F..> and </F>
  #text = ' '.join(group[1:-1])  # skip first/last lines e.g. <F..> and </F>
  parts = re.split('(<s>.*?</s>)',text,flags=re.DOTALL)
  for part in parts:
   if part.startswith('<s>'):
    continue
   #words = re.split(r'\b',part,flags=re.DOTALL)  #1
   # [\b\W\b]+  Ref: https://pynative.com/python-regex-split/
   # this is better, but not quite right
   words = re.split(r'[\b\W\b]+',part,flags=re.DOTALL) #2
   #words = re.split(r'[^A-Za-z0-9]',part,flags=re.DOTALL) #3
   #1 and #2 give same results with sub-condition below
   # however, #1 gives many more 'blank strings'.
   # Surprisingly, #3 gives different results. Not sure why.
   if dbg: print(' words=',words)
   for word in words:
    if word in ['h3','h4','pb1']:
     # these are tag names. skip them
     continue
    if re.search(wordregex,word):
     if word not in d:
      d[word] = 0
     d[word] = d[word] + 1
  if False:  # for debugging
   print('text lines:')
   for line in group:
    print(line)
   print('parts')
   for part in parts:
    print(' part = ',part)
   
    
def entry_words(entry,d,option):
 if option == 'capnum':
  #regexword = re.compile(r'^[A-Z][A-Z0-9]*$')
  regexword = re.compile(r'[A-Z][0-9]')
  entry_words_cap(entry,d,regexword)
 elif option == 'lonum':
  regexword = re.compile(r'[a-z][0-9]')
  entry_words_cap(entry,d,regexword)
 elif option == 'letternum':
  regexword = re.compile(r'[A-Za-z][0-9]')
  entry_words_cap(entry,d,regexword)
  
 else:
  print('entry_words. unknown option',option)
  exit(1)

def write_letternums(d,fileout):
 words = d.keys()
 dl = {}
 for word in words:
  a = re.findall(r'[A-Za-z][0-9]+',word)
  for x in a:
   if x not in dl:
    dl[x] = 0
   dl[x] = dl[x] + 1
 lns = sorted(dl.keys())
 with codecs.open(fileout,"w","utf-8") as f:
  tot = 0
  for ln in lns:
   c = dl[ln]
   tot = tot + c
   line = '%s : %s' % (ln,c)
   f.write(line+'\n')
 print(len(lns),"distinct lns written to",fileout)
 print(tot,'Total number of instances of the lns')

if __name__=="__main__":
 option = sys.argv[1]  # which kind of words selected
 filein = sys.argv[2] # boesp.xml
 fileout = sys.argv[3] # word frequency
 fileout1 = sys.argv[4] # letternum instances
 xmlroot = 'boesp'
 version = "1.3"  # this must agree with step0/boesp.dtd
 entries = read_entries(filein)
 d = {}  # frequency count dictionary
 for entry in entries:
  entry_words(entry,d,option)
 write_words(d,fileout)
 write_letternums(d,fileout1)
 

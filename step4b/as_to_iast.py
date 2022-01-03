# coding=utf-8
"""step4b/as_iast.py
 
"""
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step3e')
# the Entry object
from transcode import xml_header,read_entries
import transcoder
transcoder.transcoder_set_dir('./')

def ln_iast(x0):
 x = x0.replace('M3','M2')
 x = x.replace('m3','m2')
 y = transcoder.transcoder_processString(x,'as','roman') # as_roman.xml
 if False:
  print('%s -> %s' %(x0,y))
  exit(1)
 return y

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

def entry_words_cap(entry,d,wordregex):
 """ cap: full words composed of capital letters and digits
          with initial capital letter.
        exclude <s>
 """
 for i,gtype in enumerate(entry.gtypes):
  if gtype == 'S':
   continue
  # skip first/last lines 
  group = entry.groups[i] # list of lines
  text = '\n'.join(group[1:-1])  # skip first/last lines e.g. <F..> and </F>
  parts = re.split('(<s>.*?</s>)',text,flags=re.DOTALL)
  newparts = []
  for part in parts:
   if part.startswith('<s>'):
    newparts.append(part)
    continue
   words = re.split(r'([\b\W\b]+)',part,flags=re.DOTALL) #2
   newwords = []
   for word in words:
    if word in ['h3','h4','pb1']:
     # these are tag names. skip them
     newword = word
    elif re.search(wordregex,word):
     newword = ln_iast(word)
     if word not in d:
      d[word] = 0
     d[word] = d[word] + 1
    else:
     newword = word
    newwords.append(newword)
   newpart = ''.join(newwords)
   newparts.append(newpart)
  newtext = ''.join(newparts)
  newlines = newtext.split('\n')
  newgroup = []
  newgroup.append(group[0])
  for newline in newlines:
   newgroup.append(newline)
  newgroup.append(group[-1])
  entry.groups[i] = newgroup
    
def entry_words(entry,d,option=None):
 regexword = re.compile(r'[A-Za-z][0-9]')
 entry_words_cap(entry,d,regexword)

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
  newgroups = groups
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

def check(d):
 fileout = "temp_as_to_iast_words_letternum.txt"
 from extractwords import write_words
 write_words(d,fileout)
 
if __name__=="__main__":
 filein = sys.argv[1] # boesp.xml
 fileout = sys.argv[2] # word frequency
 xmlroot = 'boesp'
 version = "1.3"  # this must agree with step0/boesp.dtd
 entries = read_entries(filein)
 d = {}  # frequency count dictionary
 newentries = []
 for entry in entries:
  entry_words(entry,d,option=None)
  newentry = entry
  newentries.append(newentry)
 write_entries(newentries,xmlroot,version,fileout)
 check(d)
 

# coding=utf-8
""" extractsan1.py
 
"""
from __future__ import print_function
import sys, re,codecs
# use checkgroup.py to read input and interpret as list of entries.
sys.path.append('../step2/check')
from checkgroup import generate_entries
def out_info(e):
 info = e.attrib['n']
 # 'L=11: S,D,F 1.2'
 m = re.search(r'=(.*?):',info)
 L = m.group(1)
 m = re.search(r' ([1-3][.][0-9]+)$',info)
 page = m.group(1)
 outarr = []
 outarr.append('; %s : page %s' %(L,page))
 return outarr

def adjust_underscore(x):
 if '_' not in x:
  return x
 y = x.replace('_</s>','</s>.')
 if '_' in y:
  print('WARNING: found _',x)
 return y

def out_S(e):
 outarr = []
 text = e.text
 textlines = text.split('\n')
 for line in textlines:
  if line.strip() != '':
   line = adjust_underscore(line)
   if '@' not in line:
    outarr.append(line)
    continue
   # special handling for lines with @
   lines1 = re.split(r' @ ',line)
   if len(lines1) != 2:
    print('ERROR @:',lines1)
    exit(1)
   assert lines1[0].startswith('    ')
   outarr.append(lines1[0])
   outarr.append('      '+lines1[1])  # insert 6 spaces
 return outarr

def out_HS(e):
 outarr = []
 text =  ET.tostring(e,encoding="unicode")
 textlines = text.split('\n')
 for line in textlines:
  line1 = line.strip()
  if line1 == '':
   continue
  elif line1 in ['<HS>','</HS>']:
   continue
  else:
   line1 = adjust_underscore(line1)
   lineout = '+   %s'%line1
  outarr.append(lineout)
 return outarr

 
def entries_in_volume(entries,volume):
 volume_Lrange = {
  1: (1,2219),
  2: (2220,4649),
  3: (4650,7613),
  4: (7614,7865)
 }
 ans = []
 for entry in entries:
  L = int(entry.Ls[0])
  L1,L2 = volume_Lrange[volume]
  if (L1<=L<=L2):
   ans.append(entry)
 print(len(ans),'entries from volume',volume)
 return ans

dandas = ('|','.','।','॥')
def get_outrec(entry):
 Lseq = ','.join(entry.Ls)
 page = entry.page
 mds = '· ' # end of lines
 outarr = []
 outarr.append('; ---------------------------------------------')
 outarr.append('; %s : page %s' %(Lseq,page))
 
 for igroup,group in enumerate(entry.groups):
  tag = entry.tags[igroup]
  if tag == 'HS':
   assert len(group) == 1
   for line in group:
    x = line.replace('<HS>','')
    x = x.lstrip()
    x = x.replace('{#','<s>')
    x = x.replace('#}','</s>')
    assert x.endswith(mds)
    x = x[0:-2]  # 2 = len(mds)
    x = x.rstrip()
    out = '+   ' + x
    outarr.append(out)
  elif tag == 'S':
   # two kinds of indentation. Detect which kind based on
   # whether first line ends with danda
   x = group[0]
   x = x[0:-2].strip()
   if x.endswith(dandas):
    indents = ('    ','    ') # same for all lines
   else:
    indents = ('    ','      ') # 2nd lines more indent
   for iline,line in enumerate(group):
    x = line.replace('<S>','')
    assert x.endswith(mds)
    x = x[0:-2]  # 2 = len(mds)
    x = x.strip()
    indent = indents[iline % 2]
    out = indent + x
    outarr.append(out)
  else:
   pass
 return outarr

def write(fileout,outrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"records written to",fileout)
 
if __name__=="__main__":
 volume = int(sys.argv[1])
 assert volume in [1,2,3,4]
 filein = sys.argv[2] # boesp
 fileout = sys.argv[3] # 
 with codecs.open(filein,"r","utf-8") as f:
  lines = [line.rstrip('\r\n') for line in f]
 entries = list(generate_entries(lines))
 print(len(entries),"entries read from",filein)
 ventries = entries_in_volume(entries,volume)
 outrecs = [get_outrec(entry) for entry in ventries]
 write(fileout,outrecs)
 

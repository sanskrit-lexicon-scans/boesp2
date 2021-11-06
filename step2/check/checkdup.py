# coding=utf-8
""" checkdup.py 
 Each entry is a sequence of 'groups'.
 And each group has an 'identfier'
"""
from __future__ import print_function
import xml.etree.ElementTree as ET
import sys, re,codecs

dandas = {'hk':'|','slp1':'.','deva':'।'}
ddandas = {'hk':'||','slp1':'..','deva':'॥'}
dandaregexes= {'hk':r'([|]+)',  'slp1':r'([.]+)', 'deva': r'([।॥])'}

def get_L_from_D(line):
 """
  Assume line contains one or more <Dn>
  Return list of all n
 """
 a = []
 for m in  re.finditer(r'<D([0-9]+)>',line):
  a.append(m.group(1))
 return a

def get_A_from_D(line):
 """
  Assume line starts with one or more <Dn>
  Return list of all n
 """
 a = []
 for m in  re.finditer(r'<A([0-9]+)>',line):
  a.append(m.group(1))
 return a

def get_D_from_F(line):
 """
  <F>[0-9. ]+)
 """
 a = []
 m = re.search(r'^<F>([0-9. ]+)\)',line)
 if not m:
  return a
 x = m.group(1)
 # remove trailing space or period, if any
 x = re.sub(r'[ .]*$','',x)
 a = re.split(r'[ .]+',x)
 return a

def get_D_from_V(line):
 """
  <V>[0-9]+. 
 """
 a = []
 m = re.search(r'^<V>([0-9]+)[.] ',line)
 if not m:
  return a
 x = m.group(1)
 a = [x]
 return a

class Entry(object):
 def __init__(self,grouplist,page):
  self.groups = grouplist
  self.page = page  # page reference (1.n) where <S> starts
  #self.entrylines = entrylines(grouplist)
  # compute tags and Ls (some groups have more than 1 <Dx>
  Ls = []
  a = []
  for group in self.groups:
   # group is a sequence of lines from boesp
   firstline = group[0]
   m = re.search(r'^<(.*?)>',firstline)
   if not m:
    a.append('X')
   else:
    tag = m.group(1)
    if tag.startswith('D'):
     # there may be multiple <DX><DY> in line Example <D145> 146.
     a.append('D')
     Lvals = get_L_from_D(firstline)
     Ls = Ls + Lvals
    else:
     a.append(tag)
  self.Ls = Ls
  self.tags = a
  
def xml_header(xmlroot):
 # write header lines
 text = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE %s SYSTEM "%s.dtd">
<!-- <H> Boehtlingk, Indische Sprüche, 2. Auflage, St. Petersburg 1870 -->
<%s>
""" % (xmlroot,xmlroot,xmlroot)
 lines = text.splitlines()
 lines = [x.strip() for x in lines if x.strip()!='']
 return lines

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

def make_xml_S(group,entry,tranin):
 # group is a list of lines
 # get danda and doubledanda for this transliteration
 danda = dandas[tranin]
 ddanda = ddandas[tranin]
 dandaregex = dandaregexes[tranin]
 dbg = True
 outarr = []
 text = ' '.join(group)
 # remove page if any.  If it occurs, is it always at the end?
 pb = None
 m = re.search(r' *\[Seite([0-9][.][0-9]+)\] *$',text)
 if m:
  pb = m.group(0)
  text = re.sub(r'\[Seite([0-9][.][0-9]+)\] *$','',text)
 if '[Seite' in text:
  print('make_xml_S WARNING 1 Seite:',entrysummary(entry))   
 text = text.rstrip()
 # 09-01-2021.  Remove gratuitous <br/> tag
 text = text.replace('<br/>',' ')
 # expect ddanda at end
 # A very few have a third line ending in single danda (D=1026, 1027)
 if not text.endswith(ddanda):
  if text.endswith(danda):
   print('make_xml_S WARNING 2a %s:' % 'danda', entrysummary(entry))
  else:
   print('make_xml_S WARNING 2b %s:' % 'ddanda',entrysummary(entry))
  print('text=',text)
  print()
 # generate lines, with each line ending in | or ||
 # remove initial <S>
 text = re.sub(r'^<S> *','',text)
 # note cases with {# or #} in Sanskrit text.
 # These will need to be reformated
 if '#' in text:
  print('# in S: %s' % entrysummary(entry))
 # reformat lines so danda at end
 #parts = re.split(r'([|]+)',text)
 parts = re.split(dandaregex,text)               
 lines = []
 for part in parts:
  if part in (danda,ddanda):
   lines[-1] = lines[-1] + ' ' + part
  else:
   part = part.strip()
   if part != '':
    part = re.sub(r' +',' ',part)  # single-space separation
    lines.append(part)
 # reattach pb text to end, if present
 if pb != None:
  lines[-1] = lines[-1] + pb
 outarr.append(' <S>')
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </S>')
 return outarr

def make_xml_S1(group,entry):
 # group is a list of lines
 # For S, assume boesp-1 has already formatted the lines
 # except for <S> and [Seite] and <br/>
 group1 = []
 for text in group:
  m = re.search(r'\[Seite([0-9][.][0-9]+)\] *$',text)
  if m:
   pb = m.group(0)
   text = re.sub(r'\[Seite([0-9][.][0-9]+)\] *$','',text)
  if '[Seite' in text:
   print('make_xml_S WARNING 1 Seite:',entrysummary(entry))
  text = text.replace('<br/>',' ')
  text = re.sub(r'^<S> *','',text)
  if '#' in text:
   print('# in S: %s' % entrysummary(entry))
  text = text.strip()
  group1.append(text)
 lines = group1
 outarr = []
 outarr.append(' <S>')
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </S>')
 return outarr

def curly_to_s(text):
 text = text.replace('{#','<s>')
 text = text.replace('#}','</s>')
 return text

def make_xml_D(group,entry):
 # group is a list of lines
 outarr = []
 text = ' '.join(group)
 Ls = get_L_from_D(group[0])
 As = get_A_from_D(group[0])
 # remove the D and A tags
 text = re.sub(r'<D.*?>','',text)
 text = re.sub(r'<A.*?>','',text)
 # will have <D n="" a="">
 #if '{#' in text:
 # print('D WARNING {#: %s' %entrysummary(entry))
 # <F> occurs once in D 1475
 text = re.sub(r'<F>','Fussnote ',text) 
 text = text.strip()
 text = curly_to_s(text)
 parts = re.split(r' +',text)
 nc = 0
 lines = []
 words = []
 for part in parts:
  ncp = len(part)
  if (nc + ncp) < 60:
   words.append(part)
   nc = nc + ncp
  else:
   line = ' '.join(words)
   lines.append(line)
   words = [part]
   nc = ncp
 # last line
 if words != []:
  line = ' '.join(words)
  lines.append(line)
 L = ','.join(Ls)
 A = ','.join(As)
 outarr.append(' <D n="%s" a="%s">' % (L,A))
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </D>')
 return outarr

def make_xml_F(group,entry):
 # group is a list of lines
 outarr = []
 text = ' '.join(group)
 
 Ds = get_D_from_F(group[0])
 if Ds == []:
  print('make_xml_F: WARNING: %s' %entrysummary(entry))
  print(text)
  print()
 # remove the F tag
 text = re.sub(r'^<F>([0-9. ]+)\)','',text)
 # will have <D n="<attrib>" >
 text = text.strip()
 text = curly_to_s(text)
 parts = re.split(r' +',text)
 nc = 0
 lines = []
 words = []
 for part in parts:
  ncp = len(part)
  if (nc + ncp) < 60:
   words.append(part)
   nc = nc + ncp
  else:
   line = ' '.join(words)
   lines.append(line)
   words = [part]
   nc = ncp
 # last line
 if words != []:
  line = ' '.join(words)
  lines.append(line)
 attrib = ','.join(Ds)
 outarr.append(' <F n="%s">' % attrib)
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </F>')
 return outarr

def make_xml_V(group,entry):
 # group is a list of lines
 outarr = []
 text = ' '.join(group)
 Ds = get_D_from_V(group[0])
 if Ds == []:
  print('make_xml_V: WARNING: %s' %entrysummary(entry))
 # remove the V tag
 text = re.sub(r'^<V>([0-9]+)[.] ','',text)
 # will have <V n="<attrib>" >
 text = text.strip()
 text = curly_to_s(text)
 parts = re.split(r' +',text)
 nc = 0
 lines = []
 words = []
 for part in parts:
  ncp = len(part)
  if (nc + ncp) < 60:
   words.append(part)
   nc = nc + ncp
  else:
   line = ' '.join(words)
   lines.append(line)
   words = [part]
   nc = ncp
 # last line
 if words != []:
  line = ' '.join(words)
  lines.append(line)
 attrib = ','.join(Ds)  # Ds has just one for V
 outarr.append(' <V n="%s">' % attrib)
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </V>')
 return outarr

def make_xml_HS(group,entry):
 # group is a list of lines
 # Here, the printed text is always (I think) in one line.
 # And we construct this similarly.
 # We also do NOT adjust the line lengths
 outarr = []
 text = ' '.join(group)
 # remove the HS tag
 text = re.sub(r'^<HS>','',text)
 text = text.strip()
 text = curly_to_s(text)
 text = re.sub(r'  +',' ',text) # remove extra spaces
 lines = [text]
 outarr.append(' <HS>')
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </HS>')
 return outarr

def make_xml_H(group,entry):
 # group is a list of lines
 outarr = []
 text = ' '.join(group)
 # remove the H tag
 text = re.sub(r'^<H>','',text)
 text = text.strip()
 parts = re.split(r' +',text)
 nc = 0
 lines = []
 words = []
 for part in parts:
  ncp = len(part)
  if (nc + ncp) < 60:
   words.append(part)
   nc = nc + ncp
  else:
   line = ' '.join(words)
   lines.append(line)
   words = [part]
   nc = ncp
 # last line
 if words != []:
  line = ' '.join(words)
  lines.append(line)
 outarr.append(' <H>')
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </H>')
 return outarr

def make_xml_HS2(group,entry):
 # group is a list of lines. Only 1 instance
 outarr = []
 text = ' '.join(group)
 # remove the HS2 tag
 text = re.sub(r'^<HS2>','',text)
 text = text.strip()
 text = curly_to_s(text)
 parts = re.split(r' +',text)
 nc = 0
 lines = []
 words = []
 for part in parts:
  ncp = len(part)
  if (nc + ncp) < 60:
   words.append(part)
   nc = nc + ncp
  else:
   line = ' '.join(words)
   lines.append(line)
   words = [part]
   nc = ncp
 # last line
 if words != []:
  line = ' '.join(words)
  lines.append(line)
 outarr.append(' <HS2>')
 for line in lines:
  outarr.append('    '+line)
 outarr.append(' </HS2>')
 return outarr

def make_xml_unknown(group,entry):
 # group is a list of lines. Only 1 instance
 # The tag is unknown
 # print with X 
 outarr = []
 outarr.append('<X>')
 for line in group:
  outarr.append(line)
 outarr.append('</X>')
 return outarr

def test_S_prep(a):
 # a is array of strings
 b = []
 for x in a:
  x = x.strip()
  x = re.sub(r'  +',' ',x)
  b.append(x)
 return b

def test_S(outgroup,outgroup1,entry):
 #compare to ways to compute the lines for <S>
 # use difflib 
 lines = test_S_prep(outgroup)
 lines1 = test_S_prep(outgroup1)
 import difflib
 d = difflib.Differ()
 diff = d.compare(lines,lines1)
 print('\n' .join(diff))
 exit(1)
def entrylines(entry,tranin):
 outarr = []
 outarr.append('<entry>')
 text = entrysummary(entry)
 outarr.append(' <info n="%s"/>' %text)
 for igroup,group in enumerate(entry.groups):
  tag = entry.tags[igroup]
  if tag == 'S':
   outgroup = make_xml_S(group,entry,tranin)
   #outgroup = make_xml_S1(group,entry)
   #outgroup1 = make_xml_S1(group,entry)
   #test_S(outgroup,outgroup1,entry)
  elif tag == 'D':
   outgroup = make_xml_D(group,entry)
  elif tag == 'F':
   outgroup = make_xml_F(group,entry)
  elif tag == 'V':
   outgroup = make_xml_V(group,entry)
  elif tag == 'HS':
   outgroup = make_xml_HS(group,entry)
  elif tag == 'HS2':
   outgroup = make_xml_HS2(group,entry)
  elif tag == 'H':
   outgroup = make_xml_H(group,entry)
  else:
   #print('unknown tag:',tag)
   outgroup = make_xml_unknown(group,entry)
  for x in outgroup:
   outarr.append(x)
 outarr.append('</entry>')
 return outarr
 
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
   if group[0].startswith(('<S>','<HS>')):  # 10-17-2021. Added HS
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

def check_L(entries):
 # check sequencing of L-valuese of entries.  Print aberrations
 Lprev = None
 nprob = 0
 for ientry,entry in enumerate(entries):
  Ls = entry.Ls
  #print('Ls=',Ls)
  if Ls == []:
   print('ERROR: No L. previous = ',Lprev)
   continue
  L = int(Ls[0])
  if ientry == 0:
   Lprev = L
  elif L != (Lprev + 1):
   print('Sequencing problem at entry %s: %s should be %s'%(ientry+1,L,Lprev+1))
   # sequence comes from <DN>, in first line of second group of entry
   dgroup = entry.groups[1]
   old = dgroup[0]
   dold = '<D%s>' % L
   Lnew = Lprev+1
   dnew = '<D%s>' % Lnew
   new = old.replace(dold,dnew)
   print(old)
   print(new)
   print()
   Lprev = int(Ls[-1])
   nprob = nprob + 1
   if nprob == 5:
    print('quitting after 5 problems')
    return
  else:
   Lprev = int(Ls[-1])

def check_tagsequence(entries):
 d = {}
 for entry in entries:
  tagseq = ','.join(entry.tags)
  if tagseq not in d:
   d[tagseq] = 0
  d[tagseq] = d[tagseq] + 1
 keys = d.keys()
 for tagseq in keys:
  print('%04d %s' %(d[tagseq],tagseq))

def check_tagfreq(entries):
 d = {}
 for entry in entries:
  for tag in entry.tags:
   if tag not in d:
    d[tag] = 0
   d[tag] = d[tag] + 1
 keys = d.keys()
 for tag in keys:
  print('%04d %s' %(d[tag],tag))

def check_page(entries):
 nprob = 0
 for ientry,entry in enumerate(entries):
  page = entry.page
  v,p = page.split('.')
  if ientry == 0:
   p0 = p
  elif p0 == p:
   pass
  elif int(p) == (int(p0)+1):
   p0 = p
  else:
   text = entrysummary(entry)
   print('page problem: ',text,' p0=%s, p=%s'% (p0,p))
   nprob = nprob + 1
 print('check_page found %s problems' %nprob)

def check_san(entries):
 nprob = 0
 for ientry,entry in enumerate(entries):
  for group in entry.groups:
   text = ' '.join(group)
   n1 = len(re.findall('{#',text))
   n2 = len(re.findall('#}',text))
   if n1 != n2:
    text1 = entrysummary(entry)
    print('unbalanced {#..#} ',text1)
    for line in group:
     print(line)
    print()
    nprob = nprob + 1
 print('check_san found %s problems' %nprob)

def statistics(entries):
 check_san(entries)
 exit(1)
 check_L(entries)
 # check_tagsequence(entries)
 check_tagfreq(entries)
 check_page(entries)
 #check_san(entries)

def entries_HS_adjust(entries):
 """ HS entries are known to occur at the END of groups
  However, they seem to belong to the NEXT group.
  This routine makes the blanket change of entries thus indicated.
  That is, if an entry ends with one or more HS items, then we
  remove these and put them at the beginning of the next entry.

 """
 dbg = False
 for ientry,entry in enumerate(entries):
  oldtags = entry.tags
  ntags = len(oldtags)
  hsend = ntags - 1
  if 'HS' != oldtags[hsend]:
   continue
  #oldgroups = entry.groups not used
  while True:
   hsend1 = hsend - 1
   if oldtags[hsend1] == 'HS':
    hsend = hsend1
   else:
    break
  #  So when hsend <= idx < ntags, tags[idx] = HS
  idxkeep = [i for i in range(len(entry.groups)) if i < hsend]
  idxdrop = [i for i in range(len(entry.groups)) if hsend <= i]
  groups = [entry.groups[i] for i in idxkeep]
  tags = [entry.tags[i] for i in idxkeep]
  #
  groups1 = [entry.groups[i] for i in idxdrop]
  tags1 = [entry.tags[i] for i in idxdrop]
  # change entry.groups and tags
  entry.groups = groups
  entry.tags = tags
  # now also modify the next entry
  ientry1 = ientry+1
  if ientry1 == len(entries):
   print('entries_HS_adjust anomaly:',entrysummary(entry))
   continue
  entry1 = entries[ientry+1]
  if dbg: print('old1:',ientry1,entrysummary(entry1))
  entry1.groups = groups1 + entry1.groups
  entry1.tags = tags1 + entry1.tags
  # The page number for the entry1 should be that for entry
  entry1.page = entry.page  # only line changed
  entries[ientry1] = entry1
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

def check_option(option):
 allowed = ['D','F']
 if option not in allowed:
  print('ERROR UNKNOWN option:',option)
  print('known values:',','.join(allowed))
  exit(1)

def expand_gtype(line,gtype):
 if gtype == 'D':
  regex = r'<D[0-9]+>'
  alist = re.findall(regex,line)
 elif gtype == 'F':
  regex = r'<F>[0-9.]+\)'
  alist = re.findall(regex,line)
 elif gtype == 'S':
  regex = r'<S>'
  alist = re.findall(regex,line)
 elif gtype == 'H':
  # could be either H (header) or HS
  regex = r'^(<HS>|<H>)'
  alist = re.findall(regex,line)
 #elif gtype == 'HS':
 # regex = r'<HS>'
 # alist = re.findall(regex,line)
 elif gtype == 'V':
  # V1, V2, V3
  regex = '<V[123]>[0-9]+[.] '
  alist = re.findall(regex,line)
 else:
  # unrecognized
  alist = [gtype+'?']
 ans = ','.join(alist)
 if (gtype != 'D') and (len(alist)!=1):
  print('multiple anomaly (%s)'%gtype,line)
 return ans

def parse_gtag(gtag):
 gtype = gtag[1]  # gtype = '<X....'
 if gtype == 'D':
  regex = r'<D([0-9]+)>'
  m = re.search(regex,gtag)
  num = m.group(1)
 elif gtype == 'F':
  regex = r'<F>([0-9.]+)\)'
  m = re.search(regex,gtag)
  num0 = m.group(1)  # could have periods X.Y.Z
  # just return first
  nums = num0.split('.')
  num = nums[0]
 elif gtype == 'S':
  regex = r'<S>'
  num = 0
 elif gtype == 'H':
  # could be either H (header) or HS
  regex = r'^(<HS>|<H>)'
  num = 0
 elif gtype == 'V':
  # V1, V2, V3
  regex = '<(V[123])>([0-9]+)[.] '
  m = re.search(regex,gtag)
  gtype = m.group(1)
  num = m.group(2)
 else:
  # unrecognized
  print('parse_gtag ERROR: gtag=',gtag)
  exit(1)
 return (gtype,num)

def check_gtypes(gtypes):
 gtagnums = [parse_gtag(x) for x in gtypes]
 dtagnums = {y for x,y in gtagnums if x == 'D'} # python set
 ftagnums = {y for x,y in gtagnums if x == 'F'}
 flag = True
 if not ftagnums.issubset(dtagnums):
  print('F problem',gtypes)
  flag = False
 for tag in ['V1','V2','V3']:
  vtagnums = {y for x,y in gtagnums if x == tag}
  if not vtagnums.issubset(dtagnums):
   print(tag,'problem',gtypes)
   flag = False

 return flag

def checkgroups(entries,fileout):
 nprob = 0
 outarr = []
 regexstart = r'^<(.)'
 for entry in entries:
  gtypes = []
  for group in entry.groups:
   line = group[0] # first line
   m = re.search(regexstart,line)
   if m == None:
    #outarr.append('group problem:',line)
    gtype = '?'
   else:
    gtype = m.group(1)
   gtype1 = expand_gtype(line,gtype)
   gtypes.append(gtype1)
  flag = check_gtypes(gtypes)
  x = ','.join(gtypes)
  if flag:
   outarr.append(x)
  else:
   y = '[gtype problem]'
   outarr.append(x + ' ' + y)
   nprob = nprob + 1
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),'groups written to',fileout)

def markdup(entries,fileout):
 # Make a dictionary using firstline of
 n = 0
 d = {}
 for ientry,entry in enumerate(entries):
  groups = entry.groups
  for igroup,group in enumerate(groups):
   if entry.tags[igroup] == 'S':
    n = n + 1
    firstline = group[0]
    if firstline not in d:
     d[firstline] = []
    d[firstline].append(ientry)
 firstlines = [firstline for firstline in d if len(d[firstline]) != 1]
 #for firstline in  firstlines:
 # print(firstline)
 
 ientry_multiple = [entrylist for entrylist in d.values() if len(entrylist)!=1]
 outrecs = []
 for ientries in ientry_multiple:
  outarr = []
  Ls_arr = [','.join(entries[ientry].Ls) for ientry in ientries]
  s = ' ; '.join(Ls_arr)
  outarr.append('; %s' %s)
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print('see output in',fileout)
 print(n,'S groups')
 print(len(ientry_multiple),'verses appearing more than once')
 return outrecs
if __name__=="__main__":
 #test()
 filein = sys.argv[1] # boesp_utf8.txt
 fileout = sys.argv[2] # boesp.xml
 lines = read_and_clean_lines(filein)
    
 #head = xml_header(xmlroot)
 entries = list(generate_entries(lines))
 markdup(entries,fileout)


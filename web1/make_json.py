# coding=utf-8
from __future__ import print_function
import sys, re,codecs
sys.path.append('../step3e')
# the Entry object
from transcode import xml_header,read_entries
import json

unused_section_template =u"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>%s</title>
<link rel="stylesheet" type="text/css" href="boesp.css">
</head>
<body>
%s
<div>
<hr/>
<span style="font-size:smaller">
FOOTER. What to go here?
</span>
<br/>
</div>
<div style="height:900px"></div> <!-- a trick for proper anchor scrolling -->
</body>
</html>
"""
class Section(object):
 def __init__(self,sectionid,verses):
  self.sectionid = sectionid
  self.verses = verses
 def write_json(self,fileout):
  with codecs.open(fileout,"w","utf-8") as f:
   json = self.json()
   f.write(json + '\n')
 def json(self):
  """
  # an array of objects, each with "L" and "html"
   {"L":value, "html":value}, where value is a string
  """
  arr = [] 
  for verse in self.verses:
   Ls = verse.L.split(',')
   htmllines = entry_html(verse) # array of strings
   html = '\n'.join(htmllines) # a string
   for L in Ls:
    d = {}
    d['L'] = L    
    d['html'] = html
    arr.append(d)
  jsonstring = json.dumps(arr)
  return jsonstring
 def write_json1(self,fileout):
  with codecs.open(fileout,"w","utf-8") as f:
   json = self.json1()
   f.write(json + '\n')
 def json1(self):
  """
  # an object: {L:html
   {"L":value, "html":value}, where value is a string
  """
  d = {} 
  for verse in self.verses:
   Ls = verse.L.split(',')
   htmllines = entry_html(verse) # array of strings
   html = '\n'.join(htmllines) # a string
   for L in Ls:
    d[L] = html
  jsonstring = json.dumps(d)
  return jsonstring

 def write(self,fileout):
  with codecs.open(fileout,"w","utf-8") as f:
   html = self.html()
   f.write(html + '\n')
 def html(self):
  sectionnum = self.sectionid
  title = "Indische Sprüche %s" %  sectionnum
  bodylines = []
  bodylines.append('<H2>%s</H2>' %title)
  for verse in self.verses:
   # anchor(s)
   Ls = verse.L.split(',')
   for L in Ls:
    a = "<a id='verse%s'/>" % L
    #a = "<a id='%s'/>" % L  # does not work as not-valid form for id
    bodylines.append(a)
   verselines = entry_html(verse)
   
   for iline,line in enumerate(verselines):
    bodylines.append(line)
  bodystring = '\n'.join(bodylines)
  htmlstring = section_template %(title,bodystring)
  return htmlstring

def span_s(text,devaclass="sdeva"):
 text = text.replace('<s>','<span class="%s">'%devaclass)
 text = text.replace('</s>','</span>')
 return text

def span_g(text):
 text = text.replace('<g>','<span class="greek">')
 text = text.replace('</g>','</span>')
 return text

def span_add(text,devaclass="sdeva"):
 text = span_s(text,devaclass)
 text = span_g(text)
 return text

def HS_html(group):
 ans = [] # array of lines
 text = '\n'.join(group[1:-1])
 text = span_add(text,devaclass="sdeva")
 lines = text.split('\n')
 for line in lines:
  ans.append('%s<br/>' %line)
 return ans

def S_html(group):
 ans = [] # array of lines
 text = '\n'.join(group[1:-1])
 text = span_add(text,devaclass="sdeva")
 lines = text.split('\n')
 for line in lines:
  ans.append('%s<br/>' %line)
 return ans

def D_html(group):
 ans = [] # array of lines
 text = '\n'.join(group[1:-1])
 text = span_add(text,devaclass="sdeva")
 lines = text.split('\n')
 ans.append('<div class="de">')
 for line in lines:
  ans.append('%s<br/>' %line)
 ans.append('</div>')
 return ans

def adjust_sup2(text):
 text = re.sub(r'²(.)',r'<i>\1</i>',text,flags=re.DOTALL)
 return text

def F_html(group):
 ans = [] # array of lines
 text = '\n'.join(group[1:-1])
 text = span_add(text,devaclass="fndeva")
 text = adjust_sup2(text)
 lines = text.split('\n')
 ans.append('<div class="footnote">')
 for line in lines:
  ans.append('%s<br/>' %line)
 ans.append('</div>')
 return ans

def V_html(group):
 ans = [] # array of lines
 text = '\n'.join(group[1:-1])
 text = span_add(text,devaclass="vndeva")
 text = adjust_sup2(text)
 lines = text.split('\n')
 ans.append('<div class="vn">')
 for line in lines:
  ans.append('%s<br/>' %line)
 ans.append('</div>')
 return ans

def entry_html(entry):
 bodylines = []
 bodylines.append('<div>')
 L = entry.L
 page = entry.page
 if ',' in L:
  bodylines.append('<h3>Sayings %s, Page %s</h3>' % (L,page))
 else: 
  bodylines.append('<h3>Saying %s, Page %s</h3>' % (L,page))
 
 for igtype,gtype in enumerate(entry.gtypes):
  group = entry.groups[igtype]
  if gtype == 'HS':
   lines = HS_html(group)
  elif gtype == 'S':
   lines = S_html(group)
  elif gtype == 'D':
   lines = D_html(group)
  elif gtype == 'F':
   lines = F_html(group)
  elif gtype in ['V1','V2','V3','V4','V5']:
   lines = V_html(group)
  else:
   # other group types
   print('cannot process group type',gtype)
   continue
  for line in lines:
   bodylines.append(line)
  bodylines.append('<br/>')
 bodylines.append('</div>')
 
 return bodylines

class Verse(object):
 def __init__(self,verseid,verselines):
  self.verseid = verseid
  self.verselines = verselines

def init_verses(lines):
 verses = []
 inverse = False
 for idx,line in enumerate(lines):
  m = re.search(r'^<br /><p class="stamp">rv([0-9]+)[.]([0-9]+)[.]([0-9]+)</p>$',line)
  if idx == 0:
   # first verse
   if not m:
    print("init_verses problem",idx,line)
    exit(1)
   verseid = (m.group(1),m.group(2),m.group(3)) # keep as tuple for later
   verselines = [line]
   inverse = True
   continue
  if m:
   # first line of next verse found
   verse = Verse(verseid,verselines)
   verses.append(verse)
   # Start new verse
   verseid = (m.group(1),m.group(2),m.group(3)) # keep as tuple for later
   verselines = [line]
   inverse = True
   continue
  else:
   # add next line of current verse
   verselines.append(line)
 # install last verse
 verse = Verse(verseid,verselines)
 verses.append(verse)
 return verses

def assign_sectionid(verses):
 sids = []
 sidprev = None
 for entry in entries:
  Ls = entry.L.split(',')
  L = Ls[0]
  L1 = re.sub(r'[.].*$','',L)
  iL1 = int(L1)
  L2 = '%04d' % iL1
  sid = L2[0:2]
  entry.sid = sid
  if sid != sidprev:
   sids.append(sid)
   sidprev = sid
 return sids
def init_sections(verses):
 # verses == entries
 # a section is a collection of entries
 # Our selection based on first L-number of entry.L
 # Drop the fractional value (1234.2 -> 1234)
 # convert to integer
 # convert to xxyy string.  Then value of 'xx' is the section id
 assign_sectionid(verses)
 nsection = 100  # number of verses per section
 
 sections = []
 sectionids = assign_sectionid(verses)
 for sectionid in sectionids:
  es = [verse for verse in verses if verse.sid == sectionid]
  section = Section(sectionid,es)
  sections.append(section)
 return sections

def unused_init_sections(verses):
 # verses == entries
 # a section is a collection of entries
 # Our selection hear is based on page volume
 sections = []
 sectionids = ['1','2','3','4']
 for sectionid in sectionids:
  if sectionid in ['1','2','3']:
   es = [verse for verse in verses if verse.page[0] == sectionid]
  else:
   es = [verse for verse in verses if verse.page[0] not in ['1','2','3']]
  section = Section(sectionid,es)
  sections.append(section)
  if True:
   id1 = es[0].L
   id2 = es[-1].L
   print('section %s has %s entries from %s to %s' %(sectionid,len(es),id1,id2))
 return sections

if __name__ == "__main__":
 filein=sys.argv[1]  # boesp.xml
 dirout = sys.argv[2]
 # read boesp into array of Entry objects
 entries = read_entries(filein)
 sections = init_sections(entries)
 print(len(sections),"sections found")
 # Write each section to a file
 nsection = 0
 for isection,section in enumerate(sections):
  sectionnum = section.sectionid
  fileout = '%s/section%s.json' %(dirout,sectionnum)
  #section.write_json(fileout) #  array
  section.write_json1(fileout) #  object
  nsection = nsection + 1
  #if isection == 1: break
 print(nsection,"section files written to directory",dirout)
 
 

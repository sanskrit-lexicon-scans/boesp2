step4c

Insert greek text.


Refer https://github.com/funderburkjim/boesp-prep/issues/46

Start with a copy of step0/boesp.xml at commit
  c594eb3896f38732551280512d35345b24848f71
git show c594eb3:step0/boesp.xml > temp_boesp.xml

Source of Greek text: greektext folder, various files.


# -------------------------------------------------------------
temp_boesp_01.xml
 <gr>a.</gr> -> <gr>α</gr>.  68
 <gr>a</gr> -> <gr>α</gr>  1
 <gr>b.</gr> -> <gr>β</gr>.  72
 141 changes.
 The 2 remaining require a longer Greek text fragment at Footnote 3202
  page="2.201"

Check validation:
python ../step0/xmlvalidate.py temp_boesp_01.xml ../step0/boesp.dtd
#--------------------------------------------------------
install revised version 01 of boesp

cp temp_boesp_01.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
#--------------------------------------------------------

#--------------------------------------------------------

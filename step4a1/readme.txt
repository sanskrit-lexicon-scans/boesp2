step4a1

Refer https://github.com/funderburkjim/boesp-prep/issues/?.

Start with a copy of step0/boesp.xml at commit
  fa76cebb0fb04c1838d3b8eceaa07636ded2e53b
git show fa76cebb:step0/boesp.xml > temp_boesp.xml

----------------------------------------------------------
#extract HS and S verses from volume 2

python extract_verses.py 2 temp_boesp.xml verses_02.txt

----------------------------------------------------------
# make a devanagari version: verses_02_deva.txt

sh transcode_ab.sh slp1 deva ../../step4a1/verses_02.txt  ../../step4a1/verses_02_deva.txt


# invertibility check
cd ../step1a/sanproof_1_02
sh transcode_ab.sh deva slp1 ../../step4a1/verses_02_deva.txt ../../step4a1/temp.txt
cd ../../step4a1  # may need to do manually
diff verses_02.txt temp.txt
# no diff expected


----------------------------------------------------------
Put copies of these into boesp_prep_sam and boesp_prep_ab repositories

----------------------------------------------------------
# Get corrected versions of the verses
verses_02_rev1_sam.txt, verses_02_deva_rev1_ab.txt

# transcode deva to slp1
verses_02_rev1_ab.txt

# compare the sam and ab revisions.

----------------------------------------------------------
Insert revised verses into text
verses_02_final.txt

Use latest version of step0/boesp.xml, at
 commit ?

temp_boesp_01.xml

py

python update_xml_verses.py temp_boesp_01.xml verses_02_final.txt temp_boesp_02.xml

python update_xml_verses.py temp_boesp_01.xml temp_verses_02.txt temp_boesp_02.xml

Program uses the Entry structure from step3e/transcode.py

## list changes
python ../step0/changes/diff_to_changes.py temp_boesp_01.xml temp_boesp_02.xml changes_sanskrit_vol2.txt


# -------------------------------------------------------------

Check validation:
python ../step0/xmlvalidate.py temp_boesp_02.xml ../step0/boesp.dtd
#--------------------------------------------------------
install revised versions of xml and dtd
cp temp_boesp_02.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh

#--------------------------------------------------------
Correction of page numbers for verses which have an HS element at bottom
of previous page.
Two missing additional HS elements discovered and added.
temp_boesp_02.xml starts as copy of step0/boesp.xml at commit
3aa59f0b619fd549a31178649a866d3cad3fec71  (same as above temp_boesp_02.xml)

temp_boesp_03.xml  manual change from temp_boesp_02.xml.
python ../step0/xmlvalidate.py temp_boesp_03.xml ../step0/boesp.dtd
Install to step0/boesp.xml

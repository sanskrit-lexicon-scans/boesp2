step4a

Refer https://github.com/funderburkjim/boesp-prep/issues/43.

Start with a copy of step0/boesp.xml at commit
  780e8c808a463ba4083907b867580b58dfc2903c
git show 780e8c8:step0/boesp.xml > temp_boesp.xml

Also, start with corrections file of volume 1, as found in
 step1a/sanproof_1_02.
Provisionally,
cp ../step1a/sanproof_1_02/ab_san_1_02.txt temp_verses_1.txt

step1a/sanproof_1_02/diff_verses.txt  shows how to read the temp_verses file.

We must convert the information into this file into a form so that the
HS and S elements may be inserted into the current format of entries for
boesp.xml.

verses_1_rev.txt
  Remove +   Auflösung. and + Räthsel. at 1428 and 1429.
Also, examined step1a/sanproof_1_02/diff_verses1.txt.
  For each of the 76 differences, examined the pdf boesp-1,
  and marked with '+' what looked right to me.
  Then revised verses_1_rev.txt accordingly.
  
python update_prep.py verses_1_rev.txt temp_convert.txt

python update_prep.py verses_1_rev.txt temp_convert_rev.txt

temp_boesp_01.xml : a few manual changes so the update can proceed.
Then a program should do the verse replacements:
python update_xml_verses.py temp_boesp_01.xml temp_convert.txt temp_boesp_02.xml

python update_xml_verses.py temp_boesp_01.xml temp_convert_rev.txt temp_boesp_02.xml

Program uses the Entry structure from step3e/transcode.py

## list changes
python ../step0/changes/diff_to_changes.py temp_boesp_01.xml temp_boesp_02.xml changes_sanskrit_vol1.txt


# -------------------------------------------------------------

Check validation:
python ../step0/xmlvalidate.py temp_boesp_02.xml ../step0/boesp.dtd
#--------------------------------------------------------
install revised versions of xml and dtd
cp temp_boesp_02.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh


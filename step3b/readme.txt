step3b
Remove FDUMMY elements from boesp_utf8.xml.
Refer https://github.com/funderburkjim/boesp-prep/issues/40.

Start with a copy of step0/boesp_utf8.xml at commit
  943d0af41e5326e8e4b65d7994a30e98b5dad446
git show 943d0af:step0/boesp_utf8.xml > temp_boesp_utf8_01.xml
git show 943d0af:step0/boesp.dtd > temp_boesp.dtd

python remove_fdummy.py temp_boesp_utf8_01.xml temp_boesp_utf8_02.xml

# revise temp_boesp.dtd
Remove FDUMMY references
Check validation:
python ../step0/xmlvalidate.py temp_boesp_utf8_02.xml temp_boesp.dtd
#--------------------------------------------------------
install revised versions of xml and dtd
cp temp_boesp_utf8_02.xml ../step0/boesp_utf8.xml
cp temp_boesp.dtd ../step0/boesp.dtd


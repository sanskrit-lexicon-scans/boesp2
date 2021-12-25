step3c
Remove lg and l tags from boesp_utf8.xml.
Refer https://github.com/funderburkjim/boesp-prep/issues/41.

Start with a copy of step0/boesp_utf8.xml at commit
  0946cab3d060ef1f0f5bfece55acca490f00088e
git show 0946cab3:step0/boesp_utf8.xml > temp_boesp_utf8_01.xml
git show 0946cab3:step0/boesp.dtd > temp_boesp.dtd

python remove_lg.py temp_boesp_utf8_01.xml temp_boesp_utf8_02.xml

# revise temp_boesp.dtd
Remove lg and l references
Check validation:
python ../step0/xmlvalidate.py temp_boesp_utf8_02.xml temp_boesp.dtd
#--------------------------------------------------------
install revised versions of xml and dtd
cp temp_boesp_utf8_02.xml ../step0/boesp_utf8.xml
cp temp_boesp.dtd ../step0/boesp.dtd


step3c

Refer https://github.com/funderburkjim/boesp-prep/issues/42.

Start with a copy of step0/boesp_utf8.xml at commit
  4a77f886c21375594deba1753365850eb0fd7412
git show 4a77f88:step0/boesp_utf8.xml > temp_boesp_utf8_00.xml
git show 4a77f88:step0/boesp.dtd > temp_boesp.dtd

Some errors were discovered during the running of improve_s.py.
Corrected version as temp_boesp_utf8_01.xml.
1. L=1831:  Remove (near) duplicate of L=1829 verse
2. 2729,2730  change || to | in the 'speaker' lines
And several other changes. See commit ee7a681.

python improve_s.py temp_boesp_utf8_01.xml temp_boesp_utf8_02.xml

# revise temp_boesp.dtd
Change attribute 'n' to required for <S>
Change each verse line from  X to <s>X</s> 
  The 's' element is also used for Sanskrit text elsewhere, such as in footnotes.
Check validation:
python ../step0/xmlvalidate.py temp_boesp_utf8_02.xml temp_boesp.dtd
#--------------------------------------------------------
install revised versions of xml and dtd
cp temp_boesp_utf8_02.xml ../step0/boesp_utf8.xml
cp temp_boesp.dtd ../step0/boesp.dtd


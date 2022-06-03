step4g

German word corrections.

Refer:
 https://github.com/funderburkjim/boesp-prep/issues/39#issuecomment-1013895539

=================================================
Start with a copy of step0/boesp.xml at commit
  7b65368cc21fc5b0d08231a3d47a1e380a124e20
git show ac358613:step0/boesp.xml > temp_boesp.xml

cp ../step0/boesp.all_ansi.txt temp_ansi_0.txt

=================================================
Start with a file from Thomas (not included), copied locally as
  temp_boesp.all_ansi_corrections_june_1_2022.txt

Discovered that line 105296 is erroneously blank
It should be 'der Glauben hat, zumahl wenn dieser· '
Manually corrected temp_boesp.all_ansi_corrections_june_1_2022.txt

*** NOTIFY THOMAS OF THIS!

=================================================
# temp_ansi_1.txt # version with unix line-endings
python unixify_ansi.py temp_boesp.all_ansi_corrections_june_1_2022.txt temp_ansi_1.txt


diff temp_ansi_0.txt temp_ansi_1.txt | wc -l
# 604
So about 604/4 = 151 lines changed.

=================================================
#convert to utf8
python ../step0/cp1252_utf8.py temp_ansi_0.txt temp_utf8_0.txt
python ../step0/cp1252_utf8.py temp_ansi_1.txt temp_utf8_1.txt


diff temp_utf8_0.txt temp_utf8_1.txt | wc -l
# 604

=================================================
ITALIC MARKUP {%X%}
111 matches in 89 lines for "{%" in buffer: boesp.all_ansi.txt
no matches in boesp.xml

=================================================
create change file
python ../step0/changes/diff_to_changes.py temp_utf8_0.txt temp_utf8_1.txt changes_utf8_1.txt
153 changes written to changes_utf8_1.txt
NOTES:
1) don't change lines that differ only in ending spaces
2) Remove the middle dot at the end of lines
   This is used in the _ansi files, but not in boesp.xml

=================================================
changes_utf8_1_edit.txt 
Various of the items in changes_utf8_1.txt are changed
1) comment out 25 cases which are blank lines,
   but with different number of spaces at end.
2) IAST in AS notation in _ansi, but diacritics in boesp.xml

;-----------------
87 old leben können; darum soll man sich ihr· 
87 new nicht leben können; darum soll man sich ihr· 

=================================================
# Try to apply these utf8 changes to boesp.xml

cp ../step0/boesp.xml temp_boesp_0.xml
python make_change_utf8_xml.py temp_boesp_0.xml changes_utf8_1_edit.txt changes_xml_1.txt
124 read from changes_utf8_1_edit.txt

=================================================
apply the changes
python ../step0/changes/updateByLine.py temp_boesp_0.xml changes_xml_1.txt temp_boesp_1.xml
185728 lines read from temp_boesp_0.xml
185728 records written to temp_boesp_1.xml
124 change transactions from changes_xml_1.txt

#--------------------------------------------------------
Installation

cp temp_ansi_1.txt ../step0/boesp.all_ansi.txt
cp temp_boesp_1.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

********************************************************************

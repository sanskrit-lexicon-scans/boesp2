step4d

Misc. corrections


Refer https://github.com/funderburkjim/boesp-prep/issues/45#issuecomment-1006366284

Start with a copy of step0/boesp.xml at commit
  c30e186b73cc3bc7e2bbfb2bc12f82f3bca13343
git show c30e186:step0/boesp.xml > temp_boesp.xml


# -------------------------------------------------------------
# temp_boesp_deva_AB.txt
This is copy provided by Andhrabharati at comment:
 https://github.com/funderburkjim/boesp-prep/issues/45#issuecomment-1006769350
One detail: it has 1 fewer lines:
 wc -l temp_*
  184321 temp_boesp.xml
  184320 temp_boesp_deva.AB.txt

# -------------------------------------------------------------
temp_boesp_01.xml
The difference is that lines 98824-5 of temp_boesp.xml have been merged
into one line in temp_boesp_deva_AB.txt (along with correction).
This is fine, but causes technical difficulties.  The remedy is to make
the similar merge (of uncorrected lines) in temp_boesp.xml.  The result is
temp_boesp_01.xml.
# -------------------------------------------------------------
temp_boesp.AB.xml
Convert temp_boesp_deva.AB.txt to slp1.
This can be done as in step0/transcode_xml.sh
sh convert_ab.sh :

# -------------------------------------------------------------
change_AB.txt
Since temp_boesp_01.xml and temp_boesp.AB.xml have the same
number of lines, we can generate a file containing the lines changed.
python ../step0/changes/diff_to_changes.py temp_boesp_01.xml temp_boesp.AB.xml change_AB.txt
2889 changes written to change_AB.txt

# -------------------------------------------------------------
temp_boesp_02.xml 
2186 of AB changes lines are due to changing two consecutive spaces to a single space

python ../step0/changes/diff_to_changes.py temp_boesp_02.xml temp_boesp.AB.xml temp_change_02_AB.txt

714 changes

# -------------------------------------------------------------
temp_boesp_03.xml 
AB version removes space(s) at end of lines.
269 lines changed
python ../step0/changes/diff_to_changes.py temp_boesp_03.xml temp_boesp.AB.xml temp_change_03_AB.txt
 445 lines changed

# -------------------------------------------------------------
temp_boesp_04.xml 
1. AB version removes space before right-paren 
 33 lines changed
2. ',</s>' -> '</s>,'
 14 lines changed
3. '</s></footnote>' ->'</s> </footnote>'
 7 lines changed
4. 'Bomb ' -> 'Bomb. '
 6 lines changed
5. 'd.i.' -> 'd. i.'
 3 lines changed
6. 'LA.(' -> 'LA. ('
 15 lines changed
7. ' ;' -> ';'
 20 lines changed
8. ' :' -> ':'
 4 lines changed
9. ';</s>' -> '</s>;'
 8 lines changed
10. '([a-zA-Z])=([a-zA-Z])' -> '\1 = \2'  (regex)
 12 lines changed
11. 'TeluguCharr' -> 'Telugu-Charr'
 13 lines changed
12. 'u.s.w.' -> 'u. s. w.'
 19 lines changed.
13. ':<' -> ': <'
 7 lines changed
14. '=([a-zA-Z])' -> '= \1'  (regex)
 14 lines changed
15. '.=' -> '. ='
 2 lines changed
16. 'v.a.' -> 'v. a.'
 4 lines
 
python ../step0/changes/diff_to_changes.py temp_boesp_04.xml temp_boesp.AB.xml temp_change_04_AB.txt
 287
# -------------------------------------------------------------
change_05.txt   These are the remaining changes made.
 Note: I comment out the 12 '<ls>X</ls>' markups.  
Check validation:
python ../step0/changes/updateByLine.py temp_boesp_04.xml change_05.txt temp_boesp_05.xml

python ../step0/changes/diff_to_changes.py temp_boesp_05.xml temp_boesp.AB.xml change_not_made.txt

In line 50226, greek text. Moved <pb n="1.412"/> outside of <g>X</g>.


python ../step0/xmlvalidate.py temp_boesp_05.xml ../step0/boesp.dtd
install revised version 05 of boesp

cp temp_boesp_05.xml ../step0/boesp.xml
  commit 
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
# -------------------------------------------------------------

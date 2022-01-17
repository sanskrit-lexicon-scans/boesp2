step4f

AB corrections.

Refer:
 https://github.com/funderburkjim/boesp-prep/issues/39#issuecomment-1013895539

Start with a copy of step0/boesp.xml at commit
  ac3586131b38ad26cbe548467fe49e0ba3ab9d3a
git show ac358613:step0/boesp.xml > temp_boesp.xml

# -------------------------------------------------------------
4 AB files from #39 link above, filenames changed from X to temp_Y
  where Y is slight alteration of X

mv 'aufrecht_entries2_deva_updated (1).txt' temp_aufrecht_updated_1_deva.txt
mv last.V4.entries.missed.V5.entry.txt temp_V4_V5_deva.txt
mv missed.V3.entries.in.digitization.txt temp_missed.V3.entries_deva.txt
mv boesp_deva.AB._1b.txt temp_boesp_AB_1b_deva.txt

# -------------------------------------------------------------
slp1 versions of 4 AB files  temp_X_deva.txt -> temp_X_slp1.txt
  <s>X</s> -> <s>Y</s>  where X is devanagari and Y is slp1
sh transcode_ab.sh deva slp1 temp_boesp_AB_1b_deva.txt temp_boesp_AB_1b_slp1.txt
  185334 lines
sh transcode_ab.sh deva slp1 temp_aufrecht_updated_1_deva.txt temp_aufrecht_updated_1_slp1.txt
 227 lines
sh transcode_ab.sh deva slp1  temp_V4_V5_deva.txt temp_V4_V5_slp1.txt
 75 lines
sh transcode_ab.sh deva slp1  temp_aufrecht_updated_1_deva.txt temp_aufrecht_updated_1_slp1.txt
 277 lines

# -------------------------------------------------------------
temp_boesp.xml 185472 lines
temp_boesp_AB_1b_slp1.txt 185334 lines
Why the difference?

temp_boesp_01.xml, temp_boesp_AB_1b_01.txt
 # make copy of prev versions, and then manual changes.
 cp temp_boesp.xml temp_boesp_01.xml
 cp temp_boesp_AB_1b_slp1.txt temp_boesp_AB_01.xml

check line-numbers of '<info.../>' note first diff
python firstdiff.py temp_boesp_01.xml temp_boesp_AB_01.xml
 line 158386. Remove 'line-repeated' comment in AB (3 of them)
 Remove repeated lines at L=1796:
    VṚDDHA-CĀṆ. ²d.
    <s>varjayetyaRqitaH sadA</s>

1. L=7223.1 missing V4 . Similarly, L=7224 has extra V4 in 01
  
2. AB_01 deletes entry <info L="7668.1" page="5.223" gtypes="HS"/>
 and puts the text into Footnote of 7668
 I temporarily reinstate 7668.1 into AB_01
3. AB_01 deletes entry <info L="7687.1" page="5.226" gtypes="HS"/>
 and puts text into F7687
 I temporarily reinstate 7687.1 into AB_01
4. AB_01 deletes entry <info L="7690.1" page="5.226" gtypes="HS"/>
 Do not know where the text was put?
 I temporarily reinstate 7690.1 into AB_01
5. AB_01 deletes 7711.1 and puts text into F 7711
 I temporarily reinstance F7711.1 in AB_01
6. AB_01 deletes 7716.1 and puts text into F7716. I reinstate
8. AB_01 deletes 7750.1 and puts text ? I reinstate
9. AB_01 deletes 7756.1 and puts text in F7756 I reinstate
10. AB_01 deletes 7785.1 and puts text ? I reinstate
11. AB_01 deletes 7788.1 and puts text ? I reinstate
12. AB_01 deletes 7791.1 and puts text ? I reinstate
13. AB_01 deletes 7794.1  and puts text ? I reinstate
14. AB_01 deletes 7838.1  and puts text ? I reinstate
15. AB_01 deletes 7841.1  and puts text ? I reinstate
16. AB_01 deletes 7845.1  and puts text ? I reinstate
17. AB_01 deletes 7846.1  and puts text ? I reinstate
18. AB_01 deletes 7847.1  and puts text ? I reinstate

Now, temp_boesp_01.xml and temp_boesp_AB_01.xml have same number of lines,
  185470.

# -------------------------------------------------------------
# Further adjustments
cp temp_boesp_01.xml temp_boesp_02.xml
cp temp_boesp_AB_01.xml temp_boesp_AB_02.xml
1. delete line in V3 n=757
2. V3 776 shld be part of 777 . (777 st. 776 means 777 'in place of' 776)
   Restore AB_02
3. in V3 n=1051: delete 2nd line '11.' and put on first line.
4. V3 n=1447: wrong in both versions.
5. V3 n=1562: wrong in both.
6. V3 n=2046 wrong in both
7. V3 n=3291 wrong in both
# -------------------------------------------------------------
python ../step0/changes/diff_to_changes.py temp_boesp_02.xml temp_boesp_AB_02.xml change_02_AB_02.txt
 348 lines changed!!
# -------------------------------------------------------------
temp_boesp_AB_02.xml will be the new version of step0/boesp.xml

# xml validation:
python ../step0/xmlvalidate.py temp_boesp_AB_02.xml ../step0/boesp.dtd
#--------------------------------------------------------
Installation

cp temp_boesp_AB_02.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

#--------------------------------------------------------
For documentation, create deva version of temp_boesp_AB_02.xml and
diff with original temp_boesp_AB_1b_deva.txt

sh transcode_ab.sh slp1 deva temp_boesp_AB_02.xml temp_boesp_AB_02_deva.xml

diff temp_boesp_AB_1b_deva.txt temp_boesp_AB_02_deva.xml > diff_AB_1b_AB_02.txt

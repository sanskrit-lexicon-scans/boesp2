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

mv boesp_deva.AB._1b.txt temp_boesp_AB_1b_deva.txt
mv 'aufrecht_entries2_deva_updated (1).txt' temp_aufrecht_updated_1_deva.txt
mv last.V4.entries.missed.V5.entry.txt temp_V4_V5_deva.txt
mv missed.V3.entries.in.digitization.txt temp_missed.V3.entries_deva.txt

# -------------------------------------------------------------
slp1 versions of 4 AB files  temp_X_deva.txt -> temp_X_slp1.txt
  <s>X</s> -> <s>Y</s>  where X is devanagari and Y is slp1
sh transcode_ab.sh deva slp1 temp_boesp_AB_1b_deva.txt temp_boesp_AB_1b_slp1.txt
  185334 lines
sh transcode_ab.sh deva slp1  temp_missed.V3.entries_deva.txt temp_missed.V3.entries_slp1.txt
sh transcode_ab.sh deva slp1  temp_V4_V5_deva.txt temp_V4_V5_slp1.txt
sh transcode_ab.sh deva slp1 temp_aufrecht_updated_1_deva.txt temp_aufrecht_updated_1_slp1.txt
 227 lines
 75 lines

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
#--------------------------------------------------------
Incorporate temp_missed.V3.entries_slp1.txt
cp temp_boesp_AB_02.xml temp_boesp_AB_03.xml
Manually insert the missing V3's, and adjust info where needed.
For L=1, L=776, L=1447*, L=1562*, L=2046*, L=3291*, L=3924, 

Also incorporate missed V4, V5 entries, using temp_V4_V5_slp1.txt
Adjust info as needed.
V4: 777, 2152, 3187, 3754, 3791, 3979, 4116, 5589, 6528 
V5: 3229, 5229
Many of these already present, but added as needed.

The entries 7716.1, 7750.1, 7788.1, 7794.1 already present.

--------------------------------------------------------

Compare temp_aufrecht_updated_1_slp1.txt to
 ../step4e/aufrecht_entries2a_updated.txt
cp ../step4e/aufrecht_entries2a_updated.txt temp_aufrecht_entries2a_updated.txt
 wc -l temp_aufrecht_*
  238 temp_aufrecht_entries2a_updated.txt
  277 temp_aufrecht_updated_1_slp1.txt
39 more lines in temp_aufrecht_updated_1_slp1.txt

So the update_1_slp1 file has 39 additional lines!

The difference is due to "V5" entries
(13 V5 elements * 3 lines/V5 = 39 lines!)

Believe that these V5 have same content as certain HS entries
e.g. <V5 n="7866"> in temp_aufrecht_updated_1_slp1.txt appears as
entry L="7668.1" in temp_boesp_03.xml.
  See the mapping of the 13 in step4e/readme.txt under '7668.1 -> 7866'

ALSO must correct the gtypes parameter in both versions.

Remove these 39 lines and save into
 temp_aufrecht_updated_2_slp1.txt

  python ../step0/changes/diff_to_changes.py temp_aufrecht_entries2a_updated.txt temp_aufrecht_updated_2_slp1.txt temp_change_2a_2_aufrecht.txt
8 changes written to temp_change_2a_2_aufrecht.txt


cp temp_aufrecht_updated_2_slp1.txt temp_aufrecht_updated_3_slp1.txt

change in .._3..
ϋ  (\u03cb)     1 := GREEK SMALL LETTER UPSILON WITH DIALYTIKA
ӓ  (\u04d3)     6 := CYRILLIC SMALL LETTER A WITH DIAERESIS
ӧ  (\u04e7)     3 := CYRILLIC SMALL LETTER O WITH DIAERESIS

to
ü  (\u00fc)    20 := LATIN SMALL LETTER U WITH DIAERESIS
ä  (\u00e4)    17 := LATIN SMALL LETTER A WITH DIAERESIS
ö  (\u00f6)    11 := LATIN SMALL LETTER O WITH DIAERESIS

  python ../step0/changes/diff_to_changes.py temp_aufrecht_entries2a_updated.txt temp_aufrecht_updated_3_slp1.txt temp_change_2a_3_aufrecht.txt

1 difference: remove brackets.  
old <s>jvaladdAvajvAlA[vali]jawilamUrterviwapinaH ..</s>
new <s>jvaladdAvajvAlAvalijawilamUrterviwapinaH ..</s>

<s>jvaladdAvajvAlAvalijawilamUrterviwapinaH ..</s>

Make this change in temp_aufrecht_entries2a_updated.txt 
Then
cp temp_aufrecht_entries2a_updated.txt  ../step4e/aufrecht_entries2b_updated.txt


--------------------------------------------------------

cp temp_boesp_AB_03.xml temp_boesp_AB_04.xml

Finally insert ../step4e/aufrecht_entries2b_updated.txt
into bottom of temp_boesp_AB_04.xml

Further now need to correct the gtypes in the new entries.
Do this manually in temp_boesp_AB_04.xml

validate
python ../step0/xmlvalidate.py temp_boesp_AB_04.xml ../step0/boesp.dtd

cp temp_boesp_AB_04.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit


Analysis of proofreading by AB and Sampada. 
Volume 1  2nd iteration.

cp ../../../boesp-prep-ab/sanproof/'boesp-1_deva_AB (rev. 29 Nov).txt' ab_deva_san_1_02.txt
cp ../../../boesp-prep-sam/sanproof/boesp-1_slp1_rev2.txt sam_slp1_san_1_02.txt

# convert AB's version to slp1 (for comparison to Sampada's version)
python transcode_ab.py ab_deva_san_1_02.txt ab_san_1_02_prep.txt

# AB version has some differences in format.
# Undo these for comparison
python adjust_ab.py ab_san_1_02_prep.txt ab_san_1_02.txt

NOT DONE
# minor adjustment to Sampada's version  (two ; --- lines with no semicolon)
python adjust_sam.py sam_slp1_san_1_02.txt sam_san_1_02.txt

AB did some kinds of changes not done by Sampada:
1) separate out HS into two lines (e.g. Verse 1123)
2) correction of page number
I'd like to get the cases where just the verses are different.
python diff_verses.py sam_san_1_02.txt ab_san_1_02.txt diff_verses.txt
2175 entries from sam_san_1_02.txt
2175 entries from ab_san_1_02.txt
different number of verse lines at entry 1450  
different number of verse lines at entry 2047
These problems for sam version

----------------------------------------------------
Show the two variants of the lines that differ
python diff_verses1.py sam_san_1_02.txt ab_san_1_02.txt diff_verses1.txt

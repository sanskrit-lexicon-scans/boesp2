
Analysis of proofreading by AB and Sampada.
Volume 1
cp ../../../boesp-prep-ab/sanproof/'boesp-1_deva_AB (11th Sep).txt' ab_deva_san_1_01.txt
cp ../../../boesp-prep-sam/sanproof/boesp-1_slp1.txt sam_slp1_san_1_01.txt

# convert AB's version to slp1 (for conversion to Sampada's version)
python transcode_ab.py ab_deva_san_1_01.txt ab_san_1_01_prep.txt
 convert's AB's Devanagari to slp1.

# AB version has some differences in format.
# Undo these for comparison
python adjust_ab.py ab_san_1_01_prep.txt ab_san_1_01.txt

# minor adjustment to Sampada's version  (two ; --- lines with no semicolon)
python adjust_sam.py sam_slp1_san_1_01.txt sam_san_1_01.txt

AB did some kinds of changes not done by Sampada:
1) separate out HS into two lines (e.g. Verse 1123)
2) correction of page number
I'd like to get the cases where just the verses are different.
python diff_verses.py sam_san_1_01.txt ab_san_1_01.txt diff_verses.txt
2175 entries from sam_san_1_01.txt
2175 entries from ab_san_1_01.txt
different number of verse lines at entry 1450  
different number of verse lines at entry 2047
These problems for sam version


step4a2/readme.txt
volume 2 sanskrit verse proofreading

first round
version from Sampada: boesp-2_slp1-sam1.txt
 obtained from repository boesp-prep-sam/sanproof/boesp-2_slp1.txt
 as of 03-20-2022.

version from Andhrabharati: 
 ref: https://github.com/funderburkjim/boesp-prep-ab/issues/10#issuecomment-1079996106
 boesp-2_deva_AB.txt

convert AB version to slp1: boesp-2_slp1_ab1.txt
 copied transcode_ab.sh from step4a1, and modified slightly.
 sh transcode_ab.sh deva slp1 ../../step4a2/boesp-2_deva_AB.txt ../../step4a2/boesp-2_slp1_ab1.txt
 
Note:
../../step4a2/ is necessary because the transcoding is done by a program
 in step1a/sanproof_1_02 directory.

sh ../step4a1/transcode_ab.sh deva slp1 ../../step4a2/boesp-2_deva_AB.txt ../../step4a2/boesp-2_slp1_ab1.txt
======================================================================
Based on the issue#10 comment above, 
boesp-2_slp1-sam1a.txt, boesp-2_slp1-ab1a.txt
cp boesp-2_slp1-sam1.txt boesp-2_slp1-sam1a.txt
1. #3077  4-lines
2. #3996  remove duplicate line in sam1a
3. #4029 Not done:  Will investigate later
   Note the print change at S.4029, which makes the verse properly match the meter of AryA.
4. Calembourg.  AB thought this Word should be placed in a new HS entry at
   L=4041.1.
   Thomas has the word at the end of the Footnote for 4041.
   For the moment I make a new boesp-2_slp1-ab1a.txt with 4041.1 removed.
5. (extra).  L="3359. 4 lines Change to sam1a
6. removed '; print error: जलामव > जलमिव.' under L="4029" in ab1
With these changes, the ab1a and sam1a files have same number of lines (23039).

======================================================================
comparison.
python diff_verses1.py boesp-2_slp1-sam1a.txt boesp-2_slp1_ab1a.txt boesp-2_slp1_diff1.txt
  Uses Edit class from ../step4a1/update_xml_verses.py
 
2800 edits from boesp-2_slp1-sam1a.txt
2800 edits from boesp-2_slp1_ab1a.txt
174 lines with differences in Sanskrit verse
174 written to boesp-2_slp1_diff1.txt

prepare deva version for ab
sh ../step4a1/transcode_ab.sh slp1 deva ../../step4a2/boesp-2_slp1_diff1.txt ../../step4a2/boesp-2_deva_diff1.txt

=========================================================================
distribute to Andhrabharati for examination.

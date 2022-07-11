step4a3/readme.txt
volume 3 sanskrit verse proofreading

first round
version from Sampada: boesp-3_slp1-sam.txt
 obtained by email 07-01-2022

version from Andhrabharati: 
 ref: https://github.com/funderburkjim/boesp-prep/issues/49#issuecomment-1178037578
 boesp-3_deva_AB.txt  (renamed from verses_03_deva.AB.txt)
 There are comments from AB at bottom, these removed to
  readme_ab_3.txt, and the remaining verses in
  boesp-3_deva_ab0.txt
   
convert AB version to slp1: boesp-3_slp1_ab1.txt
 copied transcode_ab.sh from step4a1
 sh transcode_ab.sh deva slp1 ../../step4a3/boesp-3_deva_ab0.txt ../../step4a3/boesp-3_slp1_ab0.txt
28869 read from ../../step4a3/boesp-3_deva_ab0.txt
28869 written to ../../step4a3/boesp-3_slp1_ab0.txt

Note:
../../step4a3/ is necessary because the transcoding is done by a program
 in step1a/sanproof_1_02 directory.


======================================================================
resolve differences in number of lines
 wc -l boesp-3_slp1*
  28869 boesp-3_slp1_ab0.txt
  28880 boesp-3_slp1_sam.txt

python diff_verses1.py boesp-3_slp1_sam.txt boesp-3_slp1_ab0.txt temp_boesp-3_slp1_diff1.txt
3521 edits from boesp-3_slp1_sam.txt
3521 edits from boesp-3_slp1_ab0.txt
different number of edit lines at L="4794,4795" x  extra line deleted from sam1
different number of edit lines at L="5334,5335" x
different number of edit lines at L="5373,5374" x
different number of edit lines at L="5672,5673" x
different number of edit lines at L="5678,5679" x
different number of edit lines at L="5915,5916" x
different number of edit lines at L="6610,6611" x
different Ls at edit 2296
6634.3 != 6634.4
different Ls at edit 2297
6634.4 != 6634.5
different number of edit lines at L="6844,6845" x
different number of edit lines at L="7053,7054" x
different number of edit lines at L="7403,7404" x
------------------------------------------------
cp boesp-3_slp1_sam.txt boesp-3_slp1_sam1.txt
 - delete 10 extra lines from sam1 (9 are extra pb, 1 is repeated verse)
# rerun verses1.py, using sam1
python diff_verses1.py boesp-3_slp1_sam1.txt boesp-3_slp1_ab0.txt temp_boesp-3_slp1_diff1.txt
3521 edits from boesp-3_slp1_sam1.txt
3521 edits from boesp-3_slp1_ab0.txt
different Ls at edit 2296
6634.3 != 6634.4
different Ls at edit 2297
6634.4 != 6634.5

change 6634.4 to 6634.5 in sam1
Change 2nd 6634.3 to 6634.4 in sam1
# rerun verses1.py, using sam1
python diff_verses1.py boesp-3_slp1_sam1.txt boesp-3_slp1_ab0.txt boesp-3_slp1_diff1.txt

567 lines with differences in Sanskrit verse
567 written to boesp-3_slp1_diff1.txt

YIKES 567  differences!

======================================================================

prepare deva version for ab
sh transcode_ab.sh slp1 deva ../../step4a3/boesp-3_slp1_diff1.txt ../../step4a3/boesp-3_deva_diff1.txt

=========================================================================
distribution of diff1:
to Andhrabharati
  boesp-3_deva_diff1.txt
to Sampada
  boesp-3_slp1_diff1.txt
  the print-correction notes from AB (part of readme_ab_3.txt).
=========================================================================
Revision1 by Andhrabharati
ref: https://github.com/funderburkjim/boesp-prep/issues/49#issuecomment-1179654452
 verses_03_deva.AB.-Rev.1.txt
 There are comments from AB at bottom, these removed to
  readme_ab_3_rev1.txt, and the remaining verses in
  boesp-3_deva_ab0_rev1.txt
  
convert AB version to slp1: boesp-3_slp1_ab1_rev1.txt
 copied transcode_ab.sh from step4a1
 sh transcode_ab.sh deva slp1 ../../step4a3/boesp-3_deva_ab0_rev1.txt ../../step4a3/boesp-3_slp1_ab0_rev1.txt
28869 read from ../../step4a3/boesp-3_deva_ab0_rev1.txt
28869 written to ../../step4a3/boesp-3_slp1_ab0_rev1.txt

Recompute diff
python diff_verses1.py boesp-3_slp1_sam1.txt boesp-3_slp1_ab0_rev1.txt boesp-3_slp1_diff1_rev1.txt
3521 edits from boesp-3_slp1_ab0_rev1.txt
251 written to temp_boesp-3_slp1_diff1_rev1.txt

Still a lot of differences, but 316 fewer differences than before. Good!

prepare deva version for ab
sh transcode_ab.sh slp1 deva ../../step4a3/boesp-3_slp1_diff1_rev1.txt ../../step4a3/boesp-3_deva_diff1_rev1.txt

=========================================================================
distribution of diff1:
to Andhrabharati
  boesp-3_deva_diff1_rev1.txt
to Sampada
  boesp-3_slp1_diff1_rev1.txt
  the print-correction notes from AB (part of readme_ab_3.txt).
=========================================================================

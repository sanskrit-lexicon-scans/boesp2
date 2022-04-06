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
=========================================================================
revisions from AB.
boesp-2_deva_AB.revised.txt  (see boesp-prep-ab/issues/10 comments)
boesp-2_deva_diff1.AB.comments.-revised.txt
# convert to slp1
sh ../step4a1/transcode_ab.sh deva slp1 ../../step4a2/boesp-2_deva_AB.revised.txt ../../step4a2/boesp-2_slp1_ab2.txt

boesp-2_slp1_ab2a.txt  :
 remove L=4041.1 to facilitate comparison. Also remove comment at L=4029

Also convert to slp1 AB's revised comments file:
sh ../step4a1/transcode_ab.sh deva slp1 ../../step4a2/boesp-2_deva_diff1.AB.comments.-revised.txt ../../step4a2/boesp-2_slp1_diff1.AB.comments.-revised.txt

boesp-2_slp1_diff2.txt:
compare sampada's with revised-ab.
python diff_verses1.py boesp-2_slp1-sam1a.txt boesp-2_slp1_ab2a.txt boesp-2_slp1_diff2.txt

2800 edits from boesp-2_slp1-sam1a.txt
2800 edits from boesp-2_slp1_ab2a.txt
148 lines with differences in Sanskrit verse
148 written to boesp-2_slp1_diff2.txt

======================================================================
Prepare for Sampada:
put into boesp-prep-sam:
 boesp-2_slp1-sam1a.txt   Sampada to revise this file
 boesp-2_slp1_diff2.txt   Differences after AB's revision
 boesp-2_slp1_diff1.AB.comments.-revised.txt   AB's comments on diffs.
 Also mention AB's issue comments starting at
 https://github.com/funderburkjim/boesp-prep-ab/issues/10#issuecomment-1082383492
 
 cp boesp-2_slp1-sam1a.txt /c/xampp/htdocs/funderburkjim/boesp-prep-sam/sanproof/
 cp boesp-2_slp1_diff2.txt /c/xampp/htdocs/funderburkjim/boesp-prep-sam/sanproof/
 cp boesp-2_slp1_diff1.AB.comments.-revised.txt /c/xampp/htdocs/funderburkjim/boesp-prep-sam/sanproof/
======================================================================
Sampada's revisions sam1b
 boesp-2_slp1-sam1b.txt
 boesp-2_slp1-sam1b_comments.txt

boesp-2_slp1_diff3.txt
Remaining differences
python diff_verses1.py boesp-2_slp1-sam1b.txt boesp-2_slp1_ab2a.txt boesp-2_slp1_diff3.txt
2800 edits from boesp-2_slp1-sam1b.txt
2800 edits from boesp-2_slp1_ab2a.txt
25 lines with differences in Sanskrit verse
25 written to boesp-2_slp1_diff3.txt

ejf comments:
A X vs. AX   Should be 'A X' to agree with print.
Here are differences, with choice based on print agreement.
2281 <s>bindunEvADikA cintA citAtyalpA hi BUtale ..</s>
2342 <s>A janmanaH smarotpattO mAnasenozarAyitam ..</s>
2495 <s>BiyaH sImA mftyuH sukftakulasImASritaBftiH</s>
2597 <s>tfzRAM CindDi Baja kzamAM jahi madaM pApe ratiM mA kfTAH</s>
2605.1 <s>te te satpuruzAH parArGaGawakAH</s> s. Spruch 1460.
2642 <s>triBirvarzEstriBirmAsEstriBiH pakzEstriBirdinEH .</s>
* 2646 utam agrees with scan, but may be print error ('uttam')
2646 <s>triviDAH puruzA rAjannutamADamamaDyamAH .</s>
2646 <s>triviDAH puruzA rAjannuttamADamamaDyamAH .</s>
* 2731, 2732 <pb n="2.106"/>
2656 <s>mAlatISaSaBflleKAkadalInAM kaWoratA ..</s>
2743 <s>rAjAkulInaH sukulaSva dAsaH paSyantu lokAH kalikelitAni ..</s>
2918 <s>dfzwASca PullA niculA na mftA cAsmi kiM nvidam ..</s>
3045 <s>vinASe nASe vA tava sati viyogo 'styuBayaTA .</s>
3198 <s>na kiMtkvicidastIha vastvasADyaM vipaScitAm .</s>
* 3198 probable print error
 3198 <s>na kiMcitkvacidastIha vastvasADyaM vipaScitAm .</s>

3358 <s>A dehapatanAdgaNgAmupAste yaH pumAniha ..</s>
3459 <s>na Sakyo vAyurAkASe pASErbandDuM manojavaH .</s>
3562 <s>A mftyoH SriyamanvicCennEnAM manyeta durlaBAm ..</s>
3661 <s>sundopasandAvanyo 'nyaM samavIryO hatO na kim ..</s>
3811 <s>nfpARAM ca narARAM ca kevalaM tulyamUrtitA .</s>
3926 <s>paraduHKaM samAkarRya svaBAvasujano janaH .</s>
3926 <s>upakArAsamarTatvAtprApnoti hfdayavyaTAm ..</s>
4036 <s>so 'yaM candraH patati gaganAdalpaSezErmUyaKE-</s>
4125 <s>punarnaro yAcati yAcyate ca punarnaraH Socati Socyate ca ..</s>
4156.2 <s>pustake pratyayADItam</s> und <s>pustakezu ca nADItaH (nADItam)</s> s. Spruch 4155.
4193 <s>pOlasyaH kaTamanyadAraharaRe dozaM na vijYAtavA-</s>
4299 <s>premArdraM spfhaRIyanirBararahaHkrIqApragalBaM tato</s>
4487 <s>aviSvAsI taTA ca syAdyaTA saMvyavahAravAn ..</s>

Prepared boesp-2_slp1_final.txt based on above
 Two intentional print changes:
 3198 old <s>na kiMtkvicidastIha vastvasADyaM vipaScitAm .</s>
 3198 new <s>na kiMcitkvacidastIha vastvasADyaM vipaScitAm .</s>
 2646 old <s>triviDAH puruzA rAjannutamADamamaDyamAH .</s>
 2646 new <s>triviDAH puruzA rAjannuttamADamamaDyamAH .</s>
 

Compare to latest revision from ab:
python diff_verses1.py boesp-2_slp1_ab2a.txt boesp-2_slp1_final.txt boesp-2_slp1_diff_ab2a_final.txt

13 lines with differences in Sanskrit verse


Compare to latest revision from sampada:
python diff_verses1.py boesp-2_slp1-sam1b.txt boesp-2_slp1_final.txt boesp-2_slp1_diff_sam1b_final.txt
15 lines with differences in Sanskrit verse

upload these for further comments from AB and Sampada.
=============================================================

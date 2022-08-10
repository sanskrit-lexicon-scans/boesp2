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
  
convert AB version to slp1: boesp-3_slp1_ab0_rev1.txt
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
sampada's corrections based on boesp-3_slp1_diff1_rev1.txt:
boesp-3_slp1_sam2.txt
Recompute diff:
python diff_verses1.py boesp-3_slp1_sam2.txt boesp-3_slp1_ab0_rev1.txt boesp-3_slp1_diff1_rev2.txt
3521 edits from boesp-3_slp1_sam2.txt
3521 edits from boesp-3_slp1_ab0_rev1.txt
17 lines with differences in Sanskrit verse
17 written to boesp-3_slp1_diff1_rev2.txt

boesp-3_sam2_comments.txt contain comments by Sampada and Jim on these
17 differences, and also a few others mentioned by Sampada.

Ask Andhrabharati and Sampada to review these comments.
=========================================================================
AB comments in issue 49 integrated into  boesp-3_sam2_comments.txt

=========================================================================
# initialize boesp-3_slp1_final_1.txt from boesp-3_slp1_ab0_rev1.txt

cp boesp-3_slp1_ab0_rev1.txt boesp-3_slp1_final_1.txt

# initialize temp_boesp_0.xml from step0/boesp.xml
cp ../step0/boesp.xml temp_boesp_01.xml

# Manually edit
 (a) boesp-3_slp1_final_1.txt and
 (b) temp_boesp_01.xml 
so that next step succeeds
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
Note: this is required because some changes were made to step0/boesp.xml
  AFTER verse extracts for volume 3 were prepared for Sampada and Andhrabharati.

---------------------------------------------------
1) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
edit_entry error.
entry.info =  <info L="5229" page="3.120" gtypes="S,D,F,V5"/>
edit info  =  <info L="5229" page="3.120" gtypes="S,D,F"/>

modify final_1:
5560 old <info L="5229" page="3.120" gtypes="S,D,F"/>
5560 new <info L="5229" page="3.120" gtypes="S,D,F,V5"/>


---------------------------------------------------
2) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
edit entry not found 6634.5
edit_entry error.
entry.info =  <info L="7223.1" page="3.539" gtypes="HS,V4"/>
edit info  =  <info L="7223.1" page="3.539" gtypes="HS"/>

modify temp_boesp_01.xml:
 replace 6634.4 by both 6634.4 and 6634.5 of final_1
modify final_1 to agree with boesp_01 at 7223.1
---------------------------------------------------
3) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
edit_entry error.
entry.info =  <info L="7224" page="3.539" gtypes="S,D,F"/>
edit info  =  <info L="7224" page="3.539" gtypes="S,D,F,V4"/>

modify final_1 to agree with boesp 

---------------------------------------------------
4) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="4794,4795" page="3.31" gtypes="S,S,D,D,F,V5"/>

in boesp_1, remove   <pb n="3.32"/> in <S n="4794">  (pb is present after 4795)
---------------------------------------------------
5) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="5334,5335" page="3.140" gtypes="S,S,D,D,F"/>

in boesp_1, remove <pb n="3.141"/> in <S n="5334">  (pb is present after 5335)

---------------------------------------------------
6) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="5373,5374" page="3.148" gtypes="S,S,D,D,F"/>

in boesp_1, remove <pb n="3.149"/> in <S n="5373">. (pb is present after 5374)

---------------------------------------------------
7) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="5672,5673" page="3.207" gtypes="S,S,D,D,F"/>


in boesp_1, remove <pb n="3.208"/> in <S n="5672">. (pb is present in 5673)
---------------------------------------------------
8) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="5678,5679" page="3.208" gtypes="S,S,D,D,F"/>

in boesp_1, remove <pb n="3.209"/> in <S n="5678">.

---------------------------------------------------
9) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="5915,5916" page="3.260" gtypes="S,S,D,D,F"/>

in boesp_1, remove <pb n="3.261"/> from <S n="5915">

---------------------------------------------------
10) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="6610,6611" page="3.408" gtypes="S,S,D,D,F"/>

Remove duplicate line '<s>pramdAH kAmayAne zu yajamAnezu yAjakAH .</s>'
 from boesp_1

---------------------------------------------------
11) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="6844,6845" page="3.457" gtypes="S,S,D,D,F"/>

in boesp_1, remove '<pb n="3.458"/>' in <S n="6844">

---------------------------------------------------
12) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="7053,7054" page="3.502" gtypes="S,S,D,D,F"/>

in boesp_1, remove <pb n="3.503"/> from <S n="7053">

---------------------------------------------------
13) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="7403,7404" page="3.577" gtypes="S,S,D,D,F"/>

in boesp_1, remove <pb n="3.578"/> from <S n="7403">

---------------------------------------------------
14) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
newlines anomaly <info L="7545" page="3.606" gtypes="S,D,F"/>

in boesp_1, remove '<s>garalena sahAvAsAtpayAH .</s>' duplicate

---------------------------------------------------
FINALLY SUCCESS!
15) 
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_1.txt temp_boesp_02.xml
185724 lines read from temp_boesp_01.xml
9102 entries found
3521 edits from boesp-3_slp1_final_1.txt
185724 lines written to temp_boesp_02.xml

=========================================================================
FINAL REVISION OF VERSES
=========================================================================
boesp-3_slp1_final_2.txt  
cp boesp-3_slp1_final_1.txt boesp-3_slp1_final_2.txt

There are 21 'cases' mentioned in boesp-3_sam2_comments.txt.

In 7 of these 21 cases,  I have made made changes to the AB version.
In the other 14 cases, no change has been made to AB version.

----------------------------------
In 10 of these, Jim's choice is already represented by AB's text
in boesp-3_slp1_final_2.txt:
- 4844 no change. AB version used.
- 4908 no change. AB version used.
- 5042 no change. AB version used.
- 5306 no change. AB version used.
- 5689 no change. AB version used.
- 6049 no change. AB version used.
- 6109 no change. AB version used.
- 6401 no change. AB version used.
- 6842 no change. AB version used.
- 7223.1 no change. AB version used.

=========================================================================
THE 7 CHANGES MADE (shown in three groups of 4, 1, 2)
boesp-3_slp1_final_2.txt is same as boesp-3_slp1_ab0_rev1.txt except
for these 7 changes.
----------------------------------
4 changes to boesp-3_slp1_final_2.txt,
 where AB comments 'AB text is wrong here' in issue49 confirm his agreement.

+ 4771.1 AB text is wrong here
old: <s>mahAvratisahasrezu</s> s. nach Spruch <s>miTyAMdfzwisahasrezu</s>.
new: <s>mahAvratisahasrezu</s> s. nach Spruch <s>miTyAdfzwisahasrezu</s>.

+ 5487 AB text is wrong here.
old: <s>yAvadBA BAraverBAti (yAvadBABA raverBAti) tAbanmAGo na dfSyate .</s>
new: <s>yAvadBA BAraverBAti (yAvadBABA raverBAti) tAvanmAGo na dfSyate .</s>

+ 6249 AB comment confirms 'vaDyaH' (agrees with scan)
old: <s>vftimapyASritaH SatrurvaTyaH syAdvijigIzuRA .</s>
new: <s>vftimapyASritaH SatrurvaDyaH syAdvijigIzuRA .</s>

+ 6846 AB text is wrong here.
old: <s>samAdiSatpitA putraM leKaM mamAjYayA .</s>
new: <s>samAdiSatpitA putraM liKa leKaM mamAjYayA .</s>

----------------------------------
1 change to boesp-3_slp1_final_2.txt,
where  AB  concurs with comment 'Go with <s>Bintte</s> as suggested'

+ 5226.1 AB agrees  (print change)
old: <s>yadi Binatte sUryaputraH (sUryasutaH)</s> s. Spruch 5230.
new: <s>yadi Bintte sUryaputraH (sUryasutaH)</s> s. Spruch 5230.


-- 5579. ²a. <s>°praboDamanasastezAmaBinnA</s>. ²d. Lies <s>rocate</s>.
</V5>
old: <s>svAtmanyeva samAptahemamahimA merurna me rAcate ..</s>
new: <s>svAtmanyeva samAptahemamahimA merurna me rocate ..</s>

- 5710 no change
  AB shows clearer scan with 'niyant' --  and there are
  some words in MW with 'niyant' (e.g. niyantavya)
  So maybe 'niyanta' is a legitimate spelling variation of 'niyata' ?
old: <s>raTaH SarIraM puruzasya dfzwamAtmA niyantendriyARyAhuraSvAn .</s>
new: <s>raTaH SarIraM puruzasya dfzwamAtmA niyatendriyARyAhuraSvAn .</s>

----------------------------------


2 cases of changes made but not (yet) confirmed by AB comments 
Revise according to Jim's suggestions in boesp-3_sam2_comments.txt


+ 4927 AB ?
old: <s>mUlaBftyAparADena nAgantUnpratimAnayet .</s>
new: <s>mUlaBftyoparoDena nAgantUnpratimAnayet .</s>
Note: Sampada agrees with AB: mUlaBftyAparADena
Note: mUlaBftyoparoDena agrees with print

+ 6119 AB concur? (meter requires 'samo') 
old: <s>veSyA mahApaTaH proktA nijanArI yaTA ..</s>
new: <s>veSyA mahApaTaH proktA nijanArI samo yaTA ..</s>

----------------------------------
4 cases where Jim changes mind to agree with AB version.
No change in boesp-3_slp1_final_2.txt
'new' (jim's original suggestion) not used.

- 5268 'AB text is wrong here.' ( AB's original comment)
Use yadDyayaM for alphabetical ordering of shlokas.
Note: Jim makes additional comment in issue 49.
Note: AB makes further comment regarding Devanagari text in issue49.
old: <s>yadDyayaM puruzaH kiMcitkurute vE SuBASuBam .</s>
new: <s>yadvyayaM puruzaH kiMcitkurute vE SuBASuBam .</s>

- 5488 no change.  use yAvadBriyeta
  AB comment notes that 'Briyeta' conforms to alphabetical order of shlokas.
old: <s>yAvadBriyeta jaWaraM tAvatsvatvaM hi dehinAm .</s>
new: <s>yAvadDriyeta jaWaraM tAvatsvatvaM hi dehinAm .</s>

- 5579 no change
(use rAcate)  AB notices the correction in an addendum.
<V5 n="5579">

=========================================================================
Install final version of volume 3 verses into temp_boesp_03.xml.
python ../step4a1/update_xml_verses.py temp_boesp_01.xml boesp-3_slp1_final_2.txt temp_boesp_03.xml


boesp/step1a
Continue sanskrit verse proofreading work begun in step1 directory.

Basic idea:
 extract <HS> and <S> groups from boesp_utf8.txt. The Sanskrit is in HK.
 transcode  to SLP1.
 Further transcode from slp1 to devanagari.
 The slp1-devanagari versions are then proofread and a 'final' version
 generated in slp1.
 This slp1 version transcoded back to HK.
 Finally, the proofread HK verses are made to replace the original HK verses
 in boesp_utf8.
 
 and also then transcode from SLP1 
 SLP1 and Devanagari encodings for proofreading.
Also, permit
REASON:  The purpose of this transcoding is to prepare various
transcodings of the Sanskrit verses (S and HS sections) for proof-reading.
The changes Thomas makes to boesp-1_ansi.txt often introduce new corrections.
Keeping in sync with these new corrections is too time-consuming, and is
believed to be non-material to the S,HS proof-reading.

; -------------------------------------------------------------
; Preliminary to transcoding and extraction
; Various 'corrections'
; End result is temp_boesp_04.txt,
; WHICH IS IDENTICAL TO step0/changes/boesp_20.txt
; THIS MATERIAL CAN BE SKIPPED now that boesp_20.txt is constructed.
; Go to the 'TRANSCODING to slp1' section below
; -------------------------------------------------------------

Transcode boesp-1_utf8.txt
  Printed Devanagari is represented in HK transcoding.
  Devanagari appears in two forms:
  1) within an 'S' block.  Here ALL text represents Devanagari.
    An 'S' block is identified by:
      a line starting with <S>, and then all following non-blank lines.
      Skip the first <S> block which appears on line 3 and is not Sanskrit
  2) within other blocks.  Here Devanagari text is in {#...#} markup.
     Note that the {#...#} fragments may span multiple lines.
  3) the @ character is introduced -- it appears nowhere else
     It is used within <S> sections to indicate a line break for 'long lines'
     There are  156 such entries identified.

cp ../step0/changes/boesp_16.txt temp_boesp_00.txt
   commit 9bfe9ee22fe0a61e40508eb8b414c873fe2b28a5
   134169 lines.
temp_boesp_01.txt:
  manual corrections of errors noticed in hk conversion.  see temp_change_01.txt
  python ../step0/changes/updateByLine.py temp_boesp_00.txt temp_change_01.txt temp_boesp_01.txt
  ../step0/changes/boesp_17.txt is a copy of temp_boesp_01.txt.
  
  
temp_boesp_02.txt  detach multiple HS.
  cp temp_boesp_01.txt temp_boesp_02.txt
  manually change to separate joined-hs
  EXAMPLE:
OLD:
<HS>{#indro vai khaNDamAhuH#} s. Spruch· 
1110. {#ipsitaM manasaH saram#} s.· 
Spruch 1148.·
NEW:
<HS>{#indro vai khaNDamAhuH#} s. Spruch 1110. · 
 
<HS>{#ipsitaM manasaH saram#} s. Spruch 1148.· 
 
  temp_change_02.txt
python ../step0/changes/diff_to_changes.py temp_boesp_01.txt temp_boesp_02.txt temp_change_02.txt
 ../step0/changes/boesp_18.txt is copy of temp_boesp_02.txt


temp_boesp_03:  Put all <HS> on a single line (in agreement with pdf).
python merge_hs.py temp_boesp_02.txt temp_boesp_03.txt
  generate the associated changes
python ../step0/changes/diff_to_changes.py temp_boesp_02.txt temp_boesp_03.txt temp_change_03.txt

temp_boesp_04:  Reformat verses with 'long lines'
This has been done for the verses in volume 1 (1 - 2219)
 For example: saying 75:
<S> agrAhyaM hRdayaM tathaiva vadanaM yaddarpaNAntargataM· 
bhAvaH parvatasUkSmamArgaviSamaH strINAM na vijJayate |· 
cittaM puSkarapattratoyataralaM vidvadbhirAzaMsitaM· 
nArI nAma viSAGkarairiva latA doSaiH samaM vardhitA ||· 

Now to do the same for the verses from
 volume 2 : 2220-4649
 volume 3 : 4650-7613
 volume 4.2(B) : 7614-7865
This is done in 2 steps:
First, in a copy of temp_boesp_03.txt, mark additional line breaks by the
'@' character.  Note this may appear (a) after a word or (b) in the middle
of a word. The additional breaks are determined by visual examination of the pdfs.
Second, a program will actually generate the line breaks from the '@' characters.

cp temp_boesp_03.txt temp_boesp_04_atsign.txt
  Then, manually adjust temp_boesp_04_at.txt with '@' signs.
  Then, break into multiple lines at the @ sign.
python reformat_atsign.py temp_boesp_04_atsign.txt temp_boesp_04.txt


; -------------------------------------------------------------------------
; TRANSCODING to slp1
; -------------------------------------------------------------------------
NOTE: temp_boesp_04.txt is same as step0/changes/boesp_20.txt.
python boesp_transcode.py hk slp1 temp_boesp_04.txt temp_boesp_slp1.txt

  Use transcoder file hk_slp1.xml.  This is standard transcoding, except
  1) the vertical bar '|' represents danda, and is converted to slp1 period '.'
  2) the period '.' is changed to '_'
    NOTE: Assume that underscore does not appear
     anywhere in boesp-1_utf8.txt. Also, it plays no role in slp1_hk.xml
    There are no periods in the <S> sections, but many in the {##} sections.
    
Check invertibility:
python boesp_transcode.py slp1 hk temp_boesp_slp1.txt temp_boesp_slp1_hk.txt

diff temp_boesp_04.txt temp_boesp_slp1_hk.txt
 # NO DIFFERENCE -- AS DESIRED!
  (if differences, correct temp_boesp_hk.txt and rerun.

; -------------------------------------------------------------------------
; TRANSCODING to Devanagari
; -------------------------------------------------------------------------
Transcoding rules slp1_deva.xml and deva_slp1.xml copied from
sanskrit-lexicon/MWS repository in mwtranscode/transcoder/

python boesp_transcode.py slp1 deva temp_boesp_slp1.txt temp_boesp_deva.txt
# check for invertibility
python boesp_transcode.py deva slp1 temp_boesp_deva.txt temp_boesp_deva_slp1.txt
diff temp_boesp_slp1.txt  temp_boesp_deva_slp1.txt 
  # no difference. invertibility succeeds.

; -------------------------------------------------------------------------
; extraction of HS and S groups 
; -------------------------------------------------------------------------
python extractsan1.py 1 temp_boesp_slp1.txt boesp_slp1_san_1.txt
python extractsan1.py 2 temp_boesp_slp1.txt boesp_slp1_san_2.txt
# the first parameter indicates which volume to extract: 1,2,3,or 4
python extractsan1.py 1 temp_boesp_deva.txt boesp_deva_san_1.txt
python extractsan1.py 2 temp_boesp_deva.txt boesp_deva_san_2.txt

cp boesp_slp1_san_2.txt copied to boesp-prep-sam/sanproof/boesp-2_slp1.txt
cp boesp_deva_san_2.txt copied to boesp-prep-ab/sanproof/boesp-2_deva.txt
These are basis of proofreading by Sampada and Andhrabharati for volume 2.

cp boesp_slp1_san_2.txt ../../boesp-prep-sam/sanproof/boesp-2_slp1.txt
cp boesp_deva_san_2.txt ../../boesp-prep-ab/sanproof/boesp-2_deva.txt

Now Sampada and Andhrabharati will proofread.

; -------------------------------------------------------
; sanproof_1_01
Comparison number 01 of two proofreadings of volume 1 digitizations.
About 350 verses have differences (out of about 2200 verses).
diff_verses.txt  provided back to the two proofreaders for review.

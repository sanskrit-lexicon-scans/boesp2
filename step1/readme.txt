
boesp/step1
IMPORTANT NOTE:  This work is based on boesp-1_ansi.txt at commit
8d0fa64a51d72f9c043264dd25d460160066c60e

REASON:  The purpose of this transcoding is to prepare various
transcodings of the Sanskrit verses (S and HS sections) for proof-reading.
The changes Thomas makes to boesp-1_ansi.txt often introduce new corrections.
Keeping in sync with these new corrections is too time-consuming, and is
believed to be non-material to the S,HS proof-reading.

The main impact is that this work uses a separate copy of boesp-1_utf8.txt.
This version began with the 8d0fa.. version of boesp-1_ansi.txt, and has
additional corrections required for the programs herein.

For convenience, I keep (in 8d0f) the above version boesp-1_ansi.txt and
the initial conversion to utf8 in folders 8d0f:

# ------------------------------------------------------------------
# preliminary: temporary xml of hk version
python make_xml.py hk boesp-1_utf8.txt work_boesp-1_hk.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp-1_hk.xml ../step0/boesp.dtd
# ------------------------------------------------------------------


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
First, examine the characters appearing in Sanskrit text.
python sanchars.py boesp-1_utf8.txt sanchars_hk.txt
Note: 20210907-11:55 AM There appears to be some misplaced text
 around D1285 D1286.  Before changing this, saved a copy
 tempprev_boesp-1_utf8_0907.txt
 
First, transcode to slp1.
python boesp_transcode.py hk slp1 boesp-1_utf8.txt work_boesp-1_slp1.txt
  Use transcoder file hk_slp1.xml.  This is standard transcoding, except
  1) the vertical bar '|' represents danda, and is converted to slp1 period '.'
  2) the period '.' is changed to '_'
    NOTE: Assume that underscore does not appear
     anywhere in boesp-1_utf8.txt. Also, it plays no role in slp1_hk.xml
    There are no periods in the <S> sections, but many in the {##} sections.
    
Check invertibility:
python boesp_transcode.py slp1 hk work_boesp-1_slp1.txt temp_boesp-1_slp1_utf8.txt

diff boesp-1_utf8.txt  temp_boesp-1_slp1_utf8.txt
(NO DIFFERENCE -- AS DESIRED!)
# construct  xml and check validity
python make_xml.py slp1 work_boesp-1_slp1.txt work_boesp-1_slp1.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp-1_slp1.xml ../step0/boesp.dtd

# ------------------------------------------------------------------
---- Devanagari transcoding
Transcoding rules slp1_deva.xml and deva_slp1.xml copied from
sanskrit-lexicon/MWS repository in mwtranscode/transcoder/

python boesp_transcode.py slp1 deva work_boesp-1_slp1.txt work_boesp-1_deva.txt
# check for invertibility
python boesp_transcode.py deva slp1 work_boesp-1_deva.txt temp_boesp-1_deva_slp1.txt
diff work_boesp-1_slp1.txt  temp_boesp-1_deva_slp1.txt > tempdiff.txt
wc -l tempdiff.txt
0 # as hoped, invertibility succeeds.

# -- devanagari xml version
python make_xml.py deva work_boesp-1_deva.txt work_boesp-1_deva.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp-1_deva.xml ../step0/boesp.dtd

# ------------------------------------------------------------------
python extractsan.py slp1 work_boesp-1_slp1.xml work_san_slp1.txt

python extractsan.py deva work_boesp-1_deva.xml work_san_deva.txt

# -----------------------------------------------------------------
09-08-2021
a prior version of work_san_deva.txt was copied to
  boesp-prep-ab/sanproof/boesp-1_deva.txt
Today, I copy it back here as
  boesp-1_deva_v0.txt

Also, I copy this (final?) version of work_san_deva.txt to
a) boesp-1_deva.txt  (local)
b) boesp-prep-ab/sanproof/boesp-1_deva_rev.txt

I will use local boesp-1_deva.txt for comparing to Andhrabharati's corrections.

----
Also, I copy this (final?) version of work_san_slp1.txt to
a) boesp-1_slp1.txt
b) boesp-prep-sam/sanproof/boesp-1_slp1.txt
   The boesp-prep-sam repository is revised.
   


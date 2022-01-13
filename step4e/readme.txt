step4e

move h3 and h4 elements into separate HS entries.


Refer https://github.com/funderburkjim/boesp-prep/issues/39#issuecomment-1008521698

Start with a copy of step0/boesp.xml at commit
  9f08caa756d300ee8a7f5b2bd436232d705a13d7
git show 9f08caa7:step0/boesp.xml > temp_boesp.xml

Copy to temp_boesp_01.xml, where the changes will be made.
cp temp_boesp.xml temp_boesp_01.xml

Make new entries for all the h3, h4 elements (17 new entries).
These are the '.1' cross-reference entries.

See h3_h4_entries.txt for the new entries.  These identify which were
previously coded with <h3> and which with <h4>, in case this distinction
is needed later.

python aufprep.py temp_aufstart.txt
  Provides skeleton for the aufrecht entries
  They are numbered (L) starting with 1 more than the last Boe number (L=7865)
  Here is the correspondence between the .1 references in Boe and the
  new Aufrecht entries:
; The h3 entries from "Ueber die Paddhati von Śārngadhara" Von Th. Aufrecht
7668.1 -> 7866 <s>amuM kAlakzepaM</s>  pages 4-5 of volume 6
7687.1 -> 7867 <s>arTA na santi</s> page 73
7690.1 -> 7868 <s>alipawalEH</s> page 63
7711.1 -> 7869 <s>asyA manoharA°</s> page 82
7738.1 -> 7870 <s>AlokavantaH</s> page 49
7756.1 -> 7871 <s>uttaMsakOtuka°</s> page 12
7785.1 -> 7872 <s>etAsu ketaki</s> page 71
7791.1 -> 7873 <s>kaTamiha manuzyajanmA</s> page 62
   Note above should be page 29.  Print error in vol 5 at 7791.1
7838.1 -> 7874 <s>kusumaM koSAtakyAH</s> page 17
7841.1 -> 7875 <s>kfpaRasya samfdDInAM BoktAraH</s> page 48
7845.1 -> 7876 <s>kenAtra campakataro</s> page 85
7846.1 -> 7877 <s>kokila kalamAlApEH</s> page 40
7847.1 -> 7878 <s>kva citprARiprAptam</s> page 78

---------------------------------------------
aufrecht_entries.txt
 Separate file in which the Aufrecht entries are typed.
 constructed manually
aufrecht_entries1.txt
 Changedto unicode
 python aufrecht_transcode.py  aufrecht_entries.txt aufrecht_entries1.txt
;
aufrecht_entries2.txt
  Manual editing, esp. with regard to F and D elements.
  The F elements in boesp always (almost always) mention the source of the verse.
  That is the convention used for the F elements in the Aufrecht verses.

devanagari version for proof-reading
sh transcode_ab.sh slp1 deva ../../step4e/aufrecht_entries2.txt ../../step4e/aufrecht_entries2_deva.txt

#---------------------------------------------------
Andhrabharati revisions: from aufrecht_entries2_deva_updated.txt

1. Changed opening simple double-quote " to „ Double Low-9 Quotation Mark U201E
   And closing double-quote to “ Left Double Quotation Mark U201C
   These changes to closely resemble the printed text, but U201C is an odd
   choice.  Let it be.
   
#<s>ज्वलद्दावज्वाला[वलि]जटिलमूर्तेर्विटपिनः ॥</s>; filled up [वलि] to make the verse metrically correct. (Taken from another ed. of Sār.Pad.) Note ejf removed comment

sh transcode_ab.sh deva slp1 ../../step4e/aufrecht_entries2_deva_updated.txt ../../step4e/aufrecht_entries2_updated.txt

'umlaut' in German:
ä  (\u00e4)     LATIN SMALL LETTER A WITH DIAERESIS
ö  (\u00f6)     LATIN SMALL LETTER O WITH DIAERESIS
ü  (\u00fc)     LATIN SMALL LETTER U WITH DIAERESIS

Other 'umlaut' introduced:
ϋ  (\u03cb)     GREEK SMALL LETTER UPSILON WITH DIALYTIKA
ӓ  (\u04d3)     CYRILLIC SMALL LETTER A WITH DIAERESIS
ӧ  (\u04e7)     CYRILLIC SMALL LETTER O WITH DIAERESIS

Change to Latin with diaresis.

aufrecht_entries2a.txt
u  6
a  6
o  3
aufrecht_entries2a_updated.txt
u  1
a  6
o  3


sh transcode_ab.sh slp1 deva ../../step4e/aufrecht_entries2a_updated.txt ../../step4e/aufrecht_entries2a_updated_deva.txt

python ../step0/changes/diff_to_changes.py aufrecht_entries2_deva_updated.txt aufrecht_entries2a_updated_deva.txt change_entries2a_updated_deva.txt
 7 lines changed.

Current version of aufrecht verses: aufrecht_entries2a_updated.txt,
 with Devanagari version aufrecht_entries2a_updated_deva.txt.
Change from aufrecht_entries2_deva_updated.txt:
  change_entries2a_updated_deva.txt  (7 changes).
  
temp_boesp_02.xml
  Add (at the bottom) the Aufrecht entries.

install revised version 02 of boesp

cp temp_boesp_01.xml ../step0/boesp.xml
  commit 
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

step4c

Insert greek text.


Refer https://github.com/funderburkjim/boesp-prep/issues/46

Start with a copy of step0/boesp.xml at commit
  c594eb3896f38732551280512d35345b24848f71
git show c594eb3:step0/boesp.xml > temp_boesp.xml

Source of Greek text: greektext folder, various files.


# -------------------------------------------------------------
temp_boesp_01.xml
 <gr>a.</gr> -> <gr>α</gr>.  68
 <gr>a</gr> -> <gr>α</gr>  1
 <gr>b.</gr> -> <gr>β</gr>.  72
 141 changes.
 The 2 remaining require a longer Greek text fragment at Footnote 3202
  page="2.201"

Check validation:
python ../step0/xmlvalidate.py temp_boesp_01.xml ../step0/boesp.dtd

#--------------------------------------------------------
install revised version 01 of boesp

cp temp_boesp_01.xml ../step0/boesp.xml
  commit 6ef13d3506bf50bf5321be43ef82950b54ed37f4
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
# -------------------------------------------------------------
temp_boesp_02.xml
 Correct wrongly marked Greek text at Footnote 5001.
 <g></g> -> ²c.
install revised version 02 of boesp

cp temp_boesp_02.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
   commit f20eda859c3cd6abe02feaaf557b36b4df8305c9

# -------------------------------------------------------------
temp_boesp_03.xml
 Single-letter Greek text vol 3 
 at footnotes 6109, 6491, 6483, 7496
install revised version 03 of boesp
temp_change_03.txt

cp temp_boesp_03.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

Commit: 656610bab80840ffc3e8111ce60ca915f026e356
# -------------------------------------------------------------
temp_boesp_04.xml
Greek.Notes.and.Addenda.in.boesp-1-corrected.txt
F 583, V3 712, F 755,
F 794, F 932, F 1082, F 1089, F 1221,
F 1721, F 1870, F 1926, F 1958, F 1961,
V3 2119, V3 2167,
Greek.Notes.and.Addenda.in.boesp-2-corrected.txt
F 2343, F 2361, F 2405, F 2439, F 2654, 
F 2661, F 2836, F 3202 (<gr> -> <g>), F 3219, F 3231, 
F 3476, F 3504, F 3690, F 4019, F 4103, 
F 4111 *, F 4155, F 4253, F 4585, 
* 4111 F and V3 correction

Greek.Notes.and.Addenda.in.boesp-3-corrected.txt
F 4882, F 4911, F 4924, F 5510, F 5750, 
F 5786, F 5860, F 5881, F 6121, F 7569, 

Greek.Translations.boesp-1-corrected.txt
D 119,  D 223,  D 224,  D 372, D 1105,  
D 1291, D 1917,  D 2102

Greek.Translations.boesp-2-corrected.txt
D 2259, D 3411 , D 4003, D 4014 (check 1st word)
D 4299

Greek.Translations.boesp-3-corrected.txt

D 5040, D 6483, D 6642, D 6841, D 6854, 
D 7107, D 7128, D 7135, D 7144, D 7186, 
D 7199, D 7518, D 7524, D 7546, D 7557, 
D 7561

Note D 7135: This is printed as 7134, and VN is also silent on it.
  However the B.'s first supplement (1876) mentioned this as an error,
  and gave the correction.
  Jim: This is noted as <V4 n="7134">

first word may be wrong.Note: In these 2, the greek text is printed in a 'verse' form, where
the line breaks appear significant.
D 3411: mullti-line
D 7199: multi-line
D 6075: multi-line

#--------------------------------------------------------
install 04
cp temp_boesp_04.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

#--------------------------------------------------------
TODO: (Jonathan)
F 2597 
F 2956 
F 3483 
F 3595 
V3 3754
F 4103 
F 4327 
F 4496 
D 6075 DONE by Andhrabharati
D 7046 DONE by Andhrabharati
#--------------------------------------------------------
first word may be wrong to be checked in:
F 3219	<g>ο᾽θδὲ παρορᾷ τὸ πραϰτέον</g> 
D 4014  <g>«Ἰδού, τῇ ὑπερβολῇ ETCETERA<g>

#--------------------------------------------------------
temp_boesp_05.xml
<gr>X</gr> -> <g>X</g>  : Only need 1 tag for Greek text.
Also, change 'version' from 1.3 to 1.3.1 in boesp.xml and boesp.dtd.
Also, Greek text for D 6075 and D 7046 now provided, as well as a
correction to F 6109.

cp temp_boesp_05.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
#--------------------------------------------------------
temp_boesp_06.xml
The missing 8 F/V3 ones noted above, along with correction to F3219

cp temp_boesp_06.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh

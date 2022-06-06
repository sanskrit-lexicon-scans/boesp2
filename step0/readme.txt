#  Boehtlingk, Indische Sprüche

NOTE ON REDO (6-6-2022)
If boesp.xml is changed, then there are two steps:
1. sh transcode_xml.sh
2. cd ../web1; sh redo.sh
-----------------------------------

Reorganized step0 as of 10-20-2021.

Preliminary work with volume 1 has been moved to the 'oldwork' directory.
The readme.txt file therein may be useful in adapting some of this
preliminary work to current work.  

The current focus of this step0 directory is to have the base 'ansi'
version of boesp.  The primary document is 'boesp.all_ansi.txt'.
The boesp.all.index.txt and boesp_nachtr_ansi.txt files may later find use.
These files are assumed to be in cp1252 encoding.

The utility cp1252_utf8.py converts from cp1252 to utf8 encoding.
The utility utf8_cp1252.py converts from utf8 to cp1252.
The ea.py program provides frequency list of extended ascii characters
from utf8-encoded files.

boesp_utf8.txt  is the latest utf8 version. It is to be kept in sync
with boesp.all_ansi.txt, as far as possible.
Initialization:
python cp1252_utf8.py boesp.all_ansi.txt boesp_utf8.txt

Changes will be made to a sequence of versions of boesp_utf8.txt
These are put into 'changes' directory with the names
boesp_nn.txt.
boesp_00.txt is a copy of the initial version of boesp_utf8.txt
cp boesp_utf8.txt changes/boesp_00.txt

The changelog.txt file provides a summary of the sequence of changes
made to the utf8 version.


##---------------------------------------------------------
# convert from cp1252 encoding (Thomas uses this with Kedit)
# to utf8.

python cp1252_utf8.py boesp-1_ansi.txt boesp-1_utf8.txt
# check for invertibility
python utf8_cp1252.py boesp-1_utf8.txt boesp-1_utf8_cp1252.txt
diff -w boesp-1_ansi.txt boesp-1_utf8_cp1252.txt
# No difference  (the -w) ignores differences in line-endings.
# The utf8 version has Unix line-endings.
# remove unneeded file
rm boesp-1_utf8_cp1252.txt

##---------------------------------------------------------
getting previous version of a file  (using commit)
git show a448aa03a4da110b2c3bed0f8e050d7cbb3b9608:step0/boesp-1_ansi.txt > temp.txt

##---------------------------------------------------------
Find list of extended ASCII.
python ea.py boesp-1_utf8.txt temp_ea_boesp-1.txt
python ea.py boesp_utf8.txt temp_ea_boesp.txt

##---------------------------------------------------------
boesp4-1+2_ansi.txt
 cp1252 encoding. digitization of boesp4-1.pdf and boesp4-2.pdf
 
##---------------------------------------------------------
boesp4.2B_ansi.txt
 reformatting of 'verses' and footnotes from boesp4-1+2_ansi.txt

python cp1252_utf8.py boesp4.2B_ansi.txt boesp4.2B_utf8.txt

1) use ° instead of º
  About 30 replacements.
  
2) <eng> replaced
{#\([^#]+\) <eng>=</eng>  ->  {#\1#} = {#
 35 replacements  <eng>=</eng> in Devanagari text in Footnotes
<eng>=</eng> -> =
 5 replacements in German text in Footnotes
7 remaining instances of <eng>...</eng>, in 4 lines. All in <S> sections
 Remove <eng>.. from <S> and put in <F> (also, )
 7678
 7724 
 7752  
  Also remove phrase '<F>7614) KALPATARU. Es ist von einem Kinde im Mutterleibe die Rede.' from <F>7752.  This phrase not part of text in pdf.
 
3) AS spelling changes

##---------------------------------------------------------
A1NANDEVA : 1x
AUFRECHT : 25x
BAHIRLA1PIKA1 : 1x
BHA1MINI1VHA1SA : 1y
BHA1MINI1VILA1SA : 4x
BHA1RATACAMPU1 : 1x
DHARMADA1SA : 1x
G : 2x
G4INADHARMAVIVEKA : 1y
HAEB : 2x
HITOPADES4A : 1x
KALIVID2AMBANA : 5x
KALPATARU : 24x
KARN2A1MR2TA : 2x
KAVIVID2AMBANA : 1x
KUVALAJA1NANDA : 2y
MURA1RI : 2x
N : 1x
NAISH : 1Y
O : 20
PA1N2INI : 2x
PADDH : 1x
PAN4CA1JUDHAPRAPAN4CABHA1N2A : 2y
PAN4CA1JUDHAPRAPAN4CABHA1NA : 1y
PRASAN3GAR : 14x
PRASAN3GARATN : 1x
PRASAN3GARATNA1V : 2x
PRASAN3GARATNA1VALI1 : 3x
PRASAN3GARATNAVALI1 : 1y
RA1DHA1KR2SHN2ASAM3VA1DA : 2y
RA1G4AS4RKHARA : 1y ?
RA1GHAVACAITANJA : 1x
RASIKAG4I1VANA : 4x
RATNA1V : 2y
S : 7x
S4A1RN3GADH : 1x
S4A1RN3GADHARA : 56x
S4IS4UPA1LAV : 1x
SA1RVABHAUMA : 1x
SABHA1TARAM3GA : 17x
SPHUT2AS4LOKA : 72x
SU1KTISAM3GRAHA : 1x
TH : 12x
UTTARARA1MAC : 2x
VA1GBHAT2A : 1x
VA1SAVADATTA1 : 1x
VAIDJAG4I1VANA : 1y
VIDAGDHAMUKHAMAN2D2ANA : 2x
VIDVADBHU1SHAN2A : 1y
VIKRAM : 2
VIS4VAGUN2A1DARS4A : 9
VIT2HOBA1AN2N2A1 : 2x
VIT2HORA1AN2N2A1 : 1y
Z : 2x

; Nov 24, 2021 misc notes in conversation with Thomas.
; related to integration of boesp4-1 and boesp4-2 into boesp.all_ansi.txt.
7613 is last verse in volume 3.
 7614 - 7865 are verses from boesp-4.2  (part B)
   (+ (- 7865 7614) 1)  = 252 verses
 each has empty D group:  '<D[0-9]+>· '
 each has a footnote:  '^<F>[0-9]+) '
 each has a verse:  '<S><lg>'
   And there are one or more '<l>.*</l>' lines
 After removing these lines, only blank lines remain.
There seems to be no need for the '</F4>' ending tag of footnotes
F4.1C various locations in pdf
<F4.1> <F4.2>
<F4.1> 294.
  FORM:  '<F4.1>-- [0-9]+ ,'   (124)
         '<F4.1>-- [0-9]+ [.]' (154)
         '<F4.1>-- [0-9]+ =' (15)
         <F4.1>-- Spr. 3791, Z. 2. Lies BAHUD. st. NI1TIS4.</F4> (1)
(+ 124 154 15 1) = 294
<F4.2> 439
  FORM:   '<F4.2>-- [0-9]+ [.]' (433)
          '<F4.2>-- [0-9]+ [,]' (1)
          '<F4.2>-- [0-9]+ ([0-9]+, [0-9]+)' (4)
           <F4.2>6390-6392 . PRASAN3GAR. (1)
</F4>  732  (+ 294 439) (743)
732 of the lines of form '<F4.[12].>*</F4> $'
<F4.2>-- 11 . PRASAN3GARATNA1VALI1. 
empty D
<h3> Aufrecht
</p>  vestigial need attention.  No <p> tags are currently used.


History of indology. 1914  Digitization of article on Boehtlingk.
Tubigen professor. Correspondence between Boehtlingk and Roth.
  700 letters Attempt 2007 2015 2017. JSTOR
; -----------------------------------------
11-25-2021.
1. change 'masculine ordinal indicator' to 'degree sign' (137)
2. remove '</p>'  (32)
3. remove '</F4>' ending tags  (used only at end of '<F4.1>' or '<F4.2>' lines.
   change'</F4>' to '· '  (remove the </F4> closing tag, and insert the
     conventional 'middledot+space' currently used elsewhere.
4. Add middle dot to end of line 215 (which had missing </F4>)
NOW each line (except for the <F4.1C> lines temporarily at the top)
 and except for the 'explanation lines' at the top either:
 a) end in '· '  or
 b) are empty (with one space) '^ $'
; -----------------------------------------
12-30-2021 : transcode_xml.sh 
boesp.xml has Sanskrit encoded with slp1 transcoding, in <s>...</s> elements
sh transcode_xml.sh script  creates transcoded versions of boesp.xml.
boesp_hk.xml, boesp_iast.xml and boesp_deva.xml.
This is done by program and transcoder files in step3e directory.
; -----------------------------------------


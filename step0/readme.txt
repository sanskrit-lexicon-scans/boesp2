#  Boehtlingk, Indische Sprüche

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

##---------------------------------------------------------
boesp4-1+2_ansi.txt
 cp1252 encoding. digitization of boesp4-1.pdf and boesp4-2.pdf
 
##---------------------------------------------------------
boesp4.2(B.)_ansi.txt
 reformatting of 'verses' and footnotes from boesp4-1+2_ansi.txt

python cp1252_utf8.py boesp4.2(B.)_ansi.txt boesp4.2B_utf8.txt

##---------------------------------------------------------


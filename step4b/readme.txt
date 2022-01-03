step4b

AS conversion to IAST

Refer https://github.com/funderburkjim/boesp-prep/issues/44

Start with a copy of step0/boesp.xml at commit
  c774b7cc176837ce81631f2b2fa946f50b6e4f48
git show c774b7cc:step0/boesp.xml > temp_boesp.xml

Previous AS work done at step2/asprep.

# -------------------------------------------------------------
temp_boesp_01.xml
 Correction of SH to S2  (15)
 of N5G to N3G (2)
 J -> Y
 G4 -> J
   A few are from the V4/V5 entries that were not part of step2/asprep work
change_01.txt
python ../step0/changes/updateByLine.py temp_boesp.xml change_01.txt temp_boesp_01.xml

#python extractwords.py capnum temp_boesp_01.xml words_capnum.txt

#python extractwords.py lonum temp_boesp_01.xml words_lonum.txt

Extract words which have a letter-number sequence.
Count the frequency of such words.
Also, list the letter-number sequences that occur, along with their frequency.

python extractwords.py letternum temp_boesp_01.xml words_letternum.txt letternum.txt

184300 lines read from temp_boesp_01.xml
9071 entries found
743 distinct words written to words_letternum.txt
12227 Total number of instances of the words
30 distinct lns written to letternums.txt
1386 Total number of instances of the lns


# -------------------------------------------------------------
#Convert the letter-number sequences to IAST.
python transcode_ln.py letternums.txt letternums_iast.txt

743 records written to words_letternum_iast.txt

Note: boesp has M3 and m3 (dot above) for anusvara.  Usual convention in AS

is for anusvara to be M2 and m2 (dot below).
transcode_ln does this transformation before generating the iast.
as_roman.xml is used for the transcoding.

Also, convert the words
python transcode_ln.py words_letternum.txt words_letternum_iast.txt

# transcode boesp
python as_to_iast.py temp_boesp_01.xml temp_boesp_02.xml

The program also writes temp_as_iast_words_letternum.txt which SHOULD BE
the same as words_letternum.txt.
 IT IS THE SAME.

# Generate line changes between version 01 and 02 of boesp:
python ../step0/changes/diff_to_changes.py temp_boesp_01.xml temp_boesp_02.xml change_02.xml
10102 lines changed.
# -------------------------------------------------------------

Check validation:
python ../step0/xmlvalidate.py temp_boesp_02.xml ../step0/boesp.dtd
#--------------------------------------------------------
install revised version 01 of boesp

cp temp_boesp_01.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
#--------------------------------------------------------
install revised version 02 of boesp

cp temp_boesp_02.xml ../step0/boesp.xml

remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh

#--------------------------------------------------------

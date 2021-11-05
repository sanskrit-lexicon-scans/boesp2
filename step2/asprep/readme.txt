step2/asprep
Note:  This work should be considered complete.
 It led to creation of step0/changes/boesp_07.txt
 The file as_words.txt may be of use. It was created manually and
 aims to be a list of words with AS (letter-number) coding.
 The capital letter words are probably literary source words.
 The words with lower-case letters are primarily Sanskrit proper names
 which appear in the 'D' (German) sections.
 
# changes. First, correct cases where there is no space between period and num
 Example:  KATHA1S.68 -> KATHA1S. 68
python change_dotnum.py ../../step0/boesp_utf8.txt change_02.txt
 727 lines changed
Install these changes in step0, so boesp_utf8.txt is revised.
cp change_02.txt ../../step0/changes/
in step0, sh install.sh 01 02

# change_03.
 1.  Remove {% %} when containing ²
cp ../../step0/boesp_utf8.txt temp_boesp.txt

 2. unbalanced {%X%} or {#X#}
 python unbalanced.py temp_boesp_03.txt unbalanced.txt
 3. Require ² preceded by a space (or at beginning of a line)

python ../updateByLine.py temp_boesp.txt change_03.txt temp_boesp_03.txt
cp change_03.txt ../../step0/changes/
in step0, sh install 02 03

# change_04
  Spelling changes in  AS words
python ../updateByLine.py temp_boesp_03.txt change_04.txt temp_boesp_04.txt
  
Install these changes in step0, so boesp_utf8.txt is revised.
cp change_04.txt ../../step0/changes/
in step0, sh install.sh 03 04

python change_asgroup.py temp_boesp_04.txt notpwg.txt change_asgroup.txt

# as_1.txt  first extraction of AS words, before change_04
python as_1.py temp_boesp_03.txt as_1.txt
 1162 records
# rerun after revising change_04.txt
python as_1.py temp_boesp_04.txt as_1-rev.txt
 647 records

# --------------------------------------------------------------

pwgbib.txt from csl-pywork/v02/distinctfiles/pwg/pywork/pwgauth/
## change spelling conventions to facilitate comparison to as_1.txt
python pwgbib_alter.py pwgbib.txt pwgbib_alter.txt

## try to match as_1 spellings to pwgbib codes
#before change_04 rev
python as_2.py as_1.txt pwgbib.txt as_2.txt
1162 records written to as_2.txt
210 records found in PWG
11781 total count for abbreviations found in PWG
6117 total count for abbreviations not found in PWG


#after change_04 rev
python as_2.py as_1-rev.txt pwgbib.txt as_2-rev.txt
647 records written to as_2-rev.txt
201 records found in PWG
12184 total count for abbreviations found in PWG
5736 total count for abbreviations not found in PWG


# use pwgbib_altera instead of pwgbib_alter
python pwgbib_altera.py pwgbib.txt pwgbib_altera.txt

as_2a.py
  uses pwgbib_altera instead of pwgbib_alter
  K4->C,  G4->J
python as_2a.py as_1-rev.txt pwgbib.txt as_2a-rev.txt
647 records written to as_2a-rev.txt
219 records found in PWG
14914 total count for abbreviations found in PWG
3006 total count for abbreviations not found in PWG

# change_05
With these changes, the AS-oddities are removed for capital-letter words (LS words).
python ../updateByLine.py temp_boesp_04.txt change_05.txt temp_boesp_05.txt
1747 changes

cp change_05.txt ../../step0/changes/
in step0, sh install.sh 04 05

There are a few minor pre-corrections in change_05.
The rest are two selective changes:
 J -> Y  (example GR2HJA -> GR2HYA; but RA1JA unchanged)
 N5 -> N3 (example S4R2N5GA1R -> S4R2N3GA1R; but PAN5CAT. unchanged)
File as_j_n5_words.txt has all the J and N5 words, both those to change and
those to remain unchanged.
python change_j_n5.py temp_boesp_04.txt as_j_n5_words.txt temp_change_j_n5.txt
 (these changes added to change_05.txt)

#change_06
268 changes
python ../updateByLine.py temp_boesp_05.txt change_06.txt temp_boesp_06.txt


cp change_06.txt ../../step0/changes/
in step0, sh install.sh 05 06

# as_3 words containing lower-case letter following by digit.
# Details:
* skip H, HS, and S groups
* exclude sanskrit text in {#..#}
* Define 'words' by re.split(r'\b')
* exclude words that begin with Seite, Page
* exclude words like ANNNN, DNNNN  (in tags)
* include words that
   Begin with an upper or lower case letter ([A-Za-z])
   Then have 0 or more lower-case letters [a-z]
   Then have a digit
   Then end with 0 or more lower-case letters or digits [a-z0-9]

python as_3.py temp_boesp_05.txt as_3.txt
  388 words
python change_from_words.py temp_boesp_06.txt as_3.txt temp_change_as_3.txt
# redo word list after revisions:
python as_3.py temp_boesp_06.txt as_3-rev.txt
  334 words
  
# as_4 words mainly like those detected by change_asgroup.
# Details:
* include only groups F, V1, V2, V3
* exclude sanskrit text in {#..#}
* Define 'words' by re.split(r'\b')
* exclude words that begin with Seite, Page
* exclude tag like ANNNN, DNNNN  (in tags)
* exclude tag words <V1>, <V2>, <V3>, <F>, <S>, <H>, <HS>
* exclude roman-numerals:
   I, II, III, IV, IX,
   VI,
   XI, XIV, XVI,XVIII
* exclude one-letter word 'G'  (occurs only in 'Z. d. d. m. G.'
* include words that
   Begin with an upper-case letter [A-Z]
   contain only 0 or more upper-case letters and digits [A-Z0-9]
   
python as_4.py temp_boesp_06.txt as_4.txt
558 records written to as_4.txt
25187 words including frequency
as_4_query.txt  # words from as_4.txt to be checked
python change_from_words.py temp_boesp_06.txt as_4_query.txt temp_change_as_4_query.txt
Redo after some changes
python as_4.py temp_boesp_06.txt as_4-rev.txt
534 records written to as_4-rev.txt
25183 words including frequency

Also, remove obsolete </F> tags (14)

Also, revise F755, V3 - 755
 Manually create temp_boesp_05a.txt
 python diff_to_changes.py temp_boesp_05.txt temp_boesp_05a.txt temp_changes_f755.txt
 and add the result change_06


# ----------------------------------------------------
# change_07
--- changes of SH to S2 in selected words.
Manually review as_4-rev.txt, picking out the 'SH' words to change
Resulting file is as_4-rev_SH.txt

python change_from_words_SH_S2.py  temp_boesp_06.txt as_words_SH.txt temp_change_as_SH_S2.txt

python ../updateByLine.py temp_boesp_06.txt change_07.txt temp_boesp_07.txt
1857 changes

cp change_07.txt ../../step0/changes/
in step0, sh install.sh 06 07


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


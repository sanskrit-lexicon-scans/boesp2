
step2
works with all 3 volumes.

The starting point is ../step0/boesp_utf8.txt,

# change1.py
Not currently used.
##----------------------------------------
Use of MIDDLE DOT character to demarcate end of (non-empy) lines.
This was a 'trick' developed by Thomas so that his changes using Kedit would
not introduce 'unintentional' changes in lines.

## Perform various checks.
See directory check

## These subsequent notes are probably obsolete.
# ------------------------------------------------------------------
AS Anglicized Sanskrit checking
See directory asprep.
  Various changes.  Final version of boesp is in step0/changes/boesp_07.txt.
  asprep/as_words.txt may be of further use.
# ------------------------------------------------------------------
# preliminary: temporary xml of hk version
# NOTE: 10-19-2021 This is vestigial -- maybe it will be part of workflow later
  
python make_xml.py hk boesp_1.txt work_boesp_hk.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp_hk.xml ../step0/boesp.dtd
# -----------------------------------------------------------------
rectify lines in <S> groups.
see slines directory

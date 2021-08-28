##---------------------------------------------------------
#  Background and preliminary work for
#  Boehtlingk, Indische Sprüche 
##---------------------------------------------------------

##---------------------------------------------------------
  REST IS NOT USED
##---------------------------------------------------------
# Thomas uses cp1252 encodings in Kedit.
python utf8_cp1252.py <utf8-encoded-file>  <cp1252-encoded-file>
  Converts from utf8 to cp1252.
  NOT all characters can be transcoded.

CURRENTLY FOLLOWING IS WRONGLY SPECIFY
as_romanap.xml   transcoder file for going from AS (letter-number) to IAST

python transcoder_invert.py as_romanap.xml romanap_as.xml



# ea  (extended ascii).
Analysis of extended ascii characters appearing in ap57.txt and ap90.txt
see readme_ea.txt for details

python utf8_cp1252.py ea_ap57_other.txt ea_ap57_other_cp1252.txt 
problem: ȧ  (\u0227)     1 := LATIN SMALL LETTER A WITH DOT ABOVE
problem: ˘  (\u02d8)     1 := BREVE
problem: 卐  (\u5350)     1 := CJK UNIFIED IDEOGRAPH-5350

python utf8_cp1252.py ea_ap90_other.txt ea_ap90_other_cp1252.txt 
problem: ˘  (\u02d8)    16 := BREVE
problem: ⁁  (\u2041)     1 := CARET INSERTION POINT
problem: ◡  (\u25e1)     1 := LOWER HALF CIRCLE

cp ea_ap90_other_cp1252.txt temp_cp1252.txt
python cp1252_utf8.py temp_cp1252.txt temp_utf8.txt
python utf8_cp1252.py temp_utf8.txt temp_cp1252_cp1252.txt
diff temp_cp1252.txt temp_cp1252_cp1252.txt

python cologne_thomas.py cologne ea_ap57_other.txt ea_ap57_other_thomas.txt
python cologne_thomas.py thomas ea_ap57_other_thomas.txt ea_ap57_other_cologne.txt

# convert between IAST and 
python ap_transcode.py romanap as ../orig/ap57.txt ap57_as.txt
python ap_transcode.py as romanap  ap57_as.txt ap57_roman.txt

#==========================================================

python ap_transcode.py romanap as ../changes/ap57_13.txt ap57_13_as.txt
python cologne_thomas.py cologne ap57_13_as.txt ap57_13_as_cp1252.txt
# ap57_13_as_cp1252.txt is in the form that Thomas likes.
## now invert
python cologne_thomas.py thomas ap57_13_as_cp1252.txt ap57_13_as_cp1252_as.txt
python ap_transcode.py as romanap ap57_13_as_cp1252_as.txt ap57_13_as_cp1252_as_roman.txt


diff ../changes/ap57_13.txt ap57_13_as_cp1252_as_roman.txt
[NO DIFF!]

#==========================================================
python ap_transcode.py romanap as ../orig/ap90.txt ap90_as.txt
python cologne_thomas.py cologne ap90_as.txt ap90_as_cp1252.txt
# ap90_as_cp1252.txt is in the form that Thomas likes.
## now invert
python cologne_thomas.py thomas ap90_as_cp1252.txt ap90_as_cp1252_as.txt
python ap_transcode.py as romanap ap90_as_cp1252_as.txt ap90_as_cp1252_as_roman.txt


diff ../changes/ap90.txt ap90_as_cp1252_as_roman.txt
[NO DIFF!]


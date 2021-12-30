step3e

Refer https://github.com/funderburkjim/boesp-prep/issues/43.

Start with a copy of step0/boesp_utf8.xml at commit
  ef22c7e9ed57347b215751b739947486044804d8
git show ef22c7e:step0/boesp_utf8.xml > temp_boesp_utf8.xml

sanchars.py provides frequency count of characters within <s>X</s> markup.
These SHOULD be legitimate characters for the HK transliteration.
We check for other such characters, and edit those that might
cause a problem in transcoding to slp1.
This involves an editing of our temp_boesp_utf8.xml, which we do in a copy:
cp temp_boesp_utf8.xml temp_boesp_utf8_01.xml

1 instance of kaLA (<F n="1713">).  Use same slp1 L
python sanchars.py hk temp_boesp_utf8_01.xml temp_sanchars_utf8.txt

MM (hk) == ~  (slp1) == candrabindu (deva)   Also ~ in iast (roman)
degree sign ° (hk)  == °  (slp1) == laghava  (deva)  Also ° in iast.

python transcode.py hk slp1 temp_boesp_utf8_01.xml temp_boesp_slp1.xml
# Check for invertibility
python transcode.py slp1 hk temp_boesp_slp1.xml temp_boesp_hk.xml
diff temp_boesp_utf8_01.xml temp_boesp_hk.xml
  -- no difference, as expected

# get character frequency for slp1
python sanchars.py slp1 temp_boesp_slp1.xml sanchars_slp1.txt

Observation:
 In temp_sanchars_utf8.txt, 'z 14080'
 In sanchars_slp1.txt, 'S 14004'
 Since 'z' in HK is 'S' in slp1, why the difference?
 compchars.py written to investigate:
 python compchars.py z S temp_boesp_utf8.xml temp_boesp_slp1.xml compchars.txt

 Found the problem was in using 're.DOTALL' in re.sub. After correction,
 'S 14080' in sanchars_slp1.txt.

# -------------------------------------------------------------
# transcode slp1 to iast
python transcode.py slp1 roman temp_boesp_slp1.xml temp_boesp_iast.xml
# Check for invertibility
python transcode.py roman slp1 temp_boesp_iast.xml temp.xml
diff temp_boesp_slp1.xml temp.xml
  -- no difference, as expected

# get character frequency for iast
python sanchars.py roman temp_boesp_iast.xml sanchars_iast.txt

# -------------------------------------------------------------
# transcode slp1 to deva
python transcode.py slp1 deva temp_boesp_slp1.xml temp_boesp_deva.xml
# Check for invertibility
python transcode.py deva slp1 temp_boesp_deva.xml temp.xml
diff temp_boesp_slp1.xml temp.xml
  -- no difference, as expected

# get character frequency for deva
python sanchars.py deva temp_boesp_deva.xml sanchars_deva.txt

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

# -------------------------------------------------------------
# revise temp_boesp.dtd
Change attribute 'n' to required for <S>
Change each verse line from  X to <s>X</s> 
  The 's' element is also used for Sanskrit text elsewhere, such as in footnotes.
Check validation:
python ../step0/xmlvalidate.py temp_boesp_utf8_02.xml temp_boesp.dtd
#--------------------------------------------------------
install revised versions of xml and dtd
cp temp_boesp_slp1.xml ../step0/boesp.xml

# no change in dtd
#cp temp_boesp.dtd ../step0/boesp.dtd



step2
works with all 3 volumes.

The starting point is ../step0/boesp_utf8.txt,

##---------------------------------------------------------
cp ../step0/boesp_utf8.txt boesp_01.txt

python updateByLine.py boesp_utf8.txt change1.txt boesp_1.txt


##---------------------------------------------------------
Find list of extended ASCII.
# redo_ea.sh :
cp ea_boesp.txt tempprev_ea_boesp.txt
python ea.py boesp_01.txt ea_boesp.txt
diff tempprev_ea_boesp.txt ea_boesp.txt

##----------------------------------------
Use of MIDDLE DOT character to demarcate end of (non-empy) lines.
This was a 'trick' developed by Thomas so that his changes using Kedit would
not introduce 'unintentional' changes in lines.


# ------------------------------------------
check D sequence
python checkseq.py D boesp_01.txt checkseq_D.txt

# ------------------------------------------
Check that F and V1,V2,V3 material is placed 
  in correct D-group.
python checkgroup.py boesp_01.txt checkgroup.txt
; -------------------------------------------
# ------------------------------------------------------------------
AS Anglicized Sanskrit checking
This work done in asprep subdirectory

# ------------------------------------------------------------------
# preliminary: temporary xml of hk version
# NOTE: 10-19-2021This is vestigial -- maybe it will be part of workflow later
  
python make_xml.py hk boesp_1.txt work_boesp_hk.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp_hk.xml ../step0/boesp.dtd

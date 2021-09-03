echo "BEGIN step1/redo.sh"
cd ../step1
echo "-----------------------------------"
echo "create work_boesp-1_hk.xml and check validity"
python make_xml.py hk boesp-1_utf8.txt work_boesp-1_hk.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp-1_hk.xml ../step0/boesp.dtd

echo "-----------------------------------"
echo "SLP1 transcoding
echo "-- create work_boesp-1_slp1.txt "
python boesp_transcode.py hk slp1 boesp-1_utf8.txt work_boesp-1_slp1.txt
echo "-- begin check of invertibility"
python boesp_transcode.py slp1 hk work_boesp-1_slp1.txt temp_boesp-1_slp1_utf8.txt
diff boesp-1_utf8.txt  temp_boesp-1_slp1_utf8.txt > tempdiff.txt
wc -l tempdiff.txt
echo "-- end check of invertibility"

echo "-----------------------------------"
echo "Create work_boesp-1_slp1.xml and check validity"
python make_xml.py slp1 work_boesp-1_slp1.txt work_boesp-1_slp1.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp-1_slp1.xml ../step0/boesp.dtd

echo "-----------------------------------"
echo "DEVANAGARI transcoding
echo "-- create work_boesp-1_deva.txt "
python boesp_transcode.py slp1 deva work_boesp-1_slp1.txt work_boesp-1_deva.txt
echo "-- begin check of invertibility"
python boesp_transcode.py deva slp1 work_boesp-1_deva.txt temp_boesp-1_deva_slp1.txt
diff work_boesp-1_slp1.txt  temp_boesp-1_deva_slp1.txt > tempdiff.txt
wc -l tempdiff.txt
echo "-- end check of invertibility"

echo "-----------------------------------"
echo "Create work_boesp-1_deva.xml and check validity"
python make_xml.py deva work_boesp-1_deva.txt work_boesp-1_deva.xml
python /c/xampp/htdocs/cologne/xmlvalidate.py work_boesp-1_deva.xml ../step0/boesp.dtd

echo "END step1/redo.sh"
echo "-----------------------------------------------------------"

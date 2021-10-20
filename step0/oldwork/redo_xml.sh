echo "BEGIN step0/redo_xml.sh"
cd ../step0/
echo "1) recreate boesp-1.xml"
python make_xml.py hk boesp-1_utf8.txt boesp-1.xml
echo "2) validate boesp-1.xml"
python /c/xampp/htdocs/cologne/xmlvalidate.py boesp-1.xml boesp.dtd
echo "END step0/redo_xml.sh"
echo "--------------------------------------------------"

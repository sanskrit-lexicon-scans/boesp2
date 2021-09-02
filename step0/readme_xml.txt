
Conversion of digitization to an xml format, and make a dtd
against which the xml validates.

This should make further processing easier.

python make_xml.py boesp-1_utf8.txt boesp-1.xml
# check against dtd
python /c/xampp/htdocs/cologne/xmlvalidate.py boesp-1.xml boesp.dtd

cp boesp-1_utf8.txt temp_boesp-1a_utf8.txt
Temporary edited file temp_boesp-1a_utf8.txt.
  Manually change temp_boesp-1a_utf8.txt
  
python make_xml.py temp_boesp-1a_utf8.txt boesp-1.xml

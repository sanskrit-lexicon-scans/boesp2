echo "BEGIN transcode_xml.sh in step0"
echo "starting with boesp.xml (slp1 Sanskrit)"
echo "moving to step3e directory"
cd ../step3e
echo "create boesp_hk.xml"
python transcode.py slp1 hk ../step0/boesp.xml ../step0/boesp_hk.xml
echo "create boesp_deva.xml"
python transcode.py slp1 deva ../step0/boesp.xml ../step0/boesp_deva.xml
echo "create boesp_iast.xml"
python transcode.py slp1 roman ../step0/boesp.xml ../step0/boesp_iast.xml
echo "END transcode_xml.sh"

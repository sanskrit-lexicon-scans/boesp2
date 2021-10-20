VOLD=$1
VNEW=$2
cd changes
cmd="python updateByLine.py boesp_${VOLD}.txt change_${VNEW}.txt boesp_${VNEW}.txt"
echo $cmd
$cmd
cp boesp_${VNEW}.txt ../boesp_utf8.txt
cd ../
echo "revising boesp.all_ansi.txt"
python utf8_cp1252.py boesp_utf8.txt boesp.all_ansi.txt

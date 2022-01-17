tranin=$1
tranout=$2
filein="../../step4f/$3"
fileout="../../step4f/$4"
cmd="python transcode1_ab.py $tranin $tranout $filein $fileout"
cd ../step1a/sanproof_1_02
echo $cmd
$cmd
#cd ../../step4a1


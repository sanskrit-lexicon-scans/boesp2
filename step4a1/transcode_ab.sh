tranin=$1
tranout=$2
filein=$3
fileout=$4
cmd="python transcode1_ab.py $tranin $tranout $filein $fileout"
cd ../step1a/sanproof_1_02
echo $cmd
$cmd
cd ../../step4a1


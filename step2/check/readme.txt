step2/check/

# ------------------------------------------
check D sequence
python checkseq.py D ../../step0/boesp_utf8.txt checkseq_D.txt

# ------------------------------------------
Check that F and V1,V2,V3 material is placed  in correct D-group.
Also list all groups.
python checkgroup.py ../../step0/boesp_utf8.txt checkgroup.txt

# check for duplicate verses
Use a version where the formatting of s-verses has been normalized
cp ../slines/temp_boesp_4.txt temp_boesp.txt
python checkdup.py temp_boesp.txt checkdup.txt

python checkdup.py temp_boesp_edit.txt temp_checkdup_edit.txt

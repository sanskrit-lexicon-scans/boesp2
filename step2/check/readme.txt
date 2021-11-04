step2/check/

# ------------------------------------------
check D sequence
python checkseq.py D ../../step0/boesp_utf8.txt checkseq_D.txt

# ------------------------------------------
Check that F and V1,V2,V3 material is placed  in correct D-group.
Also list all groups.
python checkgroup.py ../../step0/boesp_utf8.txt checkgroup.txt

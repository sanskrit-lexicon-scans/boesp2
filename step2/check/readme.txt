step2/check/

# ------------------------------------------
check D sequence
python checkseq.py D ../../step0/boesp_utf8.txt checkseq_D.txt

# ------------------------------------------
Check that F and V1,V2,V3 material is placed  in correct D-group.
Also list all groups.
Include F4.1 and F4.2 in the groups. (11-26-2021)
python checkgroup.py ../../step0/boesp_utf8.txt checkgroup.txt

# check for duplicate verses
python checkdup.py ../../step0/boesp_utf8.txt temp_checkdup_edit.txt
7683 S groups
  28 verses appearing more than once.
Example: Both D418 and D419 have the same FIRST LINE in the verse:
Verse for 418:
<S> api kApuruSo bhIruH syAccennRpatisevakaH |· 
tathApi na parAbhatiM janAdAproti mAnavaH ||· 
Verse for 419:
<S> api kApuruSo bhIruH syAccennRpatisevakaH |· 
yadAproti phalaM lokAttasyAMzamapi no guNI ||· 


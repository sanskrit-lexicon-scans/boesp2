step4e

move h3 and h4 elements into separate HS entries.


Refer https://github.com/funderburkjim/boesp-prep/issues/39#issuecomment-1008521698

Start with a copy of step0/boesp.xml at commit
  9f08caa756d300ee8a7f5b2bd436232d705a13d7
git show 9f08caa7:step0/boesp.xml > temp_boesp.xml

Copy to temp_boesp_01.xml, where the changes will be made.
cp temp_boesp.xml temp_boesp_01.xml

Make new entries for all the h3, h4 elements (17 new entries).

See h3_h4_entries.txt for the new entries.  These identify which were
previously coded with <h3> and which with <h4>, in case this distinction
is needed later.


install revised version 01 of boesp

cp temp_boesp_01.xml ../step0/boesp.xml
  commit 
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

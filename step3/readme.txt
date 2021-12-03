step3
Make boesp.xml from step0/boesp_utf8.txt
This is similar to the work done in step1/make_xml.py, but logically
independent.
Why? Currently (as in step0/boesp_24.txt), the logic to identify entries
is complex:  based on groups of non-blank lines separated by groups of blank lines.  The page number to assign to a particular entry or group within the entry is inaccurate in many cases.  There is no ready way to check the validity of the markup.  There are some entries with multiple Spruch, and there is no identification of the different spruch (See D67,D68,D69). There is some rarely occuring markup (<Poem>, <lg>, <l>,<h3>)
We also want to have a reliable way to insert Proofread Sanskrit Spruch.
Also, want to incorporate Greek text and want to develop an html application.

If we use valid xml markup and develop a dtd, then the structure can be checked.

We'll try to do this in an 'invertible' way, so that boesp_utf8.txt can be
(except for blank lines) be reconstructed from boesp.xml.

We will begin with the 'hk' version, and call result temp_boesp_hk.xml.

There will be transcoding conversion, and boesp.xml will refer to the slp1
version.

Work with a temporary copy of current boesp_utf8.txt -- Anticipate
some changes to this non-xml version in order to end with valid xml.
cp ../step0/changes/boesp_24.txt temp_boesp_00.txt
# After these changes
Manual revisions made to temp_boesp_00.txt.
Result is step0/changes/boesp_25.txt.
cp
python make_xml.py temp_boesp_00.txt temp_boesp_hk.xml
# next uses LXML python to validate
python xmlvalidate.py temp_boesp_hk.xml boesp.dtd

python xml_invert.py temp_boesp_hk.xml temp_xml_boesp.txt
# diff, but after removing blank lines
sed '/^ *$/d' temp_boesp_00.txt > temp_boesp_00_noblank.txt
sed '/^ *$/d' temp_xml_boesp.txt  > temp_xml_boesp_noblank.txt
# Then do a diff ignoring white-space differences
diff -w temp_boesp_00_noblank.txt temp_xml_boesp_noblank.txt > tempdiff.txt
wc -l tempdiff.txt
16 lines

tempdiff -- differences not material
1,3d0
< <H> Boehtlingk, Indische Sprüche, Vol.· 
< 1-3, 2. Auflage, St. Petersburg 1870· 
< [Seite1.1]
17474c17471
< <H>Räthsel.· 
---
> <!-- <H>Räthsel. -->· 
17486c17483
< <H>Auflösung.· 
---
> <!-- <H>Auflösung. -->· 
92722c92719
< <H>Nachträge.· 
---
> <!-- <H>Nachträge. -->· 

#--------------------------------------------------------
install temp_boesp_hk.xml
cp temp_boesp_hk.xml ../step0/boesp_utf8.xml
mv boesp.dtd ../step0/

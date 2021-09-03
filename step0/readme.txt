#  Boehtlingk, Indische Sprüche

##---------------------------------------------------------
# convert from cp1252 encoding (Thomas uses this with Kedit)
# to utf8.

python cp1252_utf8.py boesp-1_ansi.txt boesp-1_utf8.txt
# check for invertibility
python utf8_cp1252.py boesp-1_utf8.txt boesp-1_utf8_cp1252.txt
diff -w boesp-1_ansi.txt boesp-1_utf8_cp1252.txt
# No difference  (the -w) ignores differences in line-endings.
# The utf8 version has Unix line-endings.
# remove unneeded file
rm boesp-1_utf8_cp1252.txt

##---------------------------------------------------------
getting previous version of a file  (using commit)
git show a448aa03a4da110b2c3bed0f8e050d7cbb3b9608:step0/boesp-1_ansi.txt > temp.txt

##---------------------------------------------------------
Find list of extended ASCII.
python ea.py boesp-1_utf8.txt temp_ea_boesp-1.txt
See readme_ea.txt

##---------------------------------------------------------
NOTE: redo_xml.sh does these 2 steps
convert to xml, and make a dtd.
python make_xml.py hk boesp-1_utf8.txt boesp-1.xml
# check against dtd
python /c/xampp/htdocs/cologne/xmlvalidate.py boesp-1.xml boesp.dtd

See readme_xml.txt for discussion

##------------------------------------------------------------
Following notes are from earlier work. No longer actively used
#---- identify sections
examine them first
python section1.py boesp-1_utf8.txt section1.txt
End of 'header' section is first blank line after <H>
section markers:
<S>  Sanskrit Devanagari transcoded as HK.
     Extends until an ending blank line.
      Usually 
     2169
D-section extends until
<DX><AY> 1559   X is current sequence number;
                Y is sequence number of first edition.
<D1396><D1397><A3833><A3834>  1 of this type		

<F>   Foootnote.  Optional
##---------------------------------------------------------
Transcode boesp to slp1.
# there are 4 parts to transcode:
1) <S> sections  (note we skip the <S> item at beg of file)
2) {#X#}
3) {#X    no closing #}
4) X#}    no opening {#
All these assumed to be standard hk transcoding

python boesp_transcode.py hk slp1 boesp-1_utf8.txt boesp-1.txt

##---------------------------------------------------------
 REST IS NOT CURRENT
##---------------------------------------------------------
##---------------------------------------------------------

For background, refer readme_ancillary.txt

This file describes the production steps.

##---------------------------------------------------------
 production steps
 Executive summary:
 1) sh redo1.sh
 2) sh redo_kedit.sh
##---------------------------------------------------------

#=======================================================================
input data files used by redo1.sh:
../orig/ap57.txt
../orig/ap90.txt
../changes/ap57_90_tooltip.txt

#=======================================================================
redo1.sh
# Generates utf8  files, that will be transcoded for Thomas
echo "Recreate merged list of headwords"
cd ../hwcomp
python hwmerge.py ../orig/ap57.txt ../orig/ap90.txt hwmerge.txt

echo "Minor reformatting of ap90"
cd ../step1
python ap90_v1.py txt ../orig/ap90.txt ap90_v1.txt
echo "Minor reformatting of ap57"
python ap57_v1.py txt ../orig/ap57.txt ap57_v1.txt

echo "headword-aligned version  of ap90"
cd ../step2
python extract.py ap90 ../hwcomp/hwmerge.txt ../step1/ap90_v1.txt ap90_v2.txt
echo "headword-aligned version  of ap57"
python extract.py ap57 ../hwcomp/hwmerge.txt ../step1/ap57_v1.txt ap57_v2.txt

echo "step2/lscomp"
python lscomp.py ../hwcomp/hwmerge.txt ../step1/ap90_v1.txt ../step1/ap57_v1.txt lscomp.txt

echo "step2/lscomp_filter"
python lscomp_filter.py ../hwcomp/hwmerge.txt ../step1/ap90_v1.txt ../step1/ap57_v1.txt lscomp_filter.txt


echo "count of literary sources"
cd ../changes
python lscount_comp.py ../orig/ap57.txt ../orig/ap90.txt ap57_90_tooltip.txt lscount_comp.txt

echo "copying ap57_90_tooltip and lscount_com to abbrev, for convenience"
cp ap57_90_tooltip.txt ../abbrev/
cp lscount_comp.txt ../abbrev/


#=======================================================================
Create kedit versions:
#=======================================================================
Script redo_kedit.sh does these creations of files in kedit directory.
sh redo_kedit.sh

These steps are done manually, one at a time.


sh utf8_kedit_hwmerge.sh ../hwcomp/hwmerge.txt ../kedit/hwmerge_kedit.txt
sh utf8_kedit_general.sh ../changes/lscount_comp.txt ../kedit/lscount_comp_kedit.txt

sh utf8_kedit_dict.sh ../step2/ap57_v2.txt ../kedit/ap57_v2_kedit.txt
sh utf8_kedit_dict.sh ../step2/ap90_v2.txt ../kedit/ap90_v2_kedit.txt

sh utf8_kedit_lscomp.sh  ../step2/lscomp.txt ../kedit/lscomp_kedit.txt
sh utf8_kedit_lscomp.sh  ../step2/lscomp_filter.txt ../kedit/lscomp_filter_kedit.txt

# ---------------------------------
# Use a temporary subdirectory tempinvert.
mkdir tempinvert # if necessary

Restore utf8 versions
sh kedit_utf8_hwmerge.sh ../kedit/hwmerge_kedit.txt tempinvert/hwmerge.txt
sh kedit_utf8_general.sh ../kedit/lscount_comp_kedit.txt tempinvert/lscount_comp.txt

sh kedit_utf8_dict.sh ../kedit/ap57_v2_kedit.txt tempinvert/ap57_v2.txt
sh kedit_utf8_dict.sh ../kedit/ap90_v2_kedit.txt tempinvert/ap90_v2.txt



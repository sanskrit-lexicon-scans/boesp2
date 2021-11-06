step2/slines/

# create change transactions for the '<S>' lines.
The first step does NOT take into account the 'long' lines.
Example:
--------------------
OLD:
<S> aMzo 'pi duSTadiSTAnAM pareSAM· 
syAdvinAzakRt | vAlalezo 'pi vyAghrANAM· 
patsyAjjIvitahAnaye ||· 
NEW:
<S>
aMzo 'pi duSTadiSTAnAM pareSAM syAdvinAzakRt |·
vAlalezo 'pi vyAghrANAM patsyAjjIvitahAnaye ||· 
--------------------

Assume that the lines end with middle dot + space
NOTE: We want to compute temp_boesp_4.txt, which also handles the @-sign issue.
And we want to be able to do this later.
We expect the end result to have same number of lines as boesp_utf8.txt.

cp ../../step0/boesp_utf8.txt temp_boesp_0.txt
python change_s.py temp_boesp_0.txt temp_change1.txt

python ../updateByLine.py temp_boesp_0.txt temp_change1.txt temp_boesp_1.txt

# handle long lines.
# work_san_hk_atsign.txt  (in step1) has sanskrit verses from volume 1
#  with lines that need to be displayed as 4 lines rather than 2.
# Such a long line is shown as 'X @ Y'  to indicate the point of split.
# The match_atsign program generates change transactions that
# Change each corresponding line of boesp_1 with this @-sign form.

# change2_orig.txt
# For this matching to work, several minor changes need to be made in
# temp_boesp_1.txt. Namely, line breaks sometimes occur after a '-',
#   and these are absent in temp_boesp_1.txt
#Since change2_orig is manual, it is sensitive to the line-numbering in temp_boesp_1.
#Try to remove this sensitivity by renumbering.  Assuming the text has not changed
#in the <S> records, this should work
python change2_renum.py change2_orig.txt temp_boesp_1.txt change2.txt

python ../updateByLine.py temp_boesp_1.txt change2.txt temp_boesp_2.txt
   
python match_atsign.py temp_boesp_2.txt work_san_hk_atsign.txt temp_change3.txt

python ../updateByLine.py temp_boesp_2.txt temp_change3.txt temp_boesp_3.txt

# change_4
#Now split the <S> lines which have @.
python split_atsign.py temp_boesp_3.txt temp_change4.txt

python ../updateByLine.py temp_boesp_3.txt temp_change4.txt temp_boesp_4.txt

# We should now be able to put all the changes into one file: temp_changes_0_4.txt.
python diff_to_changes.py temp_boesp_0.txt temp_boesp_4.txt temp_changes_0_4.txt
#  27187 changes
#
python ../updateByLine.py temp_boesp_0.txt temp_changes_0_4.txt temp.txt
# Now temp == temp_boesp_4.txt
diff temp_boesp_4.txt temp.txt | wc -l
# 0 (no difference).

## now we could (for appropriate YY)
# cp temp_changes_0_4.txt ../../step0/changes/change_YY.txt
# and in step0,
# sh install.sh XX YY
cp temp_changes_0_4.txt ../../step0/changes/change_10.txt


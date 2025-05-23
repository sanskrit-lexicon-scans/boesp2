step4d

Misc. corrections


Refer https://github.com/funderburkjim/boesp-prep/issues/45#issuecomment-1006366284

Start with a copy of step0/boesp.xml at commit
  c30e186b73cc3bc7e2bbfb2bc12f82f3bca13343
git show c30e186:step0/boesp.xml > temp_boesp.xml


# -------------------------------------------------------------
# temp_boesp_deva_AB.txt
This is copy provided by Andhrabharati at comment:
 https://github.com/funderburkjim/boesp-prep/issues/45#issuecomment-1006769350
One detail: it has 1 fewer lines:
 wc -l temp_*
  184321 temp_boesp.xml
  184320 temp_boesp_deva.AB.txt

# -------------------------------------------------------------
temp_boesp_01.xml
The difference is that lines 98824-5 of temp_boesp.xml have been merged
into one line in temp_boesp_deva_AB.txt (along with correction).
This is fine, but causes technical difficulties.  The remedy is to make
the similar merge (of uncorrected lines) in temp_boesp.xml.  The result is
temp_boesp_01.xml.
# -------------------------------------------------------------
temp_boesp.AB.xml
Convert temp_boesp_deva.AB.txt to slp1.
This can be done as in step0/transcode_xml.sh
sh convert_ab.sh :

# -------------------------------------------------------------
change_AB.txt
Since temp_boesp_01.xml and temp_boesp.AB.xml have the same
number of lines, we can generate a file containing the lines changed.
python ../step0/changes/diff_to_changes.py temp_boesp_01.xml temp_boesp.AB.xml change_AB.txt
2889 changes written to change_AB.txt

# -------------------------------------------------------------
temp_boesp_02.xml 
2186 of AB changes lines are due to changing two consecutive spaces to a single space

python ../step0/changes/diff_to_changes.py temp_boesp_02.xml temp_boesp.AB.xml temp_change_02_AB.txt

714 changes

# -------------------------------------------------------------
temp_boesp_03.xml 
AB version removes space(s) at end of lines.
269 lines changed
python ../step0/changes/diff_to_changes.py temp_boesp_03.xml temp_boesp.AB.xml temp_change_03_AB.txt
 445 lines changed

# -------------------------------------------------------------
temp_boesp_04.xml 
1. AB version removes space before right-paren 
 33 lines changed
2. ',</s>' -> '</s>,'
 14 lines changed
3. '</s></footnote>' ->'</s> </footnote>'
 7 lines changed
4. 'Bomb ' -> 'Bomb. '
 6 lines changed
5. 'd.i.' -> 'd. i.'
 3 lines changed
6. 'LA.(' -> 'LA. ('
 15 lines changed
7. ' ;' -> ';'
 20 lines changed
8. ' :' -> ':'
 4 lines changed
9. ';</s>' -> '</s>;'
 8 lines changed
10. '([a-zA-Z])=([a-zA-Z])' -> '\1 = \2'  (regex)
 12 lines changed
11. 'TeluguCharr' -> 'Telugu-Charr'
 13 lines changed
12. 'u.s.w.' -> 'u. s. w.'
 19 lines changed.
13. ':<' -> ': <'
 7 lines changed
14. '=([a-zA-Z])' -> '= \1'  (regex)
 14 lines changed
15. '.=' -> '. ='
 2 lines changed
16. 'v.a.' -> 'v. a.'
 4 lines
 
python ../step0/changes/diff_to_changes.py temp_boesp_04.xml temp_boesp.AB.xml temp_change_04_AB.txt
 287
# -------------------------------------------------------------
change_05.txt   These are the remaining changes made.
 Note: I comment out the 12 '<ls>X</ls>' markups.  
Check validation:
python ../step0/changes/updateByLine.py temp_boesp_04.xml change_05.txt temp_boesp_05.xml

python ../step0/changes/diff_to_changes.py temp_boesp_05.xml temp_boesp.AB.xml change_not_made.txt

In line 50226, greek text. Moved <pb n="1.412"/> outside of <g>X</g>.


python ../step0/xmlvalidate.py temp_boesp_05.xml ../step0/boesp.dtd
install revised version 05 of boesp

cp temp_boesp_05.xml ../step0/boesp.xml
  commit 
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
# -------------------------------------------------------------
temp_boesp_06.xml:
 Vol. 3 'LONG' S lines reformat  (about 415)
 4654, 4657, 4662, 4663, 4675,
 4680, 4691, 4711, 4715, 4734,
 4753, 4758, 4771, 4772, 4775,
 4781, 4785, 4786, 4787, 4790,
 4807, 4812, 4813, 4816, 4824,
 4825, 4829, 4831, 4840, 4853,
 4859, 4860, 4863, 4873, 4876,
 4878, 4890, 4893, 4896, 4898,
 4910, 4921, 4952, 4963, 4973,
 4978, 4982, 4987*, 4990, 5023,
 5033, 5046, 5050, 5077, 5083,
 5104, 5107, 5133, 5179, 5188,
 5190*, 5193, 5194, 5197, 5202,
 5203, 5206, 5209, 5212, 5231,
 5238, 5247, 5249, 5255, 5256,
 5257, 5267, 5292, 5295, 5302,
 5304, 5308, 5336!, 5343, 5426,
 5435!, 5437, 5438, 5439, 5440,
 5440, 5464, 5466, 5468, 5479,
 5497, 5499, 5539, 5540, 5543,
 5547, 5553, 5554, 5555, 5560,
 5561, 5562, 5563, 5567, 5569,
 5576, 5579, 5581, 5585, 5610,
 5612, 5691, 5693, 5708, 5712,
 5713, 5714, 5715, 5716, 5717,
 5728, 5733, 5739, 5740, 5756,
 5773, 5777, 5778, 5780, 5782,
 5783, 5784, 5789, 5793, 5798,
 5799, 5800, 5801, 5802, 5815,
 5817, 5822, 5824, 5826, 5827,
 5828, 5837, 5844, 5845, 5850,
 5852, 5855, 5875, 5881, 5888,
 5889, 5896, 5897, 5904, 5910,
 5929, 5936, 5939, 5941, 5949,
 5951, 5953, 5954, 5960, 5967,
 5968, 5969, 5972, 5976, 5981,
 5994, 6004, 6005, 6012, 6014,
 6031, 6032, 6033, 6035, 6036,
 6038, 6039, 6043, 6044, 6048,
 6049, 6052, 6066, 6067, 6068,
 6071, 6073, 6077, 6086, 6088,
 6089, 6095, 6110, 6117, 6128,
 6139, 6145, 6147, 6148, 6154,
 6155, 6157, 6164, 6171, 6173,
 6174, 6176, 6184, 6190, 6193,
 6204, 6211, 6221, 6230, 6231,
 6234, 6237, 6238, 6240, 6246,
 6253, 6267, 6275, 6284, 6288,
 6305, 6312, 6322, 6323, 6330,
 6331, 6332, 6336, 6345, 6348,
 6353, 6357, 6359, 6404, 6408,
 6410, 6411, 6423, 6430, 6432,
 6434, 6437, 6440, 6443, 6444,
 6445, 6452, 6455, 6456, 6468,
 6471, 6479, 6486, 6495, 6505,
 6508, 6518, 6519, 6522, 6538,
 6542, 6554, 6562, 6569, 6571,
 6574, 6587, 6588, 6591, 6599,
 6627, 6641, 6642, 6648, 6668,
 6673, 6680, 6694, 6704, 6710,
 6717, 6723, 6729, 6739, 6747,
 6759, 6781, 6783, 6789, 6803,
 6804, 6818, 6824, 6849, 6850,
 6854, 6855, 6858, 6887, 6893,
 6896, 6897, 6903, 6964, 6966
 6977, 6997, 6998, 7001, 7002,
 7017, 7022, 7023, 7025, 7028,
 7030, 7031, 7036, 7038, 7044,
 7045, 7047, 7049, 7050, 7057,
 7067, 7082, 7089*, 7097, 7100,
 7102, 7105, 7106, 7110, 7127,
 7142, 7152, 7154, 7160, 7163,
 7178, 7186, 7187, 7199, 7200,
 7205, 7226, 7228, 7231, 7233,
 7238, 7239, 7242, 7247, 7252,
 7253, 7254, 7260, 7261, 7263,
 7272, 7283, 7316, 7317, 7322,
 7328, 7330, 7336, 7337, 7347,
 7356, 7359, 7360, 7368, 7371,
 7380, 7382, 7385, 7388, 7414,
 7415, 7417, 7419, 7420, 7423,
 7497, 7500, 7506, 7508, 7509,
 7527, 7551, 7580, 7607, 7610,
 
* Previously formatted properly
! 3 lines, different
Install as commit
cp temp_boesp_06.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
This results in boesp.xml at commit de93d5502bed9af0871e9f1bc858d4757e0cd6b0.
# -------------------------------------------------------------
temp_boesp_07.xml
Further revise to shorten line length in long greek text.
There are about 100 such identfied.
Install as commit:
cp temp_boesp_07.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit
This results in boesp.xml at commit [commit hash to fill in later]
#-------------------------------------------------------------
temp_boesp_deva.AB._1.txt copied from boesp_deva.AB._1.txt at
 https://github.com/funderburkjim/boesp-prep/issues/43#issuecomment-1008294756

temp_boesp.AB._1.xml
Convert temp_boesp_deva.AB._1.txt to slp1.
This can be done as in step0/transcode_xml.sh
sh temp_convert_ab_1.sh
---
cd ../step3e
python transcode.py deva slp1 ../step4d/temp_boesp_deva.AB._1.txt  ../step4d/temp_boesp.AB._1.xml
===
Now back in step4d.
This has same number of lines (185334) as
  current boesp.xml at commit a244fe721



python ../step0/changes/diff_to_changes.py ../step0/boesp.xml temp_boesp.AB._1.xml temp_changes_boesp.AB_1.txt

837 changes  (this many lines changed)

To analyze these 837 changes, start with a copy temp_boesp_08.xml of
 boesp.xml at commit a244fe721, and make successive changes as noticed from
 temp_changes_boesp.AB_1.txt
11 '<g> ' -> '<g>'
649 ' </s>$' -> '</s>'  (regex replacement)
2  ' </s> ' -> '</s> '
34 lines:  Insert space before avagraha in sanskrit text
13 : F -> f in Sanskrit text (slp1 spelling)
3 : f1 -> f in Sanskrit text (slp1 spelling)
11 : 'h ' -> 'H '  (visarga in Sanskrit text, slp1 spelling)
12 : Missing '-' at end of Sanskrit text in a 'long' line

103 remaining changes put into change_09.txt

There is one change that is problematic
;-----------------
158357 old <s>samsAravizavfkzasya dve Pale amftopame .</s>
158357 new ; line repeated
REASON:  The '; line repeated' line violates the DTD for <S> elements.

To deal with this properly, 
First, we comment out the 158357 change from change_09.txt (manually)
Then construct temp_boesp_09.xml
python ../step0/changes/updateByLine.py temp_boesp_08.xml change_09.txt temp_boesp_09.xml

diff temp_boesp.AB._1.xml temp_boesp_09.xml
Now temp_boesp_09.xml is same as temp_boesp.AB._1.xml, except for
1) the version in first line  (which should be 1.4).
2) the presence of the '; line repeated'

Next,
cp temp_boesp_09.xml temp_boesp_10.xml
Manually delete line 158357 from temp_boesp_10.xml
Also, manually: (95240) may be corrected as Fuss ᴗᴗᴗ–! from Fuss {?!}.

Now, install temp_boesp_10.xml as new version of boesp.xml

cp temp_boesp_10.xml ../step0/boesp.xml
remake hk, deva, and slp1 versions of step0/boesp.xml
cd ../step0
sh transcode_xml.sh
add and commit

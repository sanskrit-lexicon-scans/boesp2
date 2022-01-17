web0


Generate html link target(s) for boesp.xml

Refer https://github.com/funderburkjim/boesp-prep/issues/?

Input file step0/boesp.xml 

# put output files in current directory (./)
#python make_html.py ../step0/boesp.xml .

(start with sanskrit-lexicon/rvlinks approach)

python make_html.py ../step0/boesp_deva.xml .

Convert the xml into 4 html files (for volumes 1,2,3, and a 4th for
supplements).
In each html file, there is, for each verse, an anchor such as
<a id='verse1681.1'/>.  Then url ending "/section1.html#1681.1" will
scroll to the verse.
A program wanting to link to a verse will need to know
the section (1,2,3, or 4) that contains the verse.
 
section 1 has 2499 entries from 1 to 2219
section 2 has 2800 entries from 2220 to 4649
section 3 has 3520 entries from 4650 to 7613
section 4 has 282 entries from 7614 to 7878

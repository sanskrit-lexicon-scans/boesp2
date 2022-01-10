
Guide to directories:

greektext - Greek unicode to be integrated into boesp

step0 - Original digitizations from Thomas.
 changes  A log of changes to boesp_utf8.txt (pre-xml form)
 xmlchanges Changes to boesp_utf8.xml  (incomplete)

step1 - prepare Sanskrit in <S>, <HS> sections for proofreading in
        SLP1 and Devanagari. Based on non-xml form of volume 1
        Generates a preliminary xml version of volume 1
        
step1a - continuation of step1

step2 - Various checks and changes on pre-xml version 
  asprep   AS (letter-number) coded words. (pre-xml)
  check    Several internal consistency checks
  slines   Generate 'proper' line breaks in the <S> sections

step3 - First xml version based on all 3 volumes of boesp, with provision
  for the 2 'extra' volumes.  Basis of step0/boesp_utf8.xml.
  Also, has a dtd

step3a - Revise xml entries to have <HS> groups in separate entries.

step3b - Remove FDUMMY groups from xml

step3c - Remove lg, l markdup

step3d - Add n attribute for <S>.
         Also, multiple <S> when multiple <D>
         Also, in <S> groups, add <s>X</s> markup.
            Now everywhere, <s>X</s> indicates Sanskrit text.
         Make <S> definition in boesp.dtd more specific:
            a sequence of one or more 's' elements, 
            with an optional 'pb' element at the end
step3e - Transcoding of Sanskrit text.
         step0/boesp.xml will be the 'base' form, in slp1 transcoding.
         Other forms will be boesp_hk.xml, boesp_deva.xml, boesp_iast.xml.
         boesp.dtd is not changed.
step4a - Insert corrected Sanskrit for volume 1 verses into boesp.xml
step4a1 - Sanskrit text for volume 2 verses
step4b - Transcode AS to IAST.
step4c - Insert Greektext into boesp.xml
step4d - Misc corrections mentioned in issue 45, starting at
         https://github.com/funderburkjim/boesp-prep/issues/45#issuecomment-1006366284

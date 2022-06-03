"""unixify_ansi.py  Convert all line endings to '\n'
   
"""
import sys,re,codecs

if __name__ == "__main__":
 filename = sys.argv[1]
 fileout = sys.argv[2]
 with codecs.open(filename,"r","cp1252") as f:
  lines = [x.rstrip('\r\n') for x in f]
 with codecs.open(fileout,"w","cp1252") as f:
  for line in lines:
   f.write(line + '\n')


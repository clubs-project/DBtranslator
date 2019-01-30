#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Joins the translated sentences of an abstract in a format prepared
    to be uploaded into PubPshyc 
    Date: 29.12.2017
    Author: cristinae
"""

import sys

def main(inF, outF):

    fOUT = open(outF, 'w')
    with open(inF) as f:
       id = 'empty'
       text = ''
       for line in f:
           line = line.strip()
           fields = line.split('>\t')
           #print(fields)
           if (fields[0] == id):
              text = text + " " + fields[1]
           else:
              if text:
                 fOUT.write(text+"\n")
              id = fields[0]
              text = line
       fOUT.write(text+"\n")
    fOUT.close()   


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


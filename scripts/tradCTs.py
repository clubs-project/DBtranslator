#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Translates the controlled terms previously extracted with preproField4trad.py.
    MeSH and/or Wikipedia quad-lexicons are used 
    Date: 02.01.2018
    Author: cristinae
"""

import sys
import os.path

ctPath = "../model/CT/"

def main(inF, outF):

    language = os.path.splitext(inF)[1]
    ctFile = ctPath + "mesh."+language+"key.txt"

    # Load the MeSH lexicon
    ctDict = {}
    for line in open(ctFile):
        source, targets = line.split("|||")
        ctDict[name] = int(score)

    # Read the CTs from file
    fOUT = open(outF, 'w')
    with open(inF) as f:
       id = 'empty'
       text = ''
       for line in f:
           line = line.strip()
           fields = line.split('\t')
           # eliminate the list format. Is there a better way?
           terms = fields[1].replace("[","")
           terms = terms.replace("]","")
           terms = terms.replace("'","")
           termsArray = terms.split(",")
           for term in termsArray:
               term = term.replace(")","")
               ct, area = term.split("(")
               


       fOUT.write(text+"\n")
    fOUT.close()   


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


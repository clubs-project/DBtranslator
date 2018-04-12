#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Processes a file to lowercase it and remove diacritics
    Date: 11.04.2018
    Author: cristinae
"""

import sys
import unicodedata

def remove_diacritic(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    #main(sys.argv[1], sys.argv[2])

    # Read from file
    fOUT = open(sys.argv[2], 'w')
    with open(sys.argv[1]) as f:
       for line in f:
           line = line.strip()
           line = line.lower()
           line = remove_diacritic(line).decode()
           fOUT.write(line+"\n")
    fOUT.close()   


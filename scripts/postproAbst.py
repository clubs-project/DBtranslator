#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Joins the translated sentences of an abstract in a format prepared
    to be uploaded into PubPshyc 
    Date: 29.12.2017
    Author: cristinae
"""

def main(inF, outF):



if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


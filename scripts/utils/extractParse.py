#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Extracts translatable terms from Solr parses in an adequate format for its translation
    with our multilingual lexicons
    Date: 05.04.2018
    Author: cristinae
"""

import sys
import re

def cleanParsingMarks(line):
    line = line.replace("+\(","(")
    line = line.replace("-\(","(")
    line = line.replace("*:*","")
    line = re.sub('\^\d.\d', '', line) # this pattern appear after parsing of negations?
    # what do we want to do with wildcards?
    line = line.replace("*","") # we cannot translate wildcards symbols
    line = re.sub('\w\?\w', '', line) # we don't want terms with '?'
    return line

def removeFields(line):
#    AGE (age group)	EV (evidence level)	PLOC (origin of population)
#    AU (person(s))	ISBN	PU (publisher)
#    CM (method type)	ISSN	PY (publication year)
#    COU (country of origin)	IT (additional descriptor)	SEG (database segment)
#    CS (author affiliation)	JT (journal title)	SH (subject classification)
#    CT (controlled term)	KP (key phrase)	SW (all keywords)
#    DB (data source)	LA (publication language)	TI (title)
# In data but not in webpage
#    AB, DT, ID, DOI, DFK

    labelsAll = ["AGE","EV","PLOC","AU","ISBN","ISSN","PU","CM","PY","COU","IT","SEG","CS","JT","SH","CT","KP","SW","DB","LA","TI","AB","ID","DT","DOI","DFK"]
    # PY is not in labelsRemove because it needs additional info
    labelsRemove = ["AGE","EV","PLOC","AU","COU","ISBN","ISBNO","ISSN","PU","SEG","CS","JT","DB","LA","DT","ID","DOI","DFK"]
    # labelsTrad = ["CM","IT","SH","CT","KP","SW","TI","AB"]
    
    for label in labelsRemove:
        line = re.sub("-*"+label+":\w+", "", line)
        line = re.sub("-*"+label+":\".+?\"", "", line)

    #line = re.sub("PY:.+(?![\}\]])}", "", line) #if it's a range
    #line = re.sub("PY:.+(?![\}\]])]", "", line) #if it's a range
    line = re.sub("PY:\[\d+ TO \*\}", "", line)
    line = re.sub("PY:\{\d+ TO \*\}", "", line)
    line = re.sub("PY:\[\d+ TO \d+\]", "", line)
    line = re.sub("PY:\{\* TO \d+\]", "", line)
    line = re.sub("PY:\{\* TO \d+\}", "", line)
    line = re.sub("PY:\d+", "", line) #ELSE it's a number
    line = re.sub("PY:\"\d+\"", "", line) #ELSE it's a number
    line = re.sub("PY:\[.+", "", line) #ELSE it's a number
    line = re.sub("PY:> \(\d+\)", "", line) 
    line = re.sub("PY:[\"<]\d+", "", line) #ELSE it's a number
    return line


def removeFieldLabels(line):
    # some of them (labelsRemove) are not present because they have been removed before 
    labelsAll = ["AGE","EV","PLOC","AU","ISBN","ISSN","PU","CM","PY","COU","IT","SEG","CS","JT","SH","CT","KP","SW","DB","LA","TI","AB","ID","DT","DOI","DFK"]
    for label in labelsAll:
        line = re.sub("-*"+label+":", "", line)
    return line


def parse(text):
    stack = []
    for char in text:
        if char == '(':
            #stack push
            stack.append([])
        elif char == ')':
            term = ''.join(stack.pop())
            term = re.sub('^\d*$', '', term) #if it's only a number we don't translate it
            if term and not term.isspace():
                yield term
        else:
            #stack peek
            stack[-1].append(char)


def main(inF, outF):

    fOUT = open(outF, 'w')
    with open(inF) as f:
         i=1
         for line in f:
            line = line.strip()
            line = cleanParsingMarks(line)
            # Don't invert the order!
            line = removeFields(line)
            line = removeFieldLabels(line)
            # print(list(parse(line)))
            # tant de casting per compatibilitat amb formats de CTs
            fOUT.write("Q"+str(i)+"\t"+str(list(parse(line)))+"\n")
            i=i+1
    fOUT.close()   



if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    print("Translating...")
    print(" - Free text plus fields CM, IT, SH, CT, KP, SW, TI and AB")
    print(" - Numbers are not translated")
    print(" - * is removed (only the character)")
    print(" - ? is removed (the full token)")
    main(sys.argv[1], sys.argv[2])


# 553,568 queries, 536,479 after removing queries with only untranslatable fields or numbers

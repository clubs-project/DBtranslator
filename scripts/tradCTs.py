#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Translates the controlled terms previously extracted with preproField4trad.py.
    MeSH+Wikipedia+Manual quad-lexicons are used. Translation at word level is applied if
    the complete CT is not in the dictionary, and the source is used as translation
    in case it is missing
    Date: 02.01.2018
    Author: cristinae
"""

import sys
import os.path

ctPath = "../models/CT/"

numSpecsUntrad=0
numTermsUntrad=0
numTerms=0
numSpecs=0

def rreplace(s, old, new, occurrence):
    """ Replace last occurrence of a substring in a string
    https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


def extractParentheseses(term):
    """ Given a term with possibly specifications between parentheses 
        returns the main term and the specifications in case there are
    """
    term = term.strip()
    ct = ""
    area = []
    # if it has "areas"
    if " (" in term and "((" not in term and "))" not in term and term.endswith(")"):
       term = term.replace(")","")
       area = term.split(" (")
       return area[1:], area[0]
    else:
       return "", term


def translate(string, ctDict, lang):
    """ Translates an input string. If it is not found in the dictionary, the string
        is split into words and translated independently. If it words are not ther
        either, the source is copied
    """

    global numSpecsUntrad
    global numTermsUntrad
    global numTerms
    global numSpecs

    toTrad = ""
    stringTrad = ""
    
    # we check for all the capitalizations
    capitalized = False
    if string.istitle():
       capitalized = True
    if string in ctDict:
       toTrad = string
    elif string.lower() in ctDict:
       toTrad = string.lower()
    elif string.capitalize() in ctDict:
       toTrad = string.capitalize()
 
    if toTrad in ctDict:
       trads = ctDict[toTrad].split("|||")
       #print(trads)
       for trad in trads:
           if trad.startswith(lang):
              translation = trad.replace(lang+":","")
              # recover the source casing in the translation
              if capitalized == True:
                 translation = translation.capitalize()
              else:
                 translation = translation.lower()
              return stringTrad + translation 
    else:
       words = string.split(" ")
       if len(words)==1:
          return stringTrad + words[0]
       for word in words:
          return translate(word, ctDict, lang)


def main(inF, outF):

    global numSpecsUntrad
    global numTermsUntrad
    global numTerms
    global numSpecs

    language = os.path.splitext(inF)[1].replace(".","")
    ctFile = ctPath + "quad."+language+"key.txt"

    if(language=="en"):
       l1="fr"
       l2="de"
       l3="es"
    elif(language=="es"):
       l1="fr"
       l2="de"
       l3="en"
    elif(language=="de"):
       l1="fr"
       l2="es"
       l3="en"
    elif(language=="fr"):
       l1="es"
       l2="de"
       l3="en"


    # Load the lexicon
    ctDict = {}
    targets = []
    for line in open(ctFile):
        line = line.strip()
        source, targets = line.split("|||",1)
        ctDict[source] = targets

    # Read the CTs from file
    fOUT = open(outF, 'w')
    with open(inF) as f:
       id = 'empty'
       text = ''
       for line in f:
           line = line.strip()
           fields = line.split('\t')
           lineTradL1 = fields[0] + "\t<2"+l1+">\t["
           lineTradL2 = fields[0] + "\t<2"+l2+">\t["
           lineTradL3 = fields[0] + "\t<2"+l3+">\t["
           # eliminate the list format. Is there a better way?
           terms = fields[1].replace("[","")
           terms = terms.replace("]","")
           terms = terms.replace("',","")
           termsArray = terms.split("'")
           # split terms in subunits
           for term in termsArray[1:]:
               areas, ct = extractParentheseses(term)
               # translate the subunits
               ctTradL1 = translate(ct, ctDict, l1)
               numTerms += 1
               if ct==ctTradL1:
                  numTermsUntrad += 1
               ctTradL2 = translate(ct, ctDict, l2)
               ctTradL3 = translate(ct, ctDict, l3)
               termTrad1 = "'" + ctTradL1 
               termTrad2 = "'" + ctTradL2 
               termTrad3 = "'" + ctTradL3 
               if areas is not "":
                   for area in areas:
                     areaTrad1 = translate(area, ctDict, l1)
                     termTrad1 = termTrad1 + " ("+areaTrad1+")"
                     areaTrad2 = translate(area, ctDict, l2)
                     termTrad2 = termTrad2 + " ("+areaTrad2+")"
                     areaTrad3 = translate(area, ctDict, l3)
                     termTrad3 = termTrad3 + " ("+areaTrad3+")"
                     numSpecs += 1
                     if area==areaTrad1: 
                        numSpecsUntrad += 1
               lineTradL1 = lineTradL1 + termTrad1 + "', "
               lineTradL2 = lineTradL2 + termTrad2 + "', "
               lineTradL3 = lineTradL3 + termTrad3 + "', "

           #rof termsArray
           lineTradL1 = rreplace(lineTradL1, "', ", "", 2) + "]"
           lineTradL2 = rreplace(lineTradL2, "', ", "", 2) + "]"
           lineTradL3 = rreplace(lineTradL3, "', ", "", 2) + "]"
           fOUT.write(lineTradL1+"\n")
           fOUT.write(lineTradL2+"\n")
           fOUT.write(lineTradL3+"\n")

    # CHECK: source==target doesn't mean untranslated
    #print(str(numSpecsUntrad) + " untranslated specifications out of " + str(numSpecs))
    #print(str(numTermsUntrad) + " untranslated main terms out of " + str(numTerms))
    fOUT.close()   


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


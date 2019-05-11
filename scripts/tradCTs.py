#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Translates the controlled terms previously extracted with preproField4trad.py.
    MeSH+Wikipedia+Apertium+manual+Wikidata quad-lexicons are used. 
    Translation at word level is applied if the complete CT is not in the dictionary, 
    and the source is used as translation in case it is missing
    Date: 02.01.2018
    Author: cristinae
"""

import sys
import os.path
import unicodedata

ctPath = "../models/CT/"

numTermsUntrad = 0
numTerms = 0
numWordsUntrad = 0
numWords = 0

def rreplace(s, old, new, occurrence):
    """ Replace last occurrence of a substring in a string
    https://stackoverflow.com/questions/2556108/rreplace-how-to-replace-the-last-occurrence-of-an-expression-in-a-string
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)

def percentage2d(part, whole):
    if (part != 0):
       value = 100*float(part)/float(whole)
       return "{0:.1f}".format(value)
    else:
       return "0"

def remove_diacritic(input):
    '''
    Accept a unicode string, and return a normal string (bytes in Python 3)
    without any diacritical marks.
    '''
    return unicodedata.normalize('NFKD', input).encode('ASCII', 'ignore')

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

def cleanEndString(toClean):
    """ Removes ',' and '"' from the end of the string
    """
    clean=toClean.replace('Ü', 'ü')
    if len(clean)>1:
       if clean[-1] == ',': 
          clean = clean[:-1]
    if len(clean)>1:
       if clean[-1] == '"': 
          clean = clean[:-1]
    return clean

def removePluralEnding(plural):
    """ Removes -s, -n, -en and -e as plural forms 
    """
    global language
    singular=plural
    # for Spanish
    if len(singular)>1 and language=="es":
       if singular[:-2] == 'es': 
          singular = singular[:-2]
       elif singular[-1] == 's': 
          singular = singular[:-1]
    # for French
    if len(singular)>1 and language=="fr":
       if singular[-1] == 's': 
          singular = singular[:-1]
    # for English
    if len(singular)>3 and language=="en":
       if singular[:-3] == 'ies': 
          return singular[:-3]+"y"
    if len(singular)>2 and language=="en":
       if singular[:-2] == 'es': 
          return singular[:-2]
    if len(singular)>1 and language=="en":
       if singular[-1] == 's': 
          singular = singular[:-1]
    # for German
    if len(singular)>2 and language=="de":
       if singular[:-2] == 'er': 
          return remove_diacritic(singular[:-2]).decode() #we need to remove the umlaut too
       if singular[-1] == 'n': 
          singular = singular[:-1]
    if len(singular)>1 and language=="de":
       if singular[-1] == 'e' or  singular[-1] == 's': 
          singular = singular[:-1]

    return singular

def translate(string, ctDict, lang, complete, plurals, original):
    """ Translates an input string. If it is not found in the dictionary, the string
        is split into words and translated independently. If it words are not ther
        either, the source is copied
    """

    global numTermsUntrad
    global numTerms
    global numWords
    global numWordsUntrad
    global l1 #needed only for counting, so that we do it only once


    toTrad = ""
    stringTrad = ""
    
    string=cleanEndString(string)
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
 
    if (complete and lang==l1):
        numTerms += 1
        words = string.split(" ")
        numWords = numWords + len(words)
    if toTrad in ctDict:
       trads = ctDict[toTrad].split("|||")
       #(trads)
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
       if (complete and lang==l1):
           numTermsUntrad += 1
       words = string.split(" ")
       complete = False
       if len(words)==1 and plurals==True:
          #if (original!='' and lang==l1): print(original) #debug
          if (original!='' and lang==l1): numWordsUntrad += 1
          return stringTrad + original
       if len(words)==1 and plurals==False:
          newWord = removePluralEnding(words[0])
          return translate(newWord, ctDict, lang, complete, True, words[0])
       for word in words:
          return translate(word, ctDict, lang, complete, False, word)


def main(inF, outF):

    global numTermsUntrad
    global numTerms
    global numWords
    global numWordsUntrad
    global language
    global l1

    language = os.path.splitext(inF)[1].replace(".","")
    ctFile = ctPath + "quadLexicon5."+language+"key.txt"
    #ctFile = ctPath + "mesh2."+language+"key.txt"
    print(ctFile)

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
               ctTradL1 = translate(ct, ctDict, l1, True, False, ct)
               #numTerms += 1
               #if ct==ctTradL1:
               #   numTermsUntrad += 1
               ctTradL2 = translate(ct, ctDict, l2, True, False, ct)
               ctTradL3 = translate(ct, ctDict, l3, True, False, ct)
               termTrad1 = "'" + ctTradL1 
               termTrad2 = "'" + ctTradL2 
               termTrad3 = "'" + ctTradL3 
               if areas is not "":
                   for area in areas:
                     areaTrad1 = translate(area, ctDict, l1, True, False, ct)
                     termTrad1 = termTrad1 + " ("+areaTrad1+")"
                     areaTrad2 = translate(area, ctDict, l2, True, False, ct)
                     termTrad2 = termTrad2 + " ("+areaTrad2+")"
                     areaTrad3 = translate(area, ctDict, l3, True, False, ct)
                     termTrad3 = termTrad3 + " ("+areaTrad3+")"
                     #numSpecs += 1
                     #if area==areaTrad1: 
                        #print(area)
                     #   numSpecsUntrad += 1
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

    fOUT.close()   


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s inputFile outputFile\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])

    print(sys.argv[1])
    # CHECK: source==target doesn't mean untranslated
    numTermTrad = numTerms-numTermsUntrad
    numWordTrad = numWords-numWordsUntrad
    # LaTeX friendly, human unfriendly
    print(str(numTermTrad) + " ("+percentage2d(numTermTrad, numTerms)+"\\%) "+" & "+ str(numTermsUntrad) + " ("+percentage2d(numTermsUntrad, numTerms)+"\\%) "+" & "+ str(numWordTrad) + " ("+percentage2d(numWordTrad, numWords)+"\\%) "+" & "+ str(numWordsUntrad) + " ("+percentage2d(numWordsUntrad, numWords)+"\\%) \\\\")
    #print(str(numTermsUntrad) + " untranslated parts, " + str(numTerms) + " total parts")
    #print(str(numWordsUntrad) + " untranslated words " + str(numWords)+ " total words")
 

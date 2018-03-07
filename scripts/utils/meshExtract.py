#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys;
from importlib import reload

reload(sys);
#sys.setdefaultencoding("utf8")

def extractParentheseses(term):
    ''' Given a term with possibly specifications between parentheses 
        returns the main term and the specifications in case there are
    '''
    ct = ""
    area = []
    # if it has "areas"
    if " (" in term and "((" not in term and "))" not in term and term.endswith(")"):
       term = term.replace(")","")
       area = term.split(" (")
       return area[1:], area[0]
    else:
       return "", term


def extractMain(term):
    ''' Given a term with possibly specifications between parentheses 
        returns the main term
    '''
    ct = ""
    area = []
    # if it has "areas"
    if " (" in term and "((" not in term and "))" not in term and term.endswith(")"):
       term = term.replace(")","")
       area = term.split(" (")
       return area[0]
    else:
       return term


def main():

    path = '../models/CT/'
    fileName = path+'MeSH_2017_de+en+fr+es.xml'

    fEN = open(path+'mesh.enkey.txt', 'w')
    fDE = open(path+'mesh.dekey.txt', 'w')
    fES = open(path+'mesh.eskey.txt', 'w')
    fFR = open(path+'mesh.frkey.txt', 'w')

    fENs = open(path+'meshSplit.enkey.txt', 'w')
    fDEs = open(path+'meshSplit.dekey.txt', 'w')
    fESs = open(path+'meshSplit.eskey.txt', 'w')
    fFRs = open(path+'meshSplit.frkey.txt', 'w')

    root = ET.parse(fileName).getroot()    
    for descriptor in root.findall('descriptor'):
        for concept in descriptor.findall('concept'):
            preferredEN = ''
            preferredDE = ''
            preferredES = ''
            preferredFR = ''
            ctEN = ''
            ctDE = ''
            ctES = ''
            ctFR = ''
            areasEN = []
            areasDE = []
            areasES = []
            areasFR = []
            # scan once to get the preferred term per concept
            for term in concept.findall('term'):            
                if term.get('lang')=="eng" and term.get('preferred')=="true":
                   preferredEN = term.find('string').text#.replace(" ", "_")
                   areasEN, ctEN= extractParentheseses(preferredEN)
                if term.get('lang')=="spa" and term.get('preferred')=="true":
                   preferredES = term.find('string').text#.replace(" ", "_")
                   areasES, ctES= extractParentheseses(preferredES)
                if term.get('lang')=="ger" and term.get('preferred')=="true":
                   preferredDE = term.find('string').text#.replace(" ", "_")
                   areasDE, ctDE= extractParentheseses(preferredDE)
                if term.get('lang')=="fre" and term.get('preferred')=="true":
                   preferredFR = term.find('string').text#.replace(" ", "_")
                   areasFR, ctFR= extractParentheseses(preferredFR)
            # we want a quad-lexicon
            if (preferredEN == '' or preferredES == '' or preferredDE == '' or preferredFR == ''):
                break

            str_enesdefr = '|||es:'+ preferredES + '|||de:'+ preferredDE + '|||fr:'+ preferredFR+ '|||ID:'+ concept.get('id')+'\n'
            str_esendefr = '|||en:'+ preferredEN + '|||de:'+ preferredDE + '|||fr:'+ preferredFR+ '|||ID:'+ concept.get('id')+'\n'
            str_deenesfr = '|||en:'+ preferredEN + '|||es:'+ preferredES + '|||fr:'+ preferredFR+ '|||ID:'+ concept.get('id')+'\n'
            str_frenesde = '|||en:'+ preferredEN + '|||es:'+ preferredES + '|||de:'+ preferredDE+ '|||ID:'+ concept.get('id')+'\n'

            # only terms outside parentheses
            strCT_enesdefr = '|||es:'+ ctES + '|||de:'+ ctDE + '|||fr:'+ ctFR+'\n'
            strCT_esendefr = '|||en:'+ ctEN + '|||de:'+ ctDE + '|||fr:'+ ctFR+'\n'
            strCT_deenesfr = '|||en:'+ ctEN + '|||es:'+ ctES + '|||fr:'+ ctFR+'\n'
            strCT_frenesde = '|||en:'+ ctEN + '|||es:'+ ctES + '|||de:'+ ctDE+'\n'
            ct_enesdefr = ctEN + '|||es:'+ ctES + '|||de:'+ ctDE + '|||fr:'+ ctFR+'\n'
            ct_esendefr = ctES + '|||en:'+ ctEN + '|||de:'+ ctDE + '|||fr:'+ ctFR+'\n'
            ct_deenesfr = ctDE + '|||en:'+ ctEN + '|||es:'+ ctES + '|||fr:'+ ctFR+'\n'
            ct_frenesde = ctFR + '|||en:'+ ctEN + '|||es:'+ ctES + '|||de:'+ ctDE+'\n'

            # only terms in parentheses (more than one is possible)
            area_enesdefr = ''
            area_esendefr = ''
            area_deenesfr = ''
            area_frenesde = ''
            if (len(areasEN) == len(areasES) and len(areasES) == len(areasFR) and len(areasFR) == len(areasDE)):
                i=0
                for area in areasEN:
                    area_enesdefr = areasEN[i] + '|||es:'+ areasES[i] + '|||de:'+ areasDE[i] + '|||fr:'+ areasFR[i]+'\n'
                    area_esendefr = areasES[i] + '|||en:'+ areasEN[i] + '|||de:'+ areasDE[i] + '|||fr:'+ areasFR[i]+'\n'
                    area_deenesfr = areasDE[i] + '|||en:'+ areasEN[i] + '|||es:'+ areasES[i] + '|||fr:'+ areasFR[i]+'\n'
                    area_frenesde = areasFR[i] + '|||en:'+ areasEN[i] + '|||es:'+ areasES[i] + '|||de:'+ areasDE[i]+'\n'
                    i+=1

            # Don't know how to avoid the double pass
            # write for each term the preferred term in the other languages
            for term in concept.findall('term'):
                if term.get('lang')=="eng":
                   enStr = term.find('string').text
                   fEN.write(enStr + str_enesdefr)
                   fENs.write(extractMain(enStr) + strCT_enesdefr)
                   fENs.write(ct_enesdefr)
                   fENs.write(area_enesdefr)
                   #print(area_enesdefr)
                   if term.findall('permutation'):
                      for perm in term.findall('permutation'):
                           fEN.write(perm.text + str_enesdefr)
                           fENs.write(extractMain(perm.text) + strCT_enesdefr)
   
                if term.get('lang')=="spa":
                   esStr = term.find('string').text
                   fES.write(esStr + str_esendefr)
                   fESs.write(extractMain(esStr) + strCT_esendefr)
                   fESs.write(ct_esendefr)
                   fESs.write(area_esendefr)
                   if term.findall('permutation'):
                      for perm in term.findall('permutation'):
                           fES.write(perm.text + str_esendefr)
                           fESs.write(extractMain(perm.text) + strCT_esendefr)

                if term.get('lang')=="ger":
                   deStr = term.find('string').text
                   fDE.write(deStr + str_deenesfr)
                   fDEs.write(extractMain(deStr) + strCT_deenesfr)
                   fDEs.write(ct_deenesfr)
                   fDEs.write(area_deenesfr)
                   if term.findall('permutation'):
                      for perm in term.findall('permutation'):
                           fDE.write(perm.text + str_deenesfr)
                           fDEs.write(extractMain(perm.text) + strCT_deenesfr)
    
                if term.get('lang')=="fre":
                   frStr = term.find('string').text    
                   fFR.write(frStr + str_frenesde)
                   fFRs.write(extractMain(frStr) + strCT_frenesde)
                   fFRs.write(ct_frenesde)
                   fFRs.write(area_frenesde)
                   if term.findall('permutation'):    
                      for perm in term.findall('permutation'):
                           fFR.write(perm.text + str_frenesde)
                           fFRs.write(extractMain(perm.text) + strCT_frenesde)

    print("WARNING: Duplicates exist in meshSplit.[LAN]key.txt")
    # close up the files
    fEN.close()     
    fDE.close()     
    fES.close()     
    fFR.close()     
    fENs.close()     
    fDEs.close()     
    fESs.close()     
    fFRs.close()     


if __name__ == "__main__":
    
    if len(sys.argv) is not 1:
        sys.stderr.write('Usage: python3 %s \n' % sys.argv[0])
        sys.exit(1)
    main()


# sort -u meshSplit.eskey.txt > meshSplit2.eskey.txt
# remove terms in parentheses:
# perl -0777 -pe 's/ \(.*?\)//sg' wp.enkey.txt > wp.enkey2.txt

# paste -d'|||es:|||de:|||fr:' wp.en /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.es /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.de /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.fr | sed  's/_/ /g' > wp.enkey.txt
# paste -d'|||en:|||de:|||fr:' wp.es /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.en /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.de /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.fr | sed  's/_/ /g' > wp.eskey.txt
#paste -d'|||en:|||es:|||de:' wp.fr /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.en /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.es /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.de | sed  's/_/ /g' > wp.frkey.txt
#paste -d'|||en:|||es:|||fr:' wp.de /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.en /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.es /dev/null  /dev/null  /dev/null  /dev/null  /dev/null  wp.fr | sed  's/_/ /g' > wp.dekey.txt

# cat meshSplit2.dekey.txt wp.dekey2.txt  | sort -u > quad.dekey.txt
# cat meshSplit2.enkey.txt wp.enkey2.txt  | sort -u > quad.enkey.txt
# cat meshSplit2.frkey.txt wp.frkey2.txt  | sort -u > quad.frkey.txt
# cat meshSplit2.eskey.txt wp.eskey2.txt  | sort -u > quad.eskey.txt






#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Extracts the abstracts from the PubPshyc database, and prepares the files 
    to be translated with Marian/OpenNMT
    Date: 29.12.2017
    Last modified: 23.01.2019
    Author: cristinae
"""

import urllib.request
import urllib.parse
import json
import os
import sys
import sentenceSplitter as SS


maxSentLength = 100;

# Simple compatibility
try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range



def splitLongSentences(sentences):
    ''' 
    Split long sentences into shorter units so that they can be translated.
    Sentences are spitted by the ';' character as this is the problem in the PP DB
    '''

    sentencesShort = []
    for sent in sentences:
        words = sent.split()
        l = len(words)
        if (l > maxSentLength):
            semicolonsPos = ( [pos for pos, char in enumerate(sent) if char == ';'])
            subsentences = []
            if (len(semicolonsPos) >= 1):
                subsentences = sent.split(";")
                for subsent in subsentences:
                    sentencesShort.append(subsent+';')
            else:
                for i in xrange(0, l, maxSentLength):
                    subsentences = ' '.join(words[i:i+maxSentLength])
            for subsent in subsentences:
                sentencesShort.append(subsent)

        else:
           sentencesShort.append(sent)

    return sentencesShort


def main(path, rows, absType):

    fields = []
    if absType == 'ABHR':
       fields = ['ABHR_D', 'ABHR_E', 'ABHR_F', 'ABHR_S']
    elif absType == 'ABNHR':
       fields = ['ABNHR_D', 'ABNHR_E', 'ABNHR_F', 'ABNHR_S']
    field = ','.join(fields)

    name = "abstract"
    solrBase = "http://136.199.85.71:8002/solr/"
    solrInstance = "pubpsych-core"
    #general: 
    #params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows='+rows]                                                                             
    #if we only want a DB (ACCNO here)                                                                                                                    
    params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=ACCNO:[%20*%20TO%20*%20]', 'rows='+rows]
    solrParams = '&'.join(params)
    solrURL = solrBase+solrInstance+"/select?"+solrParams

    # Read the full DB
    print("Querying at " + solrURL)
    response = urllib.request.urlopen(solrURL)
    data = json.loads(response.read().decode('utf-8'))
    #print json.dumps(data)

    # Go through each doc
    print("Writing response")
    print("WARNING: New downloads will be appended to previous files")
    for i,d in enumerate(data['response']['docs']):
        # Create a directory for the document family in case it is not there
        # a family correspond to a DB more or less
        id = str(d['ID'])
        pos = id.index('_') 
        directory = path+id[:pos]
        if not os.path.exists(directory):
           os.makedirs(directory)
        fes = open(directory+'/'+ name+'.es', 'a')
        fen = open(directory+'/'+ name+'.en', 'a')
        ffr = open(directory+'/'+ name+'.fr', 'a')
        fde = open(directory+'/'+ name+'.de', 'a')
        # Extract the abstract, split by sentence and prepare it to translate into the other languages
        # with the new nomenclature used in training
        fieldLabel = fields[0] #'D'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t') 
           sentences = SS.splitter('de', str(d[fieldLabel]))
           sentences = splitLongSentences(sentences)
           for sent in sentences:
               abstract = sent + str('\n')
               fde.write(header +'<'+name+'> '+ '<2es> ' + abstract) 
           for sent in sentences:
               abstract = sent + str('\n')
               fde.write(header +'<'+name+'> '+ '<2en> ' + abstract) 
           for sent in sentences:
               abstract = sent + str('\n')
               fde.write(header +'<'+name+'> '+ '<2fr> ' + abstract) 
        fieldLabel = fields[1] #'E'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t') 
           sentences = SS.splitter('en', str(d[fieldLabel]))
           sentences = splitLongSentences(sentences)
           for sent in sentences:
               abstract = sent + str('\n')
               fen.write(header +'<'+name+'> '+ '<2es> ' + abstract) 
           for sent in sentences:
               abstract = sent + str('\n')
               fen.write(header +'<'+name+'> '+ '<2de> ' + abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               fen.write(header +'<'+name+'> '+ '<2fr> ' + abstract)
        fieldLabel = fields[2] #'F'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t') 
           sentences = SS.splitter('fr', str(d[fieldLabel]))
           sentences = splitLongSentences(sentences)
           for sent in sentences:
               abstract = sent + str('\n')
               ffr.write(header +'<'+name+'> '+ '<2es> ' + abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               ffr.write(header +'<'+name+'> '+ '<2de> ' + abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               ffr.write(header +'<'+name+'> '+ '<2en> ' + abstract)
        fieldLabel = fields[3] #'S'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t')
           sentences = SS.splitter('es', str(d[fieldLabel]))
           sentences = splitLongSentences(sentences)
           for sent in sentences:
               abstract = sent + str('\n')
               fes.write(header +'<'+name+'> ' + '<2fr> '+ abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               fes.write(header +'<'+name+'> ' + '<2de> ' + abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               fes.write(header +'<'+name+'> ' + '<2en> ' + abstract)
        fes.close()     
        fen.close()     
        ffr.close()     
        fde.close()     


if __name__ == "__main__":
    
    if len(sys.argv) is not 4:
        sys.stderr.write('Usage: python3 %s outputFolder DBsize ABHR|ABNHR\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])


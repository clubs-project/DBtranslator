#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Extracts the abstracts from the PubPshyc database, and prepares the files 
    to be translated with Marian/OpenNMT
    Date: 29.12.2017
    Last modified: 28.12.2018
    Author: cristinae
"""

import urllib.request
import urllib.parse
import json
import os
import sys
import sentenceSplitter as SS

def main(path, rows, absType):

    fields = []
    if absType == 'ABHR':
       fields = ['ABHR_D', 'ABHR_E', 'ABHR_F', 'ABHR_S']
    elif absType == 'ABNHR':
       fields = ['ABNHR_D', 'ABNHR_E', 'ABNHR_F', 'ABNHR_S']
    field = ','.join(fields)

    name = "abstract"
    solrBase = "http://136.199.85.71:8001/solr/"
    solrInstance = "pubpsych-core"
    params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows='+rows]
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
           for sent in sentences:
               abstract = sent + str('\n')
               fde.write(header + '<2es> ' +'<'+name+'> '+ abstract) 
           for sent in sentences:
               abstract = sent + str('\n')
               fde.write(header + '<2en> ' +'<'+name+'> '+ abstract) 
           for sent in sentences:
               abstract = sent + str('\n')
               fde.write(header + '<2fr> ' +'<'+name+'> '+ abstract) 
        fieldLabel = fields[1] #'E'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t') 
           sentences = SS.splitter('en', str(d[fieldLabel]))
           for sent in sentences:
               abstract = sent + str('\n')
               fen.write(header + '<2es> ' +'<'+name+'> '+ abstract) 
           for sent in sentences:
               abstract = sent + str('\n')
               fen.write(header + '<2de> ' +'<'+name+'> '+ abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               fen.write(header + '<2fr> ' +'<'+name+'> '+ abstract)
        fieldLabel = fields[2] #'F'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t') 
           sentences = SS.splitter('fr', str(d[fieldLabel]))
           for sent in sentences:
               abstract = sent + str('\n')
               ffr.write(header + '<2es> ' +'<'+name+'> '+ abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               ffr.write(header + '<2de> ' +'<'+name+'> '+ abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               ffr.write(header + '<2en> ' +'<'+name+'> '+ abstract)
        fieldLabel = fields[3] #'S'
        if fieldLabel in d:
           header = id+' '+fieldLabel+str('\t')
           sentences = SS.splitter('es', str(d[fieldLabel]))
           for sent in sentences:
               abstract = sent + str('\n')
               fes.write(header + '<2fr> ' +'<'+name+'> ' + abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               fes.write(header + '<2de> ' +'<'+name+'> ' + abstract)
           for sent in sentences:
               abstract = sent + str('\n')
               fes.write(header + '<2en> ' +'<'+name+'> ' + abstract)
        fes.close()     
        fen.close()     
        ffr.close()     
        fde.close()     


if __name__ == "__main__":
    
    if len(sys.argv) is not 4:
        sys.stderr.write('Usage: python3 %s outputFolder DBsize ABHR|ABNHR\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])


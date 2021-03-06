#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Extracts the titles from the PubPshyc database, and prepares the files 
    to be translated with Marian/OpenNMT
    Date: 22.12.2017
    Last modified: 23.01.2019
    Author: cristinae
"""

import urllib.request
import urllib.parse
import json
import os
import sys

def main(path, rows):

    #field = "TI_orig, TI_orig_code, TI_D, TI_E, TI_F, TI_S"
    fields = ['TI_D', 'TI_E', 'TI_F', 'TI_S']
    field = ','.join(fields)
    name = "title"
    solrBase = "http://136.199.85.71:8001/solr/"
    solrInstance = "pubpsych-core"
    #params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=1037540']
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
        #directory = str(d['ID'])
        id = str(d['ID'])
        pos = id.index('_') 
        directory = path+id[:pos]  #pos+2 to include the 1st digit per DB
        if not os.path.exists(directory):
           os.makedirs(directory)
        fes = open(directory+'/'+ name+'.es', 'a')
        fen = open(directory+'/'+ name+'.en', 'a')
        ffr = open(directory+'/'+ name+'.fr', 'a')
        fde = open(directory+'/'+ name+'.de', 'a')
        # Extract the desired field and prepare it to translate into the other languages
        # TI_D, TI_E, TI_F, TI_S
        tit = 'TI_D'
        if tit in d:
           title = str(d[tit]) + str('\n')
           header = id+' '+tit+str('\t')
           fde.write(header + '<2es> ' + '<'+name+'> ' + title) 
           fde.write(header + '<2en> ' + '<'+name+'> ' + title) 
           fde.write(header + '<2fr> ' + '<'+name+'> ' + title) 
        tit = 'TI_E'
        if tit in d:
           title = str(d[tit]) + str('\n')
           header = id+' '+tit+str('\t')
           fen.write(header + '<2es> ' +'<'+name+'> ' + title) 
           fen.write(header + '<2de> ' +'<'+name+'> ' + title)
           fen.write(header + '<2fr> ' +'<'+name+'> ' + title)
        tit = 'TI_F'
        if tit in d:
           title = str(d[tit]) + str('\n')
           header = id+' '+tit+str('\t')
           ffr.write(header + '<2es> ' + '<'+name+'> ' + title)
           ffr.write(header + '<2de> ' + '<'+name+'> ' + title)
           ffr.write(header + '<2en> ' + '<'+name+'> ' + title)
        tit = 'TI_S'
        if tit in d:
           title = str(d[tit]) + str('\n')
           header = id+' '+tit+str('\t')
           fes.write(header + '<2fr> ' + '<'+name+'> ' + title)
           fes.write(header + '<2de> ' + '<'+name+'> ' + title)
           fes.write(header + '<2en> ' + '<'+name+'> ' + title)
        fes.close()     
        fen.close()     
        ffr.close()     
        fde.close()     


if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s outputFolder DBsize \n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])


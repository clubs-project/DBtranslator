#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Extract the title/controlled terms and prepares the files to be translated
    Any field with a single item (no multiple sentences) can be added to this 
    script via a new fieldType, fields and name.
    Date: 22.12.2017
    Author: cristinae
"""

import urllib.request
import urllib.parse
import json
import os
import sys

def main(path, rows, fieldType):

    fields = []
    name = "cts"
    if fieldType == 'CTH':
       fields = ['CTDH', 'CTEH', 'CTFH', 'CTSH']
       name = "cth"
    elif fieldType == 'CTL':
       fields = ['CTDL', 'CTEL', 'CTFL', 'CTSL']
       name = "ctl"
    elif fieldType == 'ITH':
       fields = ['ITDH', 'ITEH', 'ITFH', 'ITSH']
       name = "ith"
    elif fieldType == 'ITL':
       fields = ['ITDL', 'ITEL', 'ITFL', 'ITSL']
       name = "itl"
    field = ','.join(fields)

    solrBase = "http://136.199.85.71:8001/solr/"
    solrInstance = "pubpsych-core"
    #params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=1037540']
    params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows='+rows]
    solrParams = '&'.join(params)
    solrURL = solrBase+solrInstance+"/select?"+solrParams

    # Read the full DB
    print("WARNING: New downloads will be appended to previous files")
    print("Querying at " + solrURL)
    response = urllib.request.urlopen(solrURL)
    data = json.loads(response.read().decode('utf-8'))
    #print json.dumps(data)

    # Go through each doc
    print("Writing response")
    for i,d in enumerate(data['response']['docs']):
        # Create a directory for the document family in case it is not there
        # a family correspond to a DB more or less
        #directory = str(d['ID'])
        id = str(d['ID'])
        #if (id.startswith("A")):
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
        fieldLabel = fields[0]
        if fieldLabel in d:
           fieldText = str(d[fieldLabel]) + str('\n')
           header = id+' '+fieldLabel+str('\t')+fieldText
           fde.write(header) 
        fieldLabel = fields[1]
        if fieldLabel in d:
           fieldText = str(d[fieldLabel]) + str('\n')
           header = id+' '+fieldLabel+str('\t')+fieldText
           fen.write(header) 
        fieldLabel = fields[2]
        if fieldLabel in d:
           fieldText = str(d[fieldLabel]) + str('\n')
           header = id+' '+fieldLabel+str('\t')+fieldText
           ffr.write(header)
        fieldLabel = fields[3]
        if fieldLabel in d:
           fieldText = str(d[fieldLabel]) + str('\n')
           header = id+' '+fieldLabel+str('\t')+fieldText
           fes.write(header)
        fes.close()     
        fen.close()     
        ffr.close()     
        fde.close()     


if __name__ == "__main__":
    
    if len(sys.argv) is not 4:
        sys.stderr.write('Usage: python3 %s outputFolder DBsize Field \n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])



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

def main():

    solrBase = "http://136.199.85.71:8001/solr/"
    solrInstance = "pubpsych-core"
    rows=str(1038540)
    #params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=1037540']
    params = ['indent=on', 'wt=json',  'q=*:*', 'rows='+rows]
    solrParams = '&'.join(params)
    solrURL = solrBase+solrInstance+"/select?"+solrParams

    # Read the full DB
    print("Querying at " + solrURL)
    response = urllib.request.urlopen(solrURL)
    data = json.loads(response.read().decode('utf-8'))
    with open('DBpp8001.json', 'w') as outfile:
         json.dump(data, outfile)
    #print json.dumps(data)



if __name__ == "__main__":
    
    if len(sys.argv) is not 1:
        sys.stderr.write('Usage: python3 %s  \n' % sys.argv[0])
        sys.exit(1)
    main()



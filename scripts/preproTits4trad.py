# coding: utf-8

########################################################################
# Extracts the titles from the PubPshyc database, applies a pre-process
# tokenisation, truecasing and prepares the files to be translated with
# Marian
# Date: 22.12.2017
# Author: cristinae
########################################################################

import urllib.request
import urllib.parse
import json
import os

path = "../titles/"

#field = "TI_orig, TI_orig_code, TI_D, TI_E, TI_F, TI_S"
fields = ['TI_D', 'TI_E', 'TI_F', 'TI_S']
field = ','.join(fields)
name = "titles"
solrBase = "http://136.199.85.71:8000/solr/"
solrInstance = "pubpsych-core"
#params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=1037540']
params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=100']
solrParams = '&'.join(params)
solrURL = solrBase+solrInstance+"/select?"+solrParams

# Read the full DB
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
    pos = id.index('_') 
    directory = path+id[:pos+1]
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
       header = id+' '+tit+str('\t')+'<titles> ' 
       fde.write(header + '<2es> ' + title) 
       fde.write(header + '<2en> ' + title) 
       fde.write(header + '<2fr> ' + title) 
    tit = 'TI_E'
    if tit in d:
       title = str(d[tit]) + str('\n')
       header = id+' '+tit+str('\t')+'<titles> ' 
       fen.write(header + '<2es> ' + title) 
       fen.write(header + '<2de> ' + title)
       fen.write(header + '<2fr> ' + title)
    tit = 'TI_F'
    if tit in d:
       title = str(d[tit]) + str('\n')
       header = id+' '+tit+str('\t')+'<titles> ' 
       ffr.write(header + '<2es> ' + title)
       ffr.write(header + '<2de> ' + title)
       ffr.write(header + '<2en> ' + title)
    tit = 'TI_S'
    if tit in d:
       title = str(d[tit]) + str('\n')
       header = id+' '+tit+str('\t')+'<titles> ' 
       fes.write(header + '<2fr> ' + title)
       fes.write(header + '<2de> ' + title)
       fes.write(header + '<2en> ' + title)
    fes.close()     
    fen.close()     
    ffr.close()     
    fde.close()     




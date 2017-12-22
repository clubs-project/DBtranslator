# coding: utf-8

####################################################################
# 
####################################################################
import urllib.request
import urllib.parse
import json
import os


#field = "TI_orig, TI_orig_code, TI_D, TI_E, TI_F, TI_S"
fields = ['TI_D', 'TI_E', 'TI_F', 'TI_S']
field = ','.join(fields)
name = "titles"
solrBase = "http://136.199.85.71:8000/solr/"
solrInstance = "pubpsych-core"
#params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=1037540']
params = ['indent=on', 'wt=json', 'fl=ID,'+field, 'q=*:*', 'rows=10000']
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
    directory = id[:pos+2]
    if not os.path.exists(directory):
       os.makedirs(directory)
    f = open(directory+'/'+ name+'.txt', 'a')
    # Extract the desired field and prepare it to translate into the other languages
    # TI_D, TI_E, TI_F, TI_S
    tit = 'TI_D'
    if tit in d:
       header = id+' '+tit+str('\t')+'<titles> ' 
       f.write(header + '<2es> ' + str(d[tit]) + str('\n'))
       f.write(header + '<2en> ' + str(d[tit]) + str('\n'))
       f.write(header + '<2fr> ' + str(d[tit]) + str('\n'))
    tit = 'TI_E'
    if tit in d:
       header = id+' '+tit+str('\t')+'<titles> ' 
       f.write(header + '<2es> ' + str(d[tit]) + str('\n'))
       f.write(header + '<2de> ' + str(d[tit]) + str('\n'))
       f.write(header + '<2fr> ' + str(d[tit]) + str('\n'))
    tit = 'TI_F'
    if tit in d:
       header = id+' '+tit+str('\t')+'<titles> ' 
       f.write(header + '<2es> ' + str(d[tit]) + str('\n'))
       f.write(header + '<2de> ' + str(d[tit]) + str('\n'))
       f.write(header + '<2en> ' + str(d[tit]) + str('\n'))
    tit = 'TI_S'
    if tit in d:
       header = id+' '+tit+str('\t')+'<titles> ' 
       f.write(header + '<2fr>' + str(d[tit]) + str('\n'))
       f.write(header + '<2de>' + str(d[tit]) + str('\n'))
       f.write(header + '<2en>' + str(d[tit]) + str('\n'))
    f.close()     




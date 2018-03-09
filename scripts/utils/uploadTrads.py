#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Uploads the title/abstract/CT translations previously obtained with 
    tradTitlesAbstracts.sh or tradCTs.py.
    Date: 23.02.2018
    Author: cristinae
"""
import os, sys
import json
import urllib
import urllib.parse
import urllib.request
#import urllib2
import datetime

batch = 100
separator = ':::'


''' Generates the name of the field from the original field and the language of
    the translation (structure for titles) ##TI_E
'''
def lantag2fieldTit(lantag, field):
    lan = lantag[2:-1]
    if(lan=="en"):
       fieldLabel = field[:3]+'E_from_'+field[3:4]
    elif(lan=="es"):
       fieldLabel = field[:3]+'S_from_'+field[3:4]
    elif(lan=="de"):
       fieldLabel = field[:3]+'D_from_'+field[3:4]
    elif(lan=="fr"):
       fieldLabel = field[:3]+'F_from_'+field[3:4]
    return fieldLabel

''' Generates the name of the field from the original field and the language of
    the translation (structure for abstracts) ##ABHR_E
'''
def lantag2fieldAbs(lantag, field):
    lan = lantag[2:-1]
    if(lan=="en"):
       fieldLabel = field[:4]+'_E_from_'+field[5:6]
    elif(lan=="es"):
       fieldLabel = field[:4]+'_S_from_'+field[5:6]
    elif(lan=="de"):
       fieldLabel = field[:4]+'_D_from_'+field[5:6]
    elif(lan=="fr"):
       fieldLabel = field[:4]+'_F_from_'+field[5:6]
    return fieldLabel

''' Generates the name of the field from the original field and the language of
    the translation (structure for CTS)  ##CTEH
'''
def lantag2fieldCT(lantag, field):
    lan = lantag[2:-1]
    if(lan=="en"):
       fieldLabel = field[:2]+'E'+field[3:]+'_from_'+field[2:3]
    elif(lan=="es"):
       fieldLabel = field[:2]+'S'+field[3:]+'_from_'+field[2:3]
    elif(lan=="de"):
       fieldLabel = field[:2]+'D'+field[3:]+'_from_'+field[2:3]
    elif(lan=="fr"):
       fieldLabel = field[:2]+'F'+field[3:]+'_from_'+field[2:3]
    return fieldLabel



def main(inFile, content):
    # Solr details
    solrBase = "http://136.199.85.71:8001/solr/"
    solrInstance = "pubpsych-core"
    #    for downloading
    paramsDownload = ['indent=on', 'wt=json', 'rows='+str(batch) ,'q=ID:(']
    solrParamsDownload = '&'.join(paramsDownload)
    solrURLDownload = solrBase+solrInstance+"/select?"+solrParamsDownload
    #    for uploading
    paramsUpload = ['commit=true', 'wt=json']
    solrParamsUpload = '&'.join(paramsUpload)
    solrURLUpload = solrBase+solrInstance+"/update?"+solrParamsUpload

    # Read data
    print(inFile)
    print("Start time: "+str(datetime.datetime.now()))
    print("Reading data")
    print("")
    with open(inFile) as f:
       id = ''         # id of the article to update
       field = ''      # name of the field to be updated/added
       text = ''       # translation to be uploaded into field
       articles = ''   # IDs to be updated within a batch
       doc = {}        # dictionary with the ID of the document, field and 
                       # translations to be updated within a batch
       i = batch-1
       for line in f:
           line = line.strip()
           if len(line)==0:
              continue
           fields = line.split('\t')
           # input example (CT)
           # DFK_0018980 CTEL	<2fr>	['Comportement d'adaptation', 'Emotional']
           id, field = fields[0].split(' ')
           #articles = articles + 'ID=' + id + '&'
           articles = articles + id + '%20or%20'
           if content=='ct': 
              tradfield = lantag2fieldCT(fields[1], field)
           elif content=='tit': 
              tradfield = lantag2fieldTit(fields[1], field)
           elif content=='abs': 
              tradfield = lantag2fieldAbs(fields[1], field)
           else:
              print("ERROR: Please, especify a correct type of field to upload abs|tit|ct\n")
           text = fields[2]
           # the key includes the both id and the field
           #doc[id+separator+tradfield]=urllib.parse.quote(text) 
           doc[id+separator+tradfield]=text 
           if (i % batch == 0):
               # Let's download the batch of articles
               solrURLDownloadBatch = solrURLDownload + articles + '0)'
               print("Downloading batch " + solrURLDownload)
               response = urllib.request.urlopen(solrURLDownloadBatch)
               data = json.loads(response.read().decode('utf-8'))
               # Look for the articles for which we have new translations in the solr batch-dump
               # Do I really need the double pass?!
               for element in doc.keys():
                   idDoc,field = element.split(separator)
                   for i,d in enumerate(data['response']['docs']):
                       idDownloaded = str(d['ID'])
                       # add the information in the solr batch-dump of the new field
                       if (idDoc == idDownloaded):
                           d[field] = doc[idDownloaded+separator+field]
                           # this if is only triggered for CTs where a list in string format must
                           # be converted to a true list
                           if content=='ct' and d[field].startswith("['") and d[field].endswith("']"):
                              d[field] = d[field][2:-2].split("', '")
                           break
               # Let's upload the updated articles
               print("Updating batch " + solrURLUpload)
               dataSub = {"add":data['response']['docs']}
               toSubmit = json.dumps(dataSub)
               req = urllib.request.Request(solrURLUpload, bytes(toSubmit, encoding="utf-8"))
               req.add_header('Content-type', 'application/json')
               response = urllib.request.urlopen(req)
               # cleaning before going for the next batch
               articles = ''
               doc = {}
               print("")
           i = i+1
       # We are done with the file, let's commit the last batch
       if len(articles)!=0:
          solrURLDownloadBatch = solrURLDownload + articles + '0)'
          print("Last unfinished batch " + solrURLDownload)
          response = urllib.request.urlopen(solrURLDownloadBatch)
          data = json.loads(response.read().decode('utf-8'))
          for element in doc.keys():
              idDoc,field = element.split(separator)
              for i,d in enumerate(data['response']['docs']):
                  idDownloaded = str(d['ID'])
                  if (idDoc == idDownloaded):
                      d[field] = doc[idDownloaded+separator+field]
                      # this if is only triggered for CTs where a list in string format must be
                      # converted to a true list
                      if content=='ct' and d[field].startswith("['") and d[field].endswith("']"):
                         d[field] = d[field][2:-2].split("', '")
                      break
          dataSub = {"add":data['response']['docs']}
          toSubmit = json.dumps(dataSub)
          req = urllib.request.Request(solrURLUpload, bytes(toSubmit, encoding="utf-8"))
          req.add_header('Content-type', 'application/json')
          response = urllib.request.urlopen(req)
    print("\nDONE!")
    print("End time: "+str(datetime.datetime.now()))



if __name__ == "__main__":
    
    if len(sys.argv) is not 3:
        sys.stderr.write('Usage: python3 %s file [abs|tit|ct]\n' % sys.argv[0])
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])



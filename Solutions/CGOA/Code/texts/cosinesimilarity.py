#!/usr/bin/env python
# coding: utf-8

# In[24]:

import sys
print(sys.path)

import numpy as np
import math
import os
import re
import argparse

parser = argparse.ArgumentParser(description='Get the Cosine Similarity for all documents.')
parser.add_argument('filepath', type=str, nargs=1,
                    help='the filepath to the file with all documents')
parser.add_argument('keywords', type=list, nargs=1,
                    help='all entered keywords in a list')
args = parser.parse_args()

rawtext = open(args.filepath, "r", encoding="utf8")
queries = args.keywords

docs = ""
for i in rawtext:
    docs += i
    
listtext = docs.split('"textArr":')

listlist = []
for i in listtext:
    sublist = i.split('"raw":')
    listlist.append(sublist)

listlistlist = []
for i in listlist:
    for j in i:
        if '"date":' in j:
            subsublist = j.split('"date":')
            listlistlist.append(subsublist)
        else:
            continue

truetext = []
for i in np.arange(1, len(listlistlist), 3):
    doc = str(listlistlist[i])
    doc = doc.lower()
    doc = doc.replace('\\n', ' ')
    doc = re.sub('[^a-zA-Z]', ' ', doc) 
    doc = re.sub(r'\s+', ' ', doc)
    truetext.append(doc)

def termFrequency(term, document):
    normalizeDocument = document.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))

def inverseDocumentFrequency(term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in allDocuments:
        if term.lower() in doc.lower().split():
            numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1
 
    if numDocumentsWithThisTerm > 0:
        return 1.0 + math.log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0
    
def tfidf(tf, idf):
    return tf*idf

def cosineSimilarity(queries, document, allDocuments):
    #queries = list of queries
    #document = string of whitespace separated words
    #allDocuments = list of documents
    queriesString = ""
    for query in queries:
        queriesString+= query + " "
    tfidfDOCS = []
    tfidfQUERIES = []
    docTransform = 0
    queryTransform = 0
    for query in queries:
        tfDOC = termFrequency(query, document)
        idfDOC = inverseDocumentFrequency(query, allDocuments)
        tfidfDOC = tfDOC * idfDOC
        tfQUERY = termFrequency(query, queriesString)
        idfQUERY = inverseDocumentFrequency(query, queriesString)
        tfidfQUERY = tfQUERY * idfQUERY
        tfidfDOCS.append(tfidfDOC)
        tfidfQUERIES.append(tfidfQUERY)
        queryTemp = tfidfQUERY**2
        queryTransform += queryTemp
        docTemp = tfidfDOC**2
        docTransform += docTemp
    dot = np.dot(tfidfDOCS, tfidfQUERIES)
    return dot / (math.sqrt(docTransform) * math.sqrt(queryTransform))

for doc in truetext:
    print(cosineSimilarity(queries, doc, truetext))


# In[ ]:





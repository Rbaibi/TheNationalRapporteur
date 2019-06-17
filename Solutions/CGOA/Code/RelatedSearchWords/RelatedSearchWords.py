#!/usr/bin/env python
# coding: utf-8

# In[2]:


import gensim
import argparse

parser = argparse.ArgumentParser(description='Get related search words based on word2vec.')
parser.add_argument('filepath', type=str, nargs=1,
                    help='the filepath to the model')
parser.add_argument('keywords', type=list, nargs=1,
                    help='all entered keywords in a list')
args = parser.parse_args()

model = gensim.models.Word2Vec.load(args.filepath)

Suggested_Queries = model.wv.most_similar(positive=args.keywords, topn = 5)

Related_searchwords = []
for i in [0, 1, 2, 3, 4]:
    searchword = Suggested_Queries[i][0]
    Related_searchwords.append(searchword)
    
print(Related_searchwords)


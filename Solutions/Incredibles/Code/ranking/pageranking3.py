# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 14:33:26 2019

@author: anniewong

%reset -f

"""

# %%

import numpy as np
import pandas as pd
import nltk

nltk.download('punkt')  # one time execution
import os
import json
import re
from nltk.tokenize import sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# Import stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords

from translate import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# check for language and then appy the sentiment model
def get_eng_version(x):
    translator = Translator(from_lang="dutch", to_lang="english")
    translation = translator.translate(x)
    return (translation)


analyser = SentimentIntensityAnalyzer()


def get_sentiment_scores(sentence):
    snt = analyser.polarity_scores(sentence)
    #     print("{:-<40} {}".format(sentence, str(snt)))
    return (snt)


def get_opinion(x):
    if (x is None):
        return
    eng_x = x['text']
    if (x.language == "dutch"):
        eng_x = get_eng_version(x['text'])
    sent = get_sentiment_scores(eng_x)
    is_opinion = 0
    if ((sent['neg'] > 0.1) | (sent['pos'] > 0.1)):
        is_opinion = 1
    else:
        is_opinion = 0

    return (is_opinion)


total = pd.DataFrame()

file_path = os.getcwd() + "/extracted_data.json"

with open(file_path) as json_file:
    data = json.load(json_file)

    # Extract word vectors

    dutch_glove = 'wikipedia-160.txt'
    dutch_stop_words = stopwords.words('dutch')
    dutch_dim = 160

    english_glove = 'glove.6B.100d.txt'
    english_stop_words = stopwords.words('english')
    english_dim = 100

    dutch_word_embeddings = {}
    f_dutch = open(dutch_glove, encoding='utf-8')
    for line in f_dutch:
        dutch_values = line.split()
        dutch_word = dutch_values[0]
        dutch_coefs = np.asarray(dutch_values[1:], dtype='float32')
        dutch_word_embeddings[dutch_word] = dutch_coefs
    f_dutch.close()

    english_word_embeddings = {}
    f_english = open(english_glove, encoding='utf-8')
    for line in f_english:
        english_values = line.split()
        english_word = english_values[0]
        english_coefs = np.asarray(english_values[1:], dtype='float32')
        english_word_embeddings[english_word] = english_coefs
    f_english.close()

    # %%

    for i in range(20, 27):
        print('Processing data frame: ' + str(i) + ' out of: ' + str(len(data)))
        # CREATE DATAFRAME

        list_paragraphs = [paragraph['text'] for paragraph in data[i]['paragraphs']]
        df = pd.DataFrame(list_paragraphs)
        df.columns = ['article_text']
        df['title'] = data[i]['title']

        if len(data[i]['captions']) != 0:

            df['captions_number'] = data[i]['captions'][0]['number']
            df['captions_text'] = data[i]['captions'][0]['text']
            df['captions_type'] = data[i]['captions'][0]['type']

        else:

            df['captions_number'] = 0
            df['captions_text'] = "nan"
            df['captions_type'] = "nan"

        df['created_at'] = data[i]['createdAt']
        df['language'] = data[i]['language']
        df['pagenumber'] = [paragraph['pagenumber'] for paragraph in data[i]['paragraphs']]
        df['type'] = data[i]['type']
        df['par_num'] = pd.Int64Index(range(1, len(df) + 1))

        if df.iloc[0]['language'] == 'dutch':
            word_embeddings = dutch_word_embeddings
            stop_words = dutch_stop_words
            dim = dutch_dim
        else:
            word_embeddings = english_word_embeddings
            stop_words = english_stop_words
            dim = english_dim

        ## SPLIT TEXT INTO SENTENCES

        sentences = []
        for s in df['article_text']:
            sentences.append(sent_tokenize(s))

        sentences = [y for x in sentences for y in x]  # flatten list

        ## READ IN WORD EMBEDDINGS ##

        # Extract word vectors

        if df.iloc[0]['language'] == 'dutch':
            glove = 'wikipedia-160.txt'
            stop_words = stopwords.words('dutch')
            dim = 160


        else:

            glove = 'glove.6B.100d.txt'
            stop_words = stopwords.words('english')
            dim = 100

        ## TEXT PREPROCESSING ##

        sentences = df.article_text
        # remove punctuations, numbers and special characters
        clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

        # make alphabets lowercase
        clean_sentences = [s.lower() for s in clean_sentences]


        # function to remove stopwords
        def remove_stopwords(sen):
            sen_new = " ".join([i for i in sen if i not in stop_words])
            return sen_new


        # remove stopwords from the sentences
        clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences]

        ## VECTOR REPRESENTATION OF SENTENCES ##

        # Extract word vectors

        sentence_vectors = []
        for i in clean_sentences:
            if len(i) != 0:
                v = sum([word_embeddings.get(w, np.zeros((dim,))) for w in i.split()]) / (len(i.split()) + 0.001)
            else:
                v = np.zeros((dim,))
            sentence_vectors.append(v)

        ## SIMILARITY REPRESENTATION ##
        # Similarity matrix
        sim_mat = np.zeros([len(sentences), len(sentences)])

        # Initialize the matrix with cosine similarity scores.
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1, dim), sentence_vectors[j].reshape(1, dim))[0, 0]

        ## APPLYING PAGERANK ALGORITHM ##

        nx_graph = nx.from_numpy_array(sim_mat)
        scores = nx.pagerank(nx_graph)

        ## SUMMARY EXTRACTION ##

        ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

        df['article_text'] = df['article_text'].apply(lambda x: x.encode('utf-8').strip())
        df['text'] = df.article_text.apply(lambda x: x.decode("utf-8"))

        ## Calculate rank for each paragraph ##

        rankdf = pd.DataFrame(ranked_sentences)
        rankdf.columns = ['score', 'paragraph']
        rankdf['rank'] = pd.Int64Index(range(1, len(rankdf) + 1))

        rankdf['first_sen'] = rankdf['paragraph'].apply(lambda x: x.splitlines()[0].replace(' ', ''))

        # Initialize empty dataframe
        outputdf = pd.DataFrame()

        for r in ranked_sentences:
            # for r in ranked_sentences[0:3]:
            first_sent = r[1].split(".")[0]
            first_sent = first_sent.replace('(', '\(').replace(')', '\)')
            first_sent = re.escape(first_sent)
            # first_sent = first_sent.replace('\(', '\\(')
            df_filt = df[(df.text.str.contains(first_sent))]
            # print(df_filt)
            outputdf = pd.concat([outputdf, df_filt])

            outputdf['first_sen'] = outputdf['text'].apply(lambda x: x.splitlines()[0].replace(' ', ''))

        # Concat dataframes (outputdf with rankdf)

        result = pd.merge(outputdf, rankdf, how='inner', left_on='first_sen', right_on='first_sen')
        result.drop('article_text', axis=1, inplace=True)

        total = pd.concat([total, result])
        total.drop('first_sen', axis=1, inplace=True)
        total = total.drop_duplicates()
        total['is_opinion'] = total.apply(lambda x: get_opinion(x), axis=1)
        total.to_csv(os.getcwd() + '/total2.csv')

    # %%

total['is_opinion'] = total.apply(lambda x: get_opinion(x), axis=1)

# %% Export total to csv
total.to_csv(os.getcwd() + '/total2.csv')

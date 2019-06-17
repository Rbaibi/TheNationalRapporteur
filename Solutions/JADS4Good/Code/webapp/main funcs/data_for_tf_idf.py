import pandas as pd
from langdetect import detect
from nltk.tokenize import word_tokenize
import pickle
import os
import io
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import coo_matrix


def get_tf_idf(df, lang = 'nl'):
    doc_ids = df['']
    tex_doc_paths = df['']

    if lang == 'nl':
        stop_words_file = open('../data/misc_files/stopwords_dutch.txt', 'r')

    elif lang == 'en':
        stop_words_file = open('../data/misc_files/stopwords_english.txt', 'r')

    stop_words = stop_words_file.read().split('\n')

    texts = []

    source_path = '../data/text_files/clean/'

    for file in os.listdir(source_path):
        with open(source_path + file, "r", encoding="utf-8") as infile:
            text = infile.readline()
            if detect(text) == lang:
                texts.append(text)

    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words=stop_words)
    vec = coo_matrix(vectorizer.fit_transform(texts))

    df = pd.DataFrame(vec.toarray())
    df.columns = vectorizer.get_feature_names()
    df['Doc_ID'] = df.index

    df_flipped = df.melt(id_vars=["Doc_ID"], var_name="N-gram",
                               value_name="TF-IDF")

    df_flipped = df_flipped.loc[df_flipped['TF-IDF'] > 0]

    df_flipped.reset_index(inplace=True, drop=True)

    return df_flipped

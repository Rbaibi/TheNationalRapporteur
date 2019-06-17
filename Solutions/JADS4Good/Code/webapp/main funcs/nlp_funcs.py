import re
import nltk
import os
from langdetect import detect
from nltk.tokenize import word_tokenize
import pickle
import os
import io
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import coo_matrix

def sanititize_input(query):

    stop_words_dutch_file = open('../data/misc_files/stopwords_dutch.txt', 'r')
    stop_words_english_file = open('../data/misc_files/stopwords_english.txt', 'r')
    stop_words_dutch = stop_words_dutch_file.read().split('\n')
    stop_words_english = stop_words_english_file.read().split('\n')
    stop_words = stop_words_dutch + stop_words_english

    # convert to lower case
    new_query = str.lower(query)

    # removing special characters and digits
    new_query = re.sub('[^a-zA-Z\.]', ' ', new_query )
    new_query = re.sub(r'\s+', ' ', new_query)

    # tokenize words and  stem
    word_tokens = word_tokenize(re.sub('[^A-Za-z0-9]+', ' ', new_query))
    word_tokens = [word for word in word_tokens if word not in stop_words]
    # word_tokens = [word for word in word_tokens]
    new_query = ' '.join(word for word in word_tokens)

    # return sanitized query
    return new_query

def process_text(text):
    text = re.sub('[\n]', ' ', text)
    text = re.sub('[^a-zA-Z\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

def create_tf_idf_matrix():

    stop_words_file_nl = open('../data/misc_files/stopwords_dutch.txt', 'r')
    stop_words_file_en = open('../data/misc_files/stopwords_english.txt', 'r')
    stop_words_nl = stop_words_file_nl.read().split('\n')
    stop_words_en = stop_words_file_en.read().split('\n')

    en_save_folder = "../data/text_files/clean/en/"
    nl_save_folder = "../data/text_files/clean/nl/"
    texts_nl = []
    texts_en = []
    file_names_nl = []
    file_names_en = []

    source_path = '../data/text_files/clean/all/'

    for file in os.listdir(source_path):
        with open(source_path + file, "r", encoding="utf-8") as infile:
            text = infile.readline()
            if detect(text) == 'en':
                texts_en.append(text)
                file_names_en.append(file)
            elif detect(text) == 'nl':
                texts_nl.append(text)
                file_names_nl.append(file)

    for i in range(len(texts_en)):
        with io.open(en_save_folder + file_names_en[i], 'w', encoding="utf-8") as outfile1:
            outfile1.write(texts_en[i])

    for i in range(len(texts_nl)):
        with io.open(nl_save_folder + file_names_nl[i], 'w', encoding="utf-8") as outfile1:
            outfile1.write(texts_nl[i])

    vectorizer_nl = TfidfVectorizer(ngram_range=(1, 3), stop_words=stop_words_nl)
    vectorizer_en = TfidfVectorizer(ngram_range=(1, 3), stop_words=stop_words_en)
    vec_nl = coo_matrix(vectorizer_nl.fit_transform(texts_nl))
    vec_en = coo_matrix(vectorizer_en.fit_transform(texts_en))

    pickle.dump(vec_nl, open("../data/vec_nl.p", "wb"))
    pickle.dump(vec_en, open("../data/vec_en.p", "wb"))

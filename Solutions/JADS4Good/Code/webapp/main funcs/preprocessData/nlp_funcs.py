import re
import nltk
from nltk.tokenize import word_tokenize


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
import PyPDF2
import nltk
import spacy
from string import punctuation
from heapq import nlargest
import re

def spacy_summarise(text,no_sentences,language):

    if(language=='dutch'):
        nlp = spacy.load("nl_core_news_sm")

    else:
        nlp = spacy.load("en_core_web_sm")


    stopwords = nltk.corpus.stopwords.words(language)

    text = re.sub('[^a-zA-Z]', ' ', text )  
    text = re.sub(r'\s+', ' ', text) 

    docx = nlp(text)
    mytokens = [token.text for token in docx]

    # Build Word Frequency
    # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # Maximum Word Frequency
    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    # Sentence Tokens
    sentence_list = [ sentence for sentence in docx.sents ]

    # Sentence Score via comparing each word with sentence
    sentence_scores = {}  
    for sent in sentence_list:  
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if len(sent.text.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(no_sentences, sentence_scores, key=sentence_scores.get)


    # List Comprehension of Sentences Converted From Spacy.span to strings
    final_sentences = [ w.text for w in summarized_sentences ]
    return(final_sentences)


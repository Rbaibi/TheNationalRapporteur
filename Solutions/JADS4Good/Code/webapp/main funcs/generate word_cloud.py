#!/usr/bin/env python
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

import os
import io
from os import path
from wordcloud import WordCloud

path = "../data/text_files/clean/"

for file in os.listdir(path):

    # Read the whole text.
    with open(path + file, 'r') as infile:
        text = infile.readline()

    stop_words_file = open('../data/misc_files/stopwords_dutch.txt', 'r')
    stop_words = stop_words_file.read().split('\n')

    words = []
    sents = text.split('.')
    for sent in sents:
        for word in sent.split():
            if word not in stop_words:
                words.append(word)

    text = " ".join(words)
    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.show()
    plt.savefig("../data/word_cloud/" + file.strip('.txt') + ".png")
import preprocessing
import pandas as pd
import collections
from gensim import corpora
import numpy
import io
from nltk.stem.wordnet import WordNetLemmatizer


# Implementation of the tf-idf algorithm


# print(df.head(), df.loc[1], df.index)

def term_frequency(word, document):
    counter = 0
    for w in document:
        if w == word:
            counter += 1
    return counter


def create_dict():
    df = pd.read_csv("reviews.csv", delimiter=',')
    f = open('dict.txt', "w", encoding="utf-8")
    for i in range(0, 18393):
        clean_text = preprocessing.clear_text(df['review'].loc[i])
        for term in clean_text:
            f.writelines("\n" + term)

    f.close()

def count_words_occurr(filename):
    words = open(filename, "r", encoding="utf-8")
    d = dict()

    for word in words:
        if word in d:
            d[word] = d[word]+1
        else:
            d[word] = 1

    for key in list(d.keys()):
        print(key, ":", d[key])


count_words_occurr("dictionary1.txt")

'''
for i in range(0, 18393):
    print(type(df['review'].loc[i]))
    clean_text = preprocessing.clear_text(df['review'].loc[i])
    for term in clean_text:
        print(term)
        print("Frequency of " + term + " in the" + str(i) + " document")
        print(term_frequency(term, clean_text))

'''


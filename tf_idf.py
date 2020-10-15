import preprocessing
import pandas as pd
from gensim import corpora

# Implementation of the tf-idf algorithm

df = pd.read_csv("reviews.csv", delimiter=',')
print(df.head(), df.loc[1], df.index)

def term_frequency(word, document):
    counter = 0
    for w in document:
        if w == word:
            counter += 1
    return counter

dictionaries = []
for i in range(0, 18393):
    doc = preprocessing.clear_text(df['review'].loc[i])
    dictionaries[i] = corpora.Dictionary(doc)
    dictionaries[i].dfs




#def inverse_document_frequency(N,df)
'''
for i in range(0, 18393):
    print(type(df['review'].loc[i]))
    clean_text = preprocessing.clear_text(df['review'].loc[i])
    for term in clean_text:
        print(term)
        print("Frequency of " + term + " in the" + str(i) + " document")
        print(term_frequency(term, clean_text))

'''


wor = "Gianni"
doc = ["Gianni", "is", "a", "very", "good", "Gianni", "boy"]



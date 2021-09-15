import pandas as pd
import preprocessing
from nltk.tokenize import word_tokenize
import csv


def compute_score(row, vec):
    sc = 0
    row = row.replace("\\", "")
    for w in vec:
        if w[0] in row.split("'"):
            sc += 1

    return sc/len(vec)


def manage_keywords(kwds):
    score = []
    good_match = []
    df = pd.read_csv("Data/cleared_reviews.csv", delimiter=',')
    for i, row in df.iterrows():
        tup = str(i), compute_score(row['review'], kwds), row['artist']
        score.append(tup)
        if score[i][1] != 0.0:
            good_match.append(score[i])

    good_match.sort(key=lambda x:x[1], reverse= True)
    #print(good_match[:5])
    return good_match[:10]

#
# sent = ["canadian","trap", "rapper"]
# manage_keywords(sent)


'''
df = pd.read_csv("Data/reviews.csv", delimiter=',')
with open('Data/cleared_reviews.csv', 'w', encoding="utf-8") as csvfile:
    fieldnames = ['title', 'artist', 'review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

with open('Data/cleared_reviews.csv', 'a', encoding="utf-8") as csv_f:
    for i, row in df.iterrows():
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        r = word_tokenize(preprocessing.clear_text(row['review']))
        writer.writerow({'title': row['title'], 'artist': row['artist'], 'review': r})


'''




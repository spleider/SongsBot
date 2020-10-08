import sqlite3
import pandas as pd
import preprocessing
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import scraper
import numpy
import gensim
from gensim.models import Word2Vec

#create connection with sqlite db
con = sqlite3.connect("database.sqlite")

#creating a pandas data frame
query = pd.read_sql_query("SELECT url, artist, title FROM reviews;", con)

#populating data frame with urls
df = pd.DataFrame(query, columns=['url', 'artist', 'title'])
text = []

for i, row in df.iterrows():
    #print(row.__getitem__('url'))
    album = (str(row.__getitem__('title')))
    artist = (str(row.__getitem__('artist')))
    review = (scraper.extract_corpus(scraper.take_source(str(row.__getitem__('url')))))
    print(review, type(review))
    print(album + "\n", artist)




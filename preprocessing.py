import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
import gensim
from gensim.models import Word2Vec
import pandas as pd
import string


def clear_text(txt):
    #Tokenization
    tokens = word_tokenize(txt)

    #Lowercase conversion
    tokens = [w.lower() for w in tokens]

    #Removing punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    #deleting all non-words
    final_wds = [w for w in stripped if w.isalpha()]

    #removing stopwords
    stop_wd = set(stopwords.words('english'))
    final_wds = [w for w in final_wds if not w in stop_wd]

    #stemming process
    #stemmer = PorterStemmer()
    #final_wds = [stemmer.stem(w) for w in final_wds]

    #Lemmatizer
    lemtz = WordNetLemmatizer()
    final_wds = [lemtz.lemmatize(w) for w in final_wds]

    return final_wds




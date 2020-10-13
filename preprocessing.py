import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import gensim
from gensim.models import Word2Vec



def clear_text(txt):
    stopwd = set(stopwords.words('english'))
    tokens = word_tokenize(txt)
    cleared_txt = []
    for w in tokens:
        if w not in stopwd:
            cleared_txt.append(w)
    return cleared_txt


f = open('try1.txt', 'r')
print(clear_text(f.read()))
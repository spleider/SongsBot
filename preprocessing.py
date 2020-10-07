import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk


strang = open('try1.txt')

def clear_text(txt):
    stop_wd = set(stopwords.words('english'))
    tokens = word_tokenize(txt)
    line = txt.read()  # Use this to read file content as a stream:
    words = line.split()
    for r in words:
        print(r)
        if not r in stop_wd:
            appendFile = open('filteredtext.txt', 'a')
            appendFile.write(" " + r)
            print(appendFile)
            appendFile.close()

    return appendFile





import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import gensim
from gensim.models import Word2Vec

strang = "Gianni is a good boy because he helps old people to bring food at home."

def clear_text(txt):
    #tokens = txt.replace("\n", " ")
    filtered_words = [word for word in txt if word not in stopwords.words('english')]
    return filtered_words


print(clear_text(strang))
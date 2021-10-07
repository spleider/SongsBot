import pandas as pd
import preprocessing
from gensim.models import Word2Vec, KeyedVectors
import nltk

model_s = Word2Vec.load("Data/word2vec_skipgram.model")
model_c = Word2Vec.load("Data/word2vec_cbow.model")

# Creation and training of the Word2Vec model
def create_model():
    df = pd.read_csv("Data/reviews.csv", delimiter=',')

    docs = df['review'].apply(lambda x: preprocessing.clear_text(x))

    doc_vec = [nltk.word_tokenize(d) for d in docs]

    # Creation of the model
    # @params: doc_vec -> vector of documents
    #          min_count-> minimum word count
    #          size-> dimensionality of the embedding (size of the word vector)
    model1 = Word2Vec(doc_vec, min_count=1, size=50, window=10, sg=1)
    model2 = Word2Vec(doc_vec, min_count=1, size=50, window=10, sg=0)

    model1.save("word2vec_skipgram.model")
    model2.save("word2vec_cbow.model")

# Function for retrieve similar words starting from a given list of words
def return_similar(words, count):
    results = []
    while count >0:
        for word in words:
            vec = model_s.wv.most_similar(word)
            results.extend(vec[:2])
            count-=1
    return results

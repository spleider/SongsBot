import pandas as pd
import preprocessing
from gensim.models import Word2Vec, KeyedVectors
import nltk


# Creation and training of the Word2Vec model


def create_model():
    df = pd.read_csv("reviews.csv", delimiter=',')

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


# create_model()
model_s = Word2Vec.load("word2vec_skipgram.model")
model_c = Word2Vec.load("word2vec_cbow.model")


print("\nSkipgram:")
print(model_s.wv.most_similar('rap'))

print("\nCbow:")
print(model_c.wv.most_similar('rap'))
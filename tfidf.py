import preprocessing
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np
import scipy.sparse
import joblib


# Creation of the word_count vector
# Convert a collection of text documents to a matrix of token counts.
# This implementation produces a sparse representation of the counts using scipy.sparse.csr_matrix.

def get_word_count_vec():
    # Open the csv where are stored the reviews to use for compute IDF
    df = pd.read_csv("Data/reviews.csv", delimiter=',')

    # Preprocessing of the reviews
    docs = df['review'].apply(lambda x: preprocessing.clear_text(x))

    # Storing the set of english stopwords
    stopwd = stopwords.words('english')

    docs = docs.tolist()

    # Creating an instance of CountVectorizer
    # (useful for converting a collection of text documents to a matrix of token counts
    count_vec = CountVectorizer(stop_words=stopwd, max_df=0.85)

    # wc_matrix are the final term-document matrix with all the terms of the corpus
    wc_matrix = count_vec.fit_transform(docs)

    # Saving data for unigrams
    scipy.sparse.save_npz('Data/wc_matrix.npz', wc_matrix)
    joblib.dump(count_vec, "Data/countvec.pkl")


# Method for compute the TF_IDF score for a given sentence (based on the reviews corpus)
def compute_tf_idf(word_count_m, cvec, sentence):
    # Preprocessing the sentence
    clear_sentence = preprocessing.clear_text(sentence)

    # Creation of the TfidfTransformer Object,
    # useful for transform a count matrix to a normalized tf or tf-idf representation
    transformer_weights = TfidfTransformer(smooth_idf=True, use_idf=True)

    # Fitting
    transformer_weights.fit_transform(word_count_m)
    tf_idf_vec = transformer_weights.transform(cvec.transform([clear_sentence]))

    # Computing the final weights for the words
    weights = np.asarray(tf_idf_vec.mean(axis=0)).ravel().tolist()
    weights_df = pd.DataFrame({'term': cvec.get_feature_names(), 'weight': weights})
    result = weights_df.sort_values(by='weight', ascending=False).head(5)

    return result.values.tolist()
    # Print the results order by value
    # print(weights_df.sort_values(by='weight', ascending=False).head(5))

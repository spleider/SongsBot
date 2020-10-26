import preprocessing
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import re


# Implementation of the tf-idf algorithm


def create_dict():
    df = pd.read_csv("reviews.csv", delimiter=',')
    f = open('dict.txt', "w", encoding="utf-8")
    for i in range(0, 18393):
        clean_text = preprocessing.clear_text(df['review'].loc[i])
        for term in clean_text:
            f.writelines("\n" + term)

    f.close()


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def get_topn(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


def get_word_c_vec():
    df = pd.read_csv("reviews.csv", delimiter=',')
    df['review'] = df['review'].apply(lambda x: preprocessing.clear_text(x))

    docs = df['review']
    #.tolist()
    #print(docs)
    cv = CountVectorizer(max_df=0.85)

    # The method cv.fit_transform() generate a term-document matrix

    word_c_vec = cv.fit_transform(docs)
    return word_c_vec


def compute_tf_idf(word_c_vec, message):
    tf_id_transform = TfidfTransformer(smooth_idf=True, use_idf=True)
    tf_id_transform.fit(word_c_vec)

    doc = preprocessing.clear_text(message)

    cv = CountVectorizer(max_df=0.85, stop_words=stopwords.words('english'))
    feature_names = cv.get_feature_names()

    tf_idf_vector = tf_id_transform.transform(cv.transform([doc]))

    sorted_items = sort_coo(tf_idf_vector.tocoo())

    keywords = get_topn(feature_names, sorted_items, 10)

    # now print the results
    print("\nMessage:")
    print(doc)
    print("\nKeywords:")
    for k in keywords:
        print(k, keywords[k])


vec = get_word_c_vec()
mess = "Hello I'd like to have an experimental jazz album"

compute_tf_idf(vec, mess)

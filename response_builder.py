import pandas as pd
# import word2vec


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
        if score[i][1] != 0.0 and score[i][2] != 'various artists':
            good_match.append(score[i])

    good_match.sort(key=lambda x: x[1], reverse=True)
    # print(good_match[:5])
    return good_match[:5]


# sent = ["rock","drum", "guitar"]
# print(word2vec.return_similar(sent,2))
# print(manage_keywords(sent))

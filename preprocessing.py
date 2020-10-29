import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import string


def clear_text(txt):
    # Tokenization
    tokens = word_tokenize(txt)

    # Lowercase conversion
    tokens = [w.lower() for w in tokens]

    # Removing punctuation
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # deleting all non-words
    final_wds = [w for w in stripped if w.isalpha()]

    # removing stopwords
    stop_wd = set(stopwords.words('english'))
    final_wds = [w for w in final_wds if w not in stop_wd]

    # lemmatizer
    lemtz = WordNetLemmatizer()
    final_wds = [lemtz.lemmatize(w) for w in final_wds]
    final_text = []

    for term in final_wds:
        final_text.append(term + " ")

    last = ''.join(map(str, final_text))

    return last


print("\nClear Text result:\n")
print(clear_text("Hello I'm Gianni and I am a very good person because I help animals"))

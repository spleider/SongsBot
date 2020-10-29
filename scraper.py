from bs4 import BeautifulSoup
import requests


# This scraper.py module is useful for retrieving the paragraphs from the pitchfork website
def take_source(url):
    source = requests.get(url).text
    return source


def extract_corpus(source):
    soup = BeautifulSoup(source, "html.parser")
    corpus = []
    for e in soup.select("p"):
        corpus.append(e.text)

    return corpus


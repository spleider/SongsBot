from bs4 import BeautifulSoup
import bs4
import requests

def take_source(url):
        source = requests.get(url).text
        return source

def extract_corpus(source):
    soup = BeautifulSoup(source, "html.parser")
    corpus = []
    for e in soup.select("p"):
        corpus.append(e.text)

    return corpus

print(extract_corpus(take_source(url)))
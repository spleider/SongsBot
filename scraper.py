from bs4 import BeautifulSoup
import bs4
import requests


def take_source(url):
    if 'http://' or 'https://' in url:
        source = requests.get(url).text
        return source
    else:
        print("Invalid URL")


def extract_corpus(source):
    soup = BeautifulSoup(source, "html.parser")
    soup.prettify().encode('cp1252', errors='ignore')
    corpus = []
    for e in soup.select("p"):
        corpus.append(e.text)

    return corpus



#extract_corpus(take_source(url))
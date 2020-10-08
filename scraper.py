from bs4 import BeautifulSoup
import bs4
import requests

url = "http://pitchfork.com/reviews/albums/22701-traditional-music-of-notional-species-vol-ii/"

def take_source(url):
    if 'http://' or 'https://' in url:
        source = requests.get(url).text
        return source
    else:
        print("Invalid URL")


def extract_corpus(source):
    soup = BeautifulSoup(source, "html.parser")
    corpus = []
    for e in soup.select("p"):
        corpus.append(e.text)
    return corpus



#extract_corpus(take_source(url))
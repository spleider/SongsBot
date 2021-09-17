from bs4 import BeautifulSoup
import requests


# This scraper.py module is useful for retrieving the paragraphs from the pitchfork website
# With take_source we pick the source starting from the url of the web resource
def take_source(url):
    source = requests.get(url).text
    return source


# With extract corpus we can take the html of the page for retrieving the body of the reviews
def extract_corpus(source):
    soup = BeautifulSoup(source, "html.parser")
    corpus = []
    # Selection of the p tags (paragraphs) on the html
    for e in soup.select("p"):
        corpus.append(e.text)

    return corpus


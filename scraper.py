from bs4 import BeautifulSoup
import bs4
import requests

url = "https://pitchfork.com/reviews/albums/22703-mezzanine/"

def take_source(url):
    if 'http://' or 'https://' in url:
        source = requests.get(url).text
        return source
    else:
        print("Invalid URL")



def extract_corpus(source):

    soup = BeautifulSoup(source, "html.parser")

    for e in soup.select("p"):
        print(e.text)



extract_corpus(take_source(url))
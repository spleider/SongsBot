import sqlite3
import pandas as pd
import scraper
import csv
import preprocessing

#create connection with sqlite db
con = sqlite3.connect("database.sqlite")

#creating a pandas data frame
query = pd.read_sql_query("SELECT url, artist, title FROM reviews;", con)


#populating data frame with urls
df = pd.DataFrame(query, columns=['url', 'artist', 'title'])

#preparing the .txt file for storing the reviews
with open('reviews.csv', 'w', encoding="utf-8") as csvfile:
        fieldnames = ['title', 'artist', 'review']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def append_csv(tit,art,rev):
    with open('reviews.csv','a', encoding="utf-8") as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
        writer.writerow({'title': tit, 'artist':art,'review':rev})

for i, row in df.iterrows():
    #print(row.__getitem__('url'))
    album = (str(row['title']))
    artist = (str(row['artist']))
    review = (scraper.extract_corpus(scraper.take_source(row['url'])))
    append_csv(album,artist,review)
    #print(type(review))

print("Done")

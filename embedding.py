import sqlite3
import pandas as pd

#create connection with sqlite db
con = sqlite3.connect("database.sqlite")

df = pd.read_sql_query("SELECT url FROM reviews", con)



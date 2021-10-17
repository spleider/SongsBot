# SongsBot
Repository for the SongsBot telegram bot. 

@author: Enrico Collu

Project for the 2021 AI-NLP course of Università degli Studi di Cagliari.

**Introduction**

Songsbot is a Telegram bot that, starting from a phrase given in input by the user 
(for example: "I want canadian indie rock songs"), returns youtube links to songs that most correspond to the user's request.

**Main NLP features**

The system mainly uses two NLP features:
1) Tf-idf (term-frequency / inverse document-frequency)
2) Knowledge Graph with Sparql and DBpedia

_Tf-idf_ is used to score the most relevant words of the user input.
It is calculated on the basis of the corpus available in the dataset and, once the sentence is received from the user, 
a list of the most characteristic words is returned (sorted by decreasing score)

_Sparql_ is used as a query language for the DBpedia environment (a Wikipedia database that can be queried through RDF queries). 
This section of the project allows, starting from the name of an artist, to obtain information about the songs produced by him.

**Dataset composition**

The starting dataset consists of approximately 18,000 links to reviews on the Pitchfork website (https://pitchfork.com/).
Starting from these links, a Web Scraping job was carried out in order to build a new database that contained the corpus of reviews in textual form.
In this way it was possible to build a more useful dataset for the type of task to be performed.

**Python libraries**
1) sqlite3 -> database connection
2) pandas -> Dataframe management
3) bs4 and BeautifulSoup -> Web Scraping
4) requests -> HTTP requests
5) telepot -> Telegram Bot management
6) joblib -> perform parallel work
7) scipy -> managing NLP tools
8) numpy -> powerful tool for matrix operations
9) nltk.corpus -> useful for preprocessing tasks
10) sklearn.feature_extraction -> compute TF-IDF
11) SPARQLWrapper -> Sparql query environment
12) urllib.request -> retrieving youtube links
13) gensim -> Word2Vec module (tried but not used in the final version of the project)

**File and project structure**

1) **main.py** is the main project file, which connects the entire system and makes the bot active.
The bot setup and the actual service management are managed within this file.
All other modules of the project converge in this file.
   
2) **preprocessing.py** contains useful tools to carry out the main textual preprocessing operations (tokenization, lowercase conversion, stopwords removing, lemmatization, etc ...)

3) **datamanager.py** it takes care of creating the connection to the initial links database and managing the whole module for the creation of the new textual database. 
   It calls inside methods created in the scraper.py module (which allows you to carry out the work of retrieving the textual content from the pages).
   
4) **queriesSparQL.py** contains the method to perform the SparQL queries to DBpedia

5) **responsebuilder.py** it returns scores to the artists based on the keyword match within the reviews themselves.

6) **youtube_module.py** contains the useful method to return the link of the YouTube video corresponding to the artist sought (providing the first useful result)

**Usage of the bot**

1) Start the service by running the **main.py** file.

2) once the service is active, on Telegram it is necessary to search for the bot (**@Songs20Bot**) and start a chat.

3) To get started, type **/start** and send the message.
At that point the Bot will respond by providing instructions for use.
   
4) The bot will return youtube videos of the songs it deems appropriate.

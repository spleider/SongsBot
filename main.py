from pprint import pprint
import time
import scipy.sparse
import joblib
import telepot
import tfidf
import response_builder
import queriesSpar
import pandas as pd
import youtube_module
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


f = open('token.txt', "r")
bot = telepot.Bot(f.read())


# Module for manage user's text inputs
def on_chat_message(msg):
    # Saving useful message info
    content_type, chat_type, chat_id = telepot.glance(msg)
    pprint(msg)

    # Check for content type
    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = str(msg['text'])
        if '/start'== txt:
            bot.sendMessage(chat_id, 'Hello {}! I\'m SongBot.'.format(name))
            bot.sendMessage(chat_id, "I can find some tracks based on your wishes.")
            bot.sendMessage(chat_id, "We can discovery a lot of new songs together.")
            bot.sendMessage(chat_id, "Type 'go' and let's begin the trip:")

        elif txt == 'go' or txt == 'GO' or txt == 'Go':
            bot.sendMessage(chat_id, "Give me informations about the song (like genre, nationality, and so on)")

        else:
            # Load wc_matrix presaved
            matr = scipy.sparse.load_npz('Data/wc_matrix.npz')
            cvec = joblib.load("Data/countvec.pkl")

            # Compute tf-idf score on user message
            resp = tfidf.compute_tf_idf(matr, cvec, txt)

            # Retrieving artist name based on review search
            output = response_builder.manage_keywords(resp)

            # Setting number of results for the main process
            n_results = 3

            print("\nKeywords:")
            print(output)
            related_results = []
            bot.sendMessage(chat_id, "Here are some results:")

            while n_results > 0:
                # For each candidate artist (el)
                for el in output:
                    try:
                        df = pd.DataFrame()
                        # Retrieving artist's songs from the sparql endpoint on DBPEDIA
                        df = queriesSpar.get_dbpedia_results(el[2])

                        # Check for results
                        if df.shape[0] >= 1:

                            # Select only the first two records (song)
                            df = df.head(2)
                            for i, row in df.iterrows():
                                # Formatting keyword and retrieving the youtube link
                                search_kwd = str(row['song_title']) +str(row['artist'])
                                link = youtube_module.get_video_link(search_kwd)

                                # Return output to user
                                bot.sendMessage(chat_id,"Title: " + str(row['song_title']))
                                bot.sendMessage(chat_id, "Artist: "+ str(row['artist']))
                                bot.sendMessage(chat_id, "Label: " + str(row['label']))
                                bot.sendMessage(chat_id, link)
                                n_results = n_results - 1
                        else:
                            # If an artist doesn't match any song on DBPEDIA, we add it to another list.
                            # In this way I can return other related matches.
                            related_results.append(el[2])
                    except:
                        pass

            # check for eventually no results available
            if n_results == 3:
                bot.sendMessage(chat_id, "Sorry, no match found! :(")
            else:
                # Managing the related section
                bot.sendMessage(chat_id, "Here are some related results based on my search:")
                for i in range(0,5):
                    kwd = related_results[i]

                    # For avoid non musical results, append Official to the search keyword
                    link = youtube_module.get_video_link(kwd + " Official")
                    bot.sendMessage(chat_id, kwd)
                    bot.sendMessage(chat_id, link)

            # Final message
            bot.sendMessage(chat_id, "Thanks for using Songsbot! If you want to restart type /start")


# Method for manage button module
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print("Callback Query: ", query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text="YEAH")
    bot.sendMessage(query_id, "What are you looking for?")


response = bot.getUpdates()
pprint(response)

# Managing different inputs
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})


# Keeping the program running
while 1:
    time.sleep(3)
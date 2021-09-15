from pprint import pprint
import time
import scipy.sparse
import joblib
import telepot
import tfidf
import response_builder
import queriesSpar
import pandas as pd
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

import youtube_module

f = open('token.txt', "r")
bot = telepot.Bot(f.read())


def on_chat_message(msg):
    # Saving useful message info
    content_type, chat_type, chat_id = telepot.glance(msg)

    pprint(msg)

    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = str(msg['text'])
        if '/start'== txt:
            bot.sendMessage(chat_id, 'Hello {}! I\'m SongBot.'.format(name))
            bot.sendMessage(chat_id, "I can find some tracks based on your wishes.")
            bot.sendMessage(chat_id, "We can discovery a lot of new songs together.")
            bot.sendMessage(chat_id, "Type 'go' and let's begin the trip:")

        elif txt == 'go' or txt == 'GO' or txt == 'Go':
            bot.sendMessage(chat_id, "Give me informations about the song (like genre, year, nationality, and so on)")

        else:
            matr = scipy.sparse.load_npz('Data/wc_matrix.npz')
            cvec = joblib.load("Data/countvec.pkl")

            resp = tfidf.compute_tf_idf(matr, cvec, txt)
            output = response_builder.manage_keywords(resp)
            n_results = 5
            tot_res = 0
            # print("\nKeywords:")
            bot.sendMessage(chat_id, "Here are some results:")
            while n_results > 0:
                for el in output:
                    try:
                        df = pd.DataFrame()
                        df = queriesSpar.get_dbpedia_results(el[2])
                        # print(df.head())
                        if df.shape[0] >= 1:
                            if n_results == 0: break

                            df = df.head(1)
                            for i, row in df.iterrows():
                                search_kwd = str(row['song_title']) +str(row['artist'])
                                link = youtube_module.get_video_link(search_kwd)
                                bot.sendMessage(chat_id,"Title: " + str(row['song_title']))
                                bot.sendMessage(chat_id, "Artist: "+ str(row['artist']))
                                bot.sendMessage(chat_id, link)
                                n_results = n_results - 1

                    except:
                        pass
            if n_results == 5: bot.sendMessage(chat_id, "Sorry, no match found! :(")


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
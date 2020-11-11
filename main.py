from pprint import pprint
import time
import scipy.sparse
import joblib
import telepot
import tfidf
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

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
            bot.sendMessage(chat_id, "I can find some album based on your wishes.")
            bot.sendMessage(chat_id, "We can discovery a lot of albums together.")
            bot.sendMessage(chat_id, "Type 'Go' and let's begin the trip:")

        elif txt == 'go' or txt == 'GO':
            bot.sendMessage(chat_id, "Give me informations like genre, year, nationality and so on")

        else:
            matr = scipy.sparse.load_npz('Data/wc_matrix.npz')
            cvec = joblib.load("Data/countvec.pkl")

            resp = tfidf.compute_tf_idf(matr, cvec, txt)

            print("\nKeywords:")
            print(resp)


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
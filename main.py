from pprint import pprint
import time
import scipy.sparse
import joblib
import telepot
import tfidf
import response_builder
import queriesSparQL
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
        if '/start' == txt:
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

            year = None
            bef = False
            aft = False
            gen = False
            gen_n = []

            music_genres = [
                'Blues',
                'Country',
                'Dance',
                'Disco',
                'Funk',
                'Grunge',
                'Hip Hop',
                'Jazz',
                'Metal',
                'Pop',
                'Rhythm and Blues',
                'Rap',
                'Reggae',
                'Rock',
                'Industrial',
                'Alternative',
                'Ska',
                'Death Metal',
                'Techno',
                'Ambient',
                'Trip-Hop',
                'Vocal',
                'Jazz & Funk',
                'Fusion',
                'Trance',
                'Classical',
                'Instrumental',
                'Acid',
                'House',
                'Gospel',
                'Alternative Rock',
                'Classic Rock',
                'Bass',
                'Soul',
                'Punk',
                'Ethnic',
                'Gothic',
                'Darkwave',
                'Techno-Industrial',
                'Electronic',
                'Pop-Folk',
                'Eurodance',
                'Southern Rock',
                'Comedy',
                'Cult',
                'Gangsta',
                'Christian Rap',
                'Funk',
                'Jungle',
                'New Wave',
                'Psychedelic',
                'Rave',
                'Showtunes',
                'Lo-Fi',
                'Tribal',
                'Acid Punk',
                'Acid Jazz',
                'Polka',
                'Retro',
                'Musical',
                'Rock ’n’ Roll',
                'Hard Rock',
                'Folk',
                'Heavy Metal',
                'Black Metal',
                'Breakbeat',
                'Chillout',
                'Downtempo',
                'Dub',
                'EDM',
                'Eclectic',
                'Electro',
                'Electroclash',
                'Emo',
                'Experimental',
                'Garage',
                'Global',
                'Lounge']

            for word in txt.split(sep=" "):
                if word.isdigit():
                    if len(word) == 4:
                        year = word
                elif word == "before":
                    bef = True
                elif word == "after":
                    aft = True
                else:
                    for g in music_genres:
                        if word in g.lower() and not gen_n:
                            gen_n.append(g)

            # Compute tf-idf score on user message
            resp = tfidf.compute_tf_idf(matr, cvec, txt)

            print(resp)

            resp = [r for r in resp if r[1]> 0.0]

            print(resp)

            # Retrieving artist name based on review search
            output = response_builder.manage_keywords(resp)

            # Setting number of results for the main process
            n_results = 3

            print("\nKeywords:")
            print(output)
            related_results = []
            bot.sendMessage(chat_id, "Here are some results:")


            # For each candidate artist (el)
            for el in output:
                try:
                    if n_results <= 3 and n_results >= 0:
                        df = pd.DataFrame()
                        # Retrieving artist's songs from the sparql endpoint on DBPEDIA
                        if year is None:
                            df = queriesSparQL.get_dbpedia_results(el[2])

                        else:
                            df = queriesSparQL.get_dbpedia_results(el[2], year=year, bef=bef, aft=aft)

                        df = df.drop_duplicates()
                        # Check for results
                        if df.shape[0] >= 1:

                            # Select only the first two records (song)
                            df = df.head(2)
                            for i, row in df.iterrows():
                                # Formatting keyword and retrieving the youtube link
                                search_kwd = str(row['artist'] + " " + str(row['song_title']))
                                link = youtube_module.get_video_link(search_kwd)

                                # Return output to user
                                bot.sendMessage(chat_id, "Title: " + str(row['song_title']))
                                bot.sendMessage(chat_id, "Artist: " + str(row['artist']))
                                bot.sendMessage(chat_id, "Label: " + str(row['label']))
                                bot.sendMessage(chat_id, "Year: " + str(row['year']))
                                bot.sendMessage(chat_id, link)
                                n_results = n_results - 1
                        else:
                            # If an artist doesn't match any song on DBPEDIA, we add it to another list.
                            # In this way I can return other related matches.
                            if el[2] != "various artists":
                                related_results.append(el[2])
                except:
                    pass

            # check for eventually no results available
            if n_results == 3:
                bot.sendMessage(chat_id, "Sorry, no match found on DBpedia :( let's look for some related results! ")
                bot.sendMessage(chat_id, "Let's look for some related results! ")
            else:
                # Managing the related section
                bot.sendMessage(chat_id, "-------------------------------------------------")
                bot.sendMessage(chat_id, "Here are some related results based on my search:")
                for rel in related_results:
                    kwd = rel

                    # For avoid non musical results, append Official to the search keyword
                    link = youtube_module.get_video_link(kwd + " Official audio")
                    bot.sendMessage(chat_id, kwd)
                    bot.sendMessage(chat_id, link)

            if gen_n:
                bot.sendMessage(chat_id, "-------------------------------------------------")
                bot.sendMessage(chat_id, "For you, a mix based on your genre:")
                gen_n = " ".join(gen_n)

                link = youtube_module.get_video_link(gen_n + " top tracks")
                bot.sendMessage(chat_id, gen_n)
                bot.sendMessage(chat_id, link)

            # Final message
            bot.sendMessage(chat_id, "Thanks for using Songsbot! If you want to restart type /start")


# Method for manage button module - NOT USED
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

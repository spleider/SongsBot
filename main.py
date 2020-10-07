from pprint import pprint
import sparql
import sys
import queriesSpar
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from SPARQLWrapper import SPARQLWrapper


bot = telepot.Bot("1165813160:AAHeOi4DHXvSnwVYwLea3wcq9TgsGOhPUsM")
'''
q =  ('SELECT DISTINCT ?station, ?orbits WHERE { '
'?station a <http://dbpedia.org/ontology/SpaceStation> . '
'?station <http://dbpedia.org/property/orbits> ?orbits . '
'FILTER(?orbits > 50000) } ORDER BY DESC(?orbits)')
result = sparql.query('http://dbpedia.org/sparql', q)
print(result.variables)
'''


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #print(content_type, chat_type, chat_id)
    #print(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard =[ [InlineKeyboardButton(text ="Cliccami", callback_data = 'press')], ])
    if content_type == 'text':
        name = msg["from"]["first_name"]
        txt = msg['text']

        if 'hi' or 'ciao' or 'hello' in txt:
            bot.sendMessage(chat_id, 'Hello {}! I\'m SongBot.'.format(name))
            bot.sendMessage(chat_id, "We can discovery a lot of albums together.")
            bot.sendMessage(chat_id, "Give me informations like genre, year, nationality and so on")
        else:
            bot.sendMessage(chat_id, 'Sorry {}, I don\'t understand '.format(name))



    #bot.sendMessage(chat_id, "Hello, i'm SongBot", reply_markup=keyboard)
    #pprint(msg)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print("Callback Query: ", query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text="YEAH")



bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})


while 1:
    time.sleep(3)
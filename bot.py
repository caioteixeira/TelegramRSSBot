from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
import logging
import os
import feedparser

def handle_link(bot, update):
    d = feedparser.parse(update.message)
    print('parsed! ' + update.message)
    for post in d.entries:
        print('title: ' + post.title)
        bot.send_message(chat_id=update.message.chat_id, text=post.title)

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        print('Unauthorized chat id')
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print('malformed request')
        # handle malformed requests - read more below!
    except TimedOut:
        print('time out!')
        # handle slow connection problems
    except NetworkError:
        print('NetworkError!')
        # handle other connection problems
    except ChatMigrated as e:
        print('Chat ChatMigrated')
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print('Error!')
        # handle all other telegram related errors

TOKEN = os.environ.get('TOKEN')
WEBHOOK = os.environ.get('WEBHOOK')
PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (Filters.entity('url') | Filters.entity('text_link')), handle_link))
dispatcher.add_error_handler(error_callback)


# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook(WEBHOOK + TOKEN)
updater.idle()


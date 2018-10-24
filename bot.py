from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
import logging
import os
import feedparser

from time import mktime
from datetime import datetime, date, time

def get_publish_date(post):
    parsed_date = post.published_parsed
    return datetime.fromtimestamp(mktime(parsed_date))

def handle_link(bot, update):
    d = feedparser.parse(update.message.text)

    for post in d.entries:
        text = post.title
        text += '\t' + post.link
        publish_date = get_publish_date(post)
        date_diff = datetime.utcnow() - publish_date;
        if(date_diff.days < 1):
            bot.send_message(chat_id=update.message.chat_id, text=text)


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


def add_handlers(dispatcher):
    dispatcher.add_handler(
        MessageHandler(Filters.text & (Filters.entity('url') | Filters.entity('text_link')), handle_link))
    dispatcher.add_error_handler(error_callback)


def setup_webhook(updater, token):
    webhook = os.environ.get('WEBHOOK')
    port = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                          port=port,
                          url_path=token)
    updater.bot.set_webhook(webhook + token)


TOKEN = os.environ.get('TOKEN')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(TOKEN)
dispatcher = updater.dispatcher
add_handlers(dispatcher)

setup_webhook(updater, TOKEN)
updater.idle()

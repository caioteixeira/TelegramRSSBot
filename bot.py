from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
import logging
import os
import feedparser

def hello(bot, update):
    update.message.reply_text(update.message.text.upper())

def handle_link(bot, update):
	NewsFeed = feedparser.parse(update.message)
	entry = NewsFeed.entries[1]
	update.message.reply_text(entry.summary + entry.link)

TOKEN = os.environ.get('TOKEN')
WEBHOOK = os.environ.get('WEBHOOK')
PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, hello))
updater.dispatcher.add_handler(MessageHandler(Filters.entity("url")), handle_link)

# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook(WEBHOOK + TOKEN)
updater.idle()


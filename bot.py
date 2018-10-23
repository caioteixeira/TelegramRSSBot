from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from wit import Wit
import logging
import os

def hello(bot, update):
    update.message.reply_text(update.message.text.upper())

def processAudio(bot, update):
	voice = update.message.voice.get_file()
	downloadedVoice = voice.download_as_bytearray()
	update.message.reply_text("DOWNLOADED_VOICE")

TOKEN = os.environ.get('TOKEN')
WEBHOOK = os.environ.get('WEBHOOK')
PORT = int(os.environ.get('PORT', '8443'))
WIT_TOKEN = os.environ.get('WIT_TOKEN')

witClient = Wit(WIT_TOKEN)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, hello))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, processAudio))

# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook(WEBHOOK + TOKEN)
updater.idle()


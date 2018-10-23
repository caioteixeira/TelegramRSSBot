from telegram.ext import Updater
import logging

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="AAAAA")

TOKEN = os.environ.get('TOKEN')
WEBHOOK = os.environ.get('WEBHOOK')
PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater = Updater(TOKEN)
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook(WEBHOOK + TOKEN)
updater.idle()

updater.dispatcher.add_handler(CommandHandler('start', start))
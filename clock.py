from apscheduler.schedulers.blocking import BlockingScheduler
from model import Model

from bot import update_feed

import logging
import os
from telegram.ext import Updater

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    model = Model()
    token = os.environ.get('TOKEN')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater = Updater(token)
    feeds = model.get_all_feeds()

    for feed in feeds:
        update_feed(updater.bot, feed.chat.chat_id, feed.url)

sched.start()
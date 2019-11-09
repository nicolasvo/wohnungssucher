import logging
import tempfile
import json
from functools import wraps
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import Bot

with open("app/res/token.json") as f:
    token = json.load(f)["token"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

bot = Bot(token)


def start(update, context):
    update.message.reply_text('Oh, hi there. You will be updated on available apartments every 5 minutes.\n\n'
                              'https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Baden-Wuerttemberg/Karlsruhe/-/-/25,00-/EURO--800,00')
    logging.info(f'chat id: {update.message.chat_id}, user id: {update.message.from_user.id}')
    with open('app/res/chats.json', 'r') as f:
        content = json.load(f)

    if update.message.chat_id not in content['chat_ids']:
        logging.info('New chat was added!')
        content['chat_ids'].append(update.message.chat_id)
        with open('app/res/chats.json', 'w') as f:
            json.dump(content, f)


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.start_polling()
updater.idle()

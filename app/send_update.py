from telegram import Bot
import json
from app.helpers import fetch_list
import logging

url = "https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Baden-Wuerttemberg/Karlsruhe/-/-/25,00-/EURO--800,00"

with open("app/res/token.json") as f:
    token = json.load(f)["token"]

with open('app/res/chats.json', 'r') as f:
    content = json.load(f)

with open('app/res/offers.json', 'r') as f:
    existing_offers = json.load(f)

result = fetch_list(url)

if not set(result['ids']).issubset(set(existing_offers['ids'])):
    logging.info('New offers!')
    bot = Bot(token)
    bot.send_message(content['chat_ids'][0], 'New offer!')

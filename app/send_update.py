import json
import logging
from telegram import Bot, ChatAction
from helpers import fetch_offers

url = "https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Baden-Wuerttemberg/Karlsruhe/-/-/25,00-/EURO--800,00"

with open("app/res/token.json") as f:
    token = json.load(f)["token"]

with open('app/res/chats.json', 'r') as f:
    chats = json.load(f)

with open('app/res/offers.json', 'r') as f:
    existing_offers = json.load(f)

results = fetch_offers(url)

if not set(results['ids']).issubset(set(existing_offers['ids'])):
    logging.info('New offers!')
    bot = Bot(token)
    new_ids = set(results['ids']) - set(existing_offers['ids'])
    for offer in results['results']:
        if offer['id'] in new_ids:
            text = f"{offer['title']}\n" \
                   f"{offer['url']}\n" \
                   f"{offer['address']}\n" \
                   f"{offer['price']} (cold)\n" \
                   f"{offer['charges']} (charges)\n" \
                   f"{offer['price_total']} (total)\n" \
                   f"{offer['area']}\n" \
                   f"{offer['rooms']} room(s)\n" \
                   f"{offer['from_date']}"

            existing_offers['ids'].append(offer['id'])
            existing_offers['results'].append(offer)
            for chat_id in chats['chat_ids']:
                bot.send_chat_action(chat_id, ChatAction.TYPING)
                bot.send_message(chat_id, text=text)

    with open('app/res/offers.json', 'w') as f:
        json.dump(existing_offers, f)


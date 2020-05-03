import requests
from lxml import html


def fetch_apartment(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    xpath_from_date = '//dd[@class="is24qa-bezugsfrei-ab grid-item three-fifths"]/text()'
    xpath_charges = '//dd[@class="is24qa-nebenkosten grid-item three-fifths"]/text()'
    xpath_price_total = '//dd[@class="is24qa-gesamtmiete grid-item three-fifths font-bold"]/text()'
    return {
        "from_date": tree.xpath(xpath_from_date)[0].strip() if len(tree.xpath(xpath_from_date)) else 'N/A',
        "charges": tree.xpath(xpath_charges)[1].strip() if len(tree.xpath(xpath_charges)) else 'N/A',
        "price_total": tree.xpath(xpath_price_total)[0].strip() if len(tree.xpath(xpath_price_total)) else 'N/A',
    }


def fetch_offers(url):
    response = requests.get(url)
    tree = html.fromstring(response.content)
    latest = tree.xpath('//div[@class="result-list-entry__data"]')
    result = []
    ids = []
    for apartment in latest:
        id = apartment.xpath('./a[@class="result-list-entry__brand-title-container"]')[0].get('data-go-to-expose-id')
        price, area, rooms = [_.xpath('./dd//text()')[0] for _ in apartment.xpath('.//dl')]
        url_apartment = f'https://www.immobilienscout24.de/expose/{id}'

        dict_ = {
            "id": id,
            "title": apartment.xpath('./a[@class="result-list-entry__brand-title-container"]/h5/text()')[0],
            "url": url_apartment,
            "address": apartment.xpath('.//button/text()')[0],
            "price": price,
            "area": area,
            "rooms": rooms,
        }

        dict_.update(fetch_apartment(url_apartment))

        result.append(dict_)
        ids.append(id)

    return {
        "results": result,
        "ids": ids,
    }

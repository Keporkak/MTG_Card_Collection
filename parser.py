import requests
import json
from pyquery import PyQuery as pq
from pprint import pprint as pp
from tkinter import *


def series_for_card(card_name):
    card_search_url = 'https://www.cardkingdom.com/catalog/search?filter%5Bipp%5D=60&filter%5Bsort%5D=name&filter%5Bname%5D={}'
    search_result = requests.get(card_search_url.format(card_name))
    d = pq(search_result.content)
    results = d('div.productListRow div.mainListing div.productCardWrapper')

    series = {}

    for card in results.items():
        title = list(card.find('div.itemContentWrapper .productDetailTitle a').items())[0].text().strip()
        description = list(card.find('div.itemContentWrapper div.productDetailSet').items())[0].text().strip()
        price = list(card.find('div.itemContentWrapper div.addToCartWrapper div.amtAndPrice .stylePrice').items())[0].text().strip()
        rarity = description[-2:-1]

        if title not in series:
            series[title] = []

        series[title].append([description[:-4], rarity, price])

    return series


while True:
    series = {}
    card_name = input('Card name: ')

    with open('collection.json', 'r') as collection:
        file_content = collection.read()
        series = json.loads(file_content)
        collection.close()

    series.update(series_for_card(card_name))

    with open('collection.json', 'w') as collection:
        json.dump(series, collection)
        collection.close()

    pp(series)
    print()

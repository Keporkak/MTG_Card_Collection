import requests
import json
from pyquery import PyQuery as pq
from pprint import pprint as pp

## FUNCTIONS ##

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

def specfic_card_cost(card_name, edition):
    price = 'NOT_FOUND'

    with open('edColl.json', 'r') as jsoun:
        editions = json.loads(jsoun.read())
        jsoun.close()

    selected = editions[edition]

    card_url = 'https://www.cardkingdom.com/catalog/view/?filter%5Bsort%5D=name&filter%5Bsearch%5D=mtg_advanced&filter%5Btab%5D=mtg_foil&filter%5Bname%5D={}&filter%5Bcategory_id%5D={}&filter%5Bmulti%5D%5B0%5D=1&filter%5Btype_mode%5D=any&filter%5Btype_key%5D=&filter%5Bpow1%5D=&filter%5Bpow2%5D=&filter%5Btuf1%5D=&filter%5Btuf2%5D=&filter%5Bconcast1%5D=&filter%5Bconcast2%5D=&filter%5Bprice_op%5D=&filter%5Bprice%5D=&filter%5Bkey_text1%5D=&filter%5Bmanaprod_select%5D=any&filter[tab]=mtg_card'
    search_result = requests.get(card_url.format(card_name, selected))
    d = pq(search_result.content)
    results = d('div.productListRow div.mainListing div.productCardWrapper')

    for card in results.items():
        price = list(card.find('div.itemContentWrapper div.addToCartWrapper div.amtAndPrice .stylePrice').items())[0].text().strip()

    return price

def load_editions():
    print ('Loading editions... ', end='', flush=True)

    search_url = 'https://www.cardkingdom.com/catalog/search?filter%5Bipp%5D=60&filter%5Bsort%5D=name&filter%5Bname%5D=Search'
    search_result = requests.get(search_url)
    d = pq(search_result.content)
    results = d('div.productListRow div.sidePanel div.editionToggle div.filterContainer div.layoutWrapper select option[value]')

    editions = {}

    for edition in results.items():
        editions[edition.text().strip()] = edition.val()

    with open('edColl.json', 'w') as jsoun:
        json.dump(editions, jsoun)
        jsoun.close()

    print('DONE')

## ACTUAL PROGRAM ##

load_editions()
while True:
    card_name = input('Card name: ')
    edition = input('Edition: ')

    with open('collection.json', 'r') as collection:
        file_content = collection.read()
        json_content = json.loads(file_content)
        collection.close()

    series = specfic_card_cost(card_name, edition)
    #json_content.update(series)

    with open('collection.json', 'w') as collection:
        json.dump(json_content, collection)
        collection.close()

    pp(series)
    print()

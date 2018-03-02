import requests
from pyquery import PyQuery as pq
from pprint import pprint as pp


def series_for_card(card_name):
    card_search_url = 'https://www.cardkingdom.com/catalog/search?search=header&filter%5Bname%5D={}'
    search_result = requests.get(card_search_url.format(card_name))
    d = pq(search_result.content)
    results = d('div.productListRow div.mainListing div.productCardWrapper')

    series = {}
#    editions = []

    for card in results.items():
        title = list(card.find('div.itemContentWrapper .productDetailTitle a').items())[0].text().strip()
        description = list(card.find('div.itemContentWrapper div.productDetailSet').items())[0].text().strip()
        description = description[:-4]

        if title not in series:
            series[title] = []

        series[title].append(description)
#        editions.append(description)

    return series


while True:
    card_name = input('Card name: ')
    series = series_for_card(card_name)
    pp(series)
    print()

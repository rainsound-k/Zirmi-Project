from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_11st_item_info(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    item_img = soup.select_one('.thumbBox .v-align img').get('src')
    item_price_str = soup.select_one('.sale_price').text
    item_price = int(item_price_str.replace(',', ''))
    item_name = soup.select_one('.heading h2').text

    context = {
        'item_img': item_img,
        'item_price': item_price,
        'item_name': item_name,
    }
    return context



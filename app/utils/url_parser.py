import re
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_item_info_url(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    if '11st.co.kr' in url:
        if not soup.select_one('.thumbBox .v-align img'):
            item_img = ''
        else:
            item_img = soup.select_one('.thumbBox .v-align img').get('src')
        if not soup.select_one('.sale_price'):
            item_price_str = ''
        else:
            item_price_str = soup.select_one('.sale_price').text
        if not item_price_str:
            item_price = ''
        else:
            item_price = int(item_price_str.replace(',', ''))
        if not soup.select_one('.heading h2'):
            item_name = ''
        else:
            item_name = soup.select_one('.heading h2').text

    elif 'gmarket.co.kr' in url:
        if not soup.select_one('.thumb-gallery .viewer .on img'):
            item_img = ''
        else:
            item_img = soup.select_one('.thumb-gallery .viewer .on img').get('src')
        if not soup.select_one('.price_real'):
            item_price_str = ''
        else:
            item_price_str = soup.select_one('.price_real').text
        if not item_price_str:
            item_price = ''
        else:
            item_price = int(item_price_str.replace(',', '').replace('원', ''))
        if not soup.select_one('.itemtit'):
            item_name = ''
        else:
            item_name = soup.select_one('.itemtit').text

    elif 'auction.co.kr' in url:
        if not soup.select_one('.thumb-gallery .viewerwrap .viewer .on img'):
            item_img = ''
        else:
            item_img = soup.select_one('.thumb-gallery .viewerwrap .viewer .on img').get('src')
        if not soup.select_one('.price_real'):
            item_price_str = ''
        else:
            item_price_str = soup.select_one('.price_real').text
        if not item_price_str:
            item_price = ''
        else:
            item_price = int(item_price_str.replace(',', '').replace('원', ''))
        if not soup.select_one('.itemtit'):
            item_name = ''
        else:
            item_name = soup.select_one('.itemtit').text

    elif 'interpark.com' in url:
        # 동적페이지므로 js 데이터로 추출
        soup_text = soup.text
        if not re.search(r'"upldFileTp":"15","fileFnm":"(.+.jpg)(.+"upldFileTp":"16")', soup_text):
            item_img = ''
        else:
            item_img = re.search(r'"upldFileTp":"15","fileFnm":"(.+.jpg)(.+"upldFileTp":"16")', soup_text).group(1)
        if not re.search(r'"dcPrice":(\d+)', soup_text):
            item_price_str = ''
        else:
            item_price_str = re.search(r'"dcPrice":(\d+)', soup_text).group(1)
        if not item_price_str:
            item_price = ''
        else:
            item_price = int(item_price_str)
        if not re.search(r'"prdNm":"(.+)","spcase', soup_text):
            item_name = ''
        else:
            item_name = re.search(r'"prdNm":"(.+)","spcase', soup_text).group(1)

    elif 'smartstore.naver.com' in url:
        if not soup.select_one('.bimg .img_va img'):
            item_img = ''
        else:
            item_img = soup.select_one('.bimg .img_va img').get('src').replace('?type=m450', '')
        if not soup.elect_one('.fc_point .thm'):
            item_price_str = ''
        else:
            item_price_str = soup.select_one('.fc_point .thm').text
        if not item_price_str:
            item_price = ''
        else:
            item_price = int(item_price_str.replace(',', ''))
        if not soup.select_one('.prd_name'):
            item_name = ''
        else:
            item_name = soup.select_one('.prd_name').text.replace('상품명: ', '')

    else:
        item_img = ''
        item_price = ''
        item_name = ''

    context = {
        'item_img': item_img,
        'item_price': item_price,
        'item_name': item_name,
    }
    return context



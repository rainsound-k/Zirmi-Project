import re
from urllib.request import urlopen

from bs4 import BeautifulSoup


def get_item_info_url(url):
    if 'auction.co.kr' in url:
        item_no = re.search(r'[iI]tem[nN]o=(\w+)(.*)', url).group(1)
        url = 'http://itempage3.auction.co.kr/DetailView.aspx?ItemNo=' + item_no
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

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

    elif 'gmarket.co.kr' in url:
        item_no = re.search(r'goods[cC]ode=(\w+)(.*)', url).group(1)
        url = 'http://item.gmarket.co.kr/DetailView/Item.asp?goodscode=' + item_no
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

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

    elif '11st.co.kr' in url:
        item_no = re.search(r'prd[nN]o=(\w+)(.*)', url).group(1)
        url = 'http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getSellerProductDetail&prdNo=' + item_no
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

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

    elif 'interpark.com' in url:
        # 모바일과 데스크탑 url 구조가 다름
        if 'm.shop.interpark.com' in url:
            item_no = re.search(r'product/(\w+)(.*)', url).group(1)
        else:
            item_no = re.search(r'prdNo=(\w+)(.*)', url).group(1)
        url = 'http://shopping.interpark.com/product/productInfo.do?prdNo=' + item_no
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        # 동적페이지므로 js 데이터로 추출
        soup_text = soup.text
        if not re.search(r'"upldFileTp":"15","fileFnm":"(.+.jpg)', soup_text):
            item_img = ''
        else:
            item_img_group = re.search(r'"upldFileTp":"15","fileFnm":"(.+jpg)', soup_text).group(1)
            item_img = item_img_group[:item_img_group.find('"')]
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
        item_no = re.search(r'products/(\w+)(.*)', url).group(1)
        url = 'http://smartstore.naver.com/aladin/products/' + item_no
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')

        if not soup.select_one('.bimg .img_va img'):
            item_img = ''
        else:
            item_img = soup.select_one('.bimg .img_va img').get('src').replace('?type=m450', '')
        if not soup.select_one('.fc_point .thm'):
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
        url = url

    context = {
        'item_img': item_img,
        'item_price': item_price,
        'item_name': item_name,
        'url': url,
    }

    return context

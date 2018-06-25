import re
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


class ItemData:
    def __init__(self, url):
        self.url = url
        self.item_img = ''
        self.item_price = ''
        self.item_name = ''

    def get_info_from_11st(self):
        url = self.url
        if re.search(r'prd[nN]o=(\w+)(.*)', url):
            item_no = re.search(r'prd[nN]o=(\w+)(.*)', url).group(1)
            url = 'http://www.11st.co.kr/product/SellerProductDetail.tmall?method=getSellerProductDetail&prdNo=' \
                  + item_no
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.thumbBox .v-align img'):
                item_img = ''
            else:
                item_img = soup.select_one('.thumbBox .v-align img').get('src')
            if not soup.select_one('.price_detail .sale_price'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.price_detail .sale_price').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.heading h2'):
                item_name = ''
            else:
                item_name = soup.select_one('.heading h2').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_gmarket(self):
        url = self.url
        if re.search(r'goods[cC]ode=(\w+)(.*)', url):
            item_no = re.search(r'goods[cC]ode=(\w+)(.*)', url).group(1)
            url = 'http://item.gmarket.co.kr/DetailView/Item.asp?goodscode=' + item_no
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.thumb-gallery .viewer .on img'):
                item_img = ''
            else:
                item_img = soup.select_one('.thumb-gallery .viewer .on img').get('src')
            if not soup.select_one('.price_real'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.price_real').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', '').replace('원', ''))
            if not soup.select_one('.itemtit'):
                item_name = ''
            else:
                item_name = soup.select_one('.itemtit').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_auction(self):
        url = self.url
        if re.search(r'[iI]tem[nN]o=(\w+)(.*)', url):
            item_no = re.search(r'[iI]tem[nN]o=(\w+)(.*)', url).group(1)
            url = 'http://itempage3.auction.co.kr/DetailView.aspx?ItemNo=' + item_no
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')

        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.thumb-gallery .viewerwrap .viewer .on img'):
                item_img = ''
            else:
                item_img = soup.select_one('.thumb-gallery .viewerwrap .viewer .on img').get('src')
            if not soup.select_one('.price_real'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.price_real').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', '').replace('원', ''))
            if not soup.select_one('.itemtit'):
                item_name = ''
            else:
                item_name = soup.select_one('.itemtit').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_interpark(self):
        url = self.url
        # 모바일과 데스크탑 url 구조가 다름
        if 'm.shop.interpark.com' in url and re.search(r'product/(\w+)(.*)', url):
            item_no = re.search(r'product/(\w+)(.*)', url).group(1)
            url = 'http://shopping.interpark.com/product/productInfo.do?prdNo=' + item_no
        elif re.search(r'prdNo=(\w+)(.*)', url):
            item_no = re.search(r'prdNo=(\w+)(.*)', url).group(1)
            url = 'http://shopping.interpark.com/product/productInfo.do?prdNo=' + item_no
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
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

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_naver_store(self):
        url = self.url
        if re.search(r'products/(\w+)(.*)', url):
            shop_name = re.search(r'com/(\w+)/products/(\w+)(.*)', url).group(1)
            item_no = re.search(r'com/(\w+)/products/(\w+)(.*)', url).group(2)
            url = f'http://smartstore.naver.com/{shop_name}/products/{item_no}'
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.bimg .img_va img'):
                item_img = ''
            else:
                before_item_img = soup.select_one('.bimg .img_va img').get('src')
                item_img = re.search(r'(.+jpg)(.*)', before_item_img).group(1)
            if not soup.select_one('.fc_point .thm'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.fc_point .thm').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.prd_name'):
                item_name = ''
            else:
                item_name = soup.select_one('.prd_name').text.replace('상품명: ', '')

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_naver_short_url(self):
        url = self.url
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.bimg .img_va img'):
                item_img = ''
            else:
                before_item_img = soup.select_one('.bimg .img_va img').get('src')
                item_img = re.search(r'(.+jpg)(.*)', before_item_img).group(1)
            if not soup.select_one('.fc_point .thm'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.fc_point .thm').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.prd_name'):
                item_name = ''
            else:
                item_name = soup.select_one('.prd_name').text.replace('상품명: ', '')

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_lotte_mall(self):
        url = self.url
        if re.search(r'goods_no=(\w+)(.*)', url):
            item_no = re.search(r'goods_no=(\w+)(.*)', url).group(1)
            url = 'http://www.lotteimall.com/goods/viewGoodsDetail.lotte?goods_no=' + item_no
        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.area_thumb .thumb_product img'):
                item_img = ''
                item_name = ''
            else:
                item_img = soup.select_one('.area_thumb .thumb_product img').get('src')
                item_name = soup.select_one('.area_thumb .thumb_product img').get('alt')
            if not soup.select_one('.price .final .num'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.price .final .num').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_lotte_dot_com(self):
        url = self.url
        if 'ellotte.com' in url:
            if re.search(r'goods_no=(\w+)(.*)', url):
                item_no = re.search(r'goods_no=(\w+)(.*)', url).group(1)
                url = 'http://www.ellotte.com/goods/viewGoodsDetail.lotte?goods_no=' + item_no
        else:
            if re.search(r'goods_no=(\w+)(.*)', url):
                item_no = re.search(r'goods_no=(\w+)(.*)', url).group(1)
                url = 'http://www.lotte.com/goods/viewGoodsDetail.lotte?goods_no=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.zoomImg .zoom img'):
                item_img = ''
            else:
                item_img = soup.select_one('.zoomImg .zoom img').get('src')
            if not soup.select_one('.price .big'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.price .big').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.prd-name .pname'):
                item_name = ''
            else:
                item_name = soup.select_one('.prd-name .pname').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_hyundai(self):
        url = self.url
        if 'm.hyundaihmall.com' in url:
            if re.search(r'ItemCode=(\w+)(.*)', url):
                item_no = re.search(r'ItemCode=(\w+)(.*)', url).group(1)
                url = 'http://www.hyundaihmall.com/front/pda/itemPtc.do?slitmCd=' + item_no
        else:
            if re.search(r'slitmCd=(\w+)(.*)', url):
                item_no = re.search(r'slitmCd=(\w+)(.*)', url).group(1)
                url = 'http://www.hyundaihmall.com/front/pda/itemPtc.do?slitmCd=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.pdtPhoto .pic480x480 img'):
                item_img = ''
            else:
                item_img = soup.select_one('.pdtPhoto .pic480x480 img').get('src')
            if not soup.select_one('.finalPrice'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.finalPrice strong').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.prdInfoTitle .pdtTitle'):
                item_name = ''
            else:
                item_name = soup.select_one('.prdInfoTitle .pdtTitle').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_ssg(self):
        url = self.url
        if re.search(r'itemId=(\w+)(.*)', url):
            item_no = re.search(r'itemId=(\w+)(.*)', url).group(1)
            url = 'http://www.ssg.com/item/itemView.ssg?itemId=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.cdtl_imgbox img'):
                item_img = ''
            else:
                item_img = 'http:' + soup.select_one('.cdtl_imgbox img').get('src')
            if not soup.select_one('.cdtl_price .ssg_price'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.cdtl_price .ssg_price').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.cdtl_info_tit'):
                item_name = ''
            else:
                item_name = soup.select_one('.cdtl_info_tit').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_gs(self):
        url = self.url
        if re.search(r'prdid=(\w+)(.*)', url):
            item_no = re.search(r'prdid=(\w+)(.*)', url).group(1)
            url = 'http://with.gsshop.com/prd/prd.gs?prdid=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.view_area .btn_img img'):
                item_img = ''
            else:
                item_img = soup.select_one('.view_area .btn_img img').get('src')
            if not soup.select_one('.price-definition-ins ins'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.price-definition-ins ins').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.product-title'):
                item_name = ''
            else:
                if soup.select_one('.product-title span'):
                    before_item_name = soup.select_one('.product-title span').text
                    item_name = soup.select_one('.product-title').text.strip().replace(before_item_name, '')
                item_name = soup.select_one('.product-title').text.strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_galleria(self):
        url = self.url
        if re.search(r'item_id=(\w+)(.*)', url):
            item_no = re.search(r'item_id=(\w+)(.*)', url).group(1)
            url = 'http://www.galleria.co.kr/item/showItemDtl.do?item_id=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('#gallery img'):
                item_img = ''
                item_name = ''
            else:
                item_img = soup.select_one('#gallery img').get('src')
                item_name = soup.select_one('#gallery img').get('alt')
            if not soup.select_one('.customer .fl .t_price'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.customer .fl .t_price').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_ak(self):
        url = self.url
        if re.search(r'goods_id=(\w+)(.*)', url):
            item_no = re.search(r'goods_id=(\w+)(.*)', url).group(1)
            url = 'http://www.akmall.com/goods/GoodsDetail.do?goods_id=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('#mainGoodsImage'):
                item_img = ''
                item_name = ''
            else:
                item_img = 'http:' + soup.select_one('#mainGoodsImage').get('src')
                item_name = soup.select_one('#mainGoodsImage').get('alt')
            if not soup.select_one('.sale .c_pink i'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.sale .c_pink i').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_ns(self):
        url = self.url
        if re.search(r'partNumber=(\w+)(.*)', url):
            item_no = re.search(r'partNumber=(\w+)(.*)', url).group(1)
            url = 'http://www.nsmall.com/ProductDisplay?partNumber=' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('#photoview_img'):
                item_img = ''
            else:
                item_img = 'http:' + soup.select_one('#photoview_img').get('src')
            if not soup.select_one('.save_price .price'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.save_price .price').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('#ip_productName'):
                item_name = ''
            else:
                item_name = soup.select_one('#ip_productName').get('value').strip()

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_coupang(self):
        url = self.url
        if re.search(r'products/(\w+)(.*)', url):
            item_no = re.search(r'products/(\w+)(.*)', url).group(1)
            if re.search(r'itemId=(\w+)(.*)', url):
                item_id = re.search(r'itemId=(\w+)(.*)', url).group(1)
                url = f'https://www.coupang.com/vp/products/{item_no}?itemId={item_id}'
            url = f'https://www.coupang.com/vp/products/{item_no}'
        hdr = {'referer': 'http://m.naver.com', 'User-Agent': 'Mozilla/5.0'}
        req = requests.get(url, headers=hdr)
        soup = BeautifulSoup(req.text, 'html.parser')

        if not soup.select_one('.prod-image__detail'):
            item_img = ''
        else:
            item_img = 'http:' + soup.select_one('.prod-image__detail').get('src')
        if not soup.select_one('.prod-sale-price .total-price strong'):
            item_price_str = ''
        else:
            item_price_str = soup.select_one('.prod-sale-price .total-price strong').text.strip()
        if not item_price_str:
            item_price = ''
        else:
            item_price = int(item_price_str.replace('원', '').replace(',', ''))
        if not soup.select_one('.prod-buy-header .prod-buy-header__title'):
            item_name = ''
        else:
            item_name = soup.select_one('.prod-buy-header .prod-buy-header__title').text.strip()

        self.item_img = item_img
        self.item_price = item_price
        self.item_name = item_name
        self.url = url

    def get_info_from_wemakeprice(self):
        url = self.url
        if re.search(r'deal/adeal/(\w+)(.*)', url):
            item_no = re.search(r'deal/adeal/(\w+)(.*)', url).group(1)
            url = 'http://www.wemakeprice.com/deal/adeal/' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if not soup.select_one('.img_area .roll .slides_control .onecutImage'):
                item_img = ''
            else:
                item_img = soup.select_one('.img_area .roll .slides_control .onecutImage').get('src')
            if not soup.select_one('.sale .num'):
                item_price_str = ''
            else:
                item_price_str = soup.select_one('.sale .num').text.strip()
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.price_area .deal_tit'):
                item_name = ''
            else:
                before_item_name = soup.select_one('.price_area .deal_tit')
                item_name = re.search(r'\t\t\t(.+)<br/>(.*)', str(before_item_name)).group(1)

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_tmon(self):
        url = self.url
        if 'mobile' in url and re.search(r'deals/(\w+)(.*)', url):
            item_no = re.search(r'deals/(\w+)(.*)', url).group(1)
            url = 'https://www.ticketmonster.co.kr/deal/' + item_no
        elif re.search(r'deal/(\w+)(.*)', url):
            item_no = re.search(r'deal/(\w+)(.*)', url).group(1)
            url = 'https://www.ticketmonster.co.kr/deal/' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'lxml')

            if not soup.select_one('#front_image_area'):
                item_img = ''
            else:
                item_img = soup.select_one('#front_image_area').get('src')
            if not soup.select_one('.price .now_price') and not soup.select_one('.sell .num'):
                item_price_str = ''
            elif soup.select_one('.price .now_price'):
                before_item_price_str = soup.select('.price .now_price')
                item_price_list = []
                for i in before_item_price_str:
                    item_price_list.append(i.text)
                item_price_str = ','.join(re.findall('\d+', item_price_list[0]))
            elif soup.select_one('.sell .num'):
                item_price_str = soup.select_one('.sell .num')
            else:
                item_price_str = ''
            if not item_price_str:
                item_price = ''
            else:
                item_price = int(item_price_str.replace(',', ''))
            if not soup.select_one('.ct_wrp .main') and not soup.select_one('.ct_area .tit'):
                item_name = ''
            elif soup.select_one('.ct_wrp .main'):
                item_name = soup.select_one('.ct_wrp .main').text.strip()
            elif soup.select_one('.ct_area .tit'):
                item_name = soup.select_one('.ct_area .tit').text.strip()
            else:
                item_name = ''

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

    def get_info_from_g9(self):
        url = self.url
        item_no = ''
        if 'm.g9.co.kr' in url:
            if re.search(r'VIP/(\w+)(.*)', url):
                item_no = re.search(r'VIP/(\w+)(.*)', url).group(1)
                url = 'http://www.g9.co.kr/Display/VIP/Index/' + item_no
        elif 'g9ro.kr' in url:
            url = url
        else:
            if re.search(r'Index/(\w+)(.*)', url):
                item_no = re.search(r'Index/(\w+)(.*)', url).group(1)
                url = 'http://www.g9.co.kr/Display/VIP/Index/' + item_no

        try:
            html = urlopen(url)
        except Exception as ex:
            print(f'{ex} 에러가 발생했습니다')
        else:
            soup = BeautifulSoup(html, 'html.parser')

            if 'g9ro.kr' in url:
                if re.search(r'http://image.g9.co.kr/g/(\d+)', str(soup)):
                    item_no = re.search(r'http://image.g9.co.kr/g/(\d+)', str(soup)).group(1)
                    item_img = f'http://image.g9.co.kr/g/{item_no}/n'
                else:
                    item_img = ''
            else:
                item_img = f'http://image.g9.co.kr/g/{item_no}/n'
            item_price = ''

            if not re.search(r'<meta content="G9 - (.+)', str(soup)):
                item_name = ''
            else:
                before_item_name = re.search(r'<meta content="G9 - (.+)', str(soup)).group(1)
                item_name = before_item_name[:before_item_name.find('"')]

            self.item_img = item_img
            self.item_price = item_price
            self.item_name = item_name
            self.url = url

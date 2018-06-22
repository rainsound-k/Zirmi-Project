from utils.url_parser import ItemData


class CheckURL:
    def __init__(self, url):
        self.url = url
        self.item_data = ItemData(url)

    def check_url_from_parser(self):
        url = self.url

        if '11st.co.kr' in url:
            self.item_data.get_info_from_11st()

        elif 'gmarket.co.kr' in url:
            self.item_data.get_info_from_gmarket()

        elif 'auction.co.kr' in url:
            self.item_data.get_info_from_auction()

        elif 'interpark.com' in url:
            self.item_data.get_info_from_interpark()

        elif 'smartstore.naver.com' in url:
            self.item_data.get_info_from_naver_store()

        elif 'naver.me' in url:
            self.item_data.get_info_from_naver_short_url()

        elif 'lotteimall.com' in url:
            self.item_data.get_info_from_lotte_mall()

        elif 'lotte.com' in url:
            self.item_data.get_info_from_lotte_dot_com()

        elif 'hyundaihmall.com' in url:
            self.item_data.get_info_from_hyundai()

        elif 'ssg.com' in url:
            self.item_data.get_info_from_ssg()

        elif 'gsshop.com' in url:
            self.item_data.get_info_from_gs()

        elif 'galleria.co.kr' in url:
            self.item_data.get_info_from_galleria()

        elif 'akmall.com' in url:
            self.item_data.get_info_from_ak()

        elif 'nsmall.com' in url:
            self.item_data.get_info_from_ns()

        # elif 'coupang.com' in url:
        #     self.item_data.get_info_from_coupang()

        elif 'wemakeprice.com' in url:
            self.item_data.get_info_from_wemakeprice()

        elif 'ticketmonster.co.kr' in url:
            self.item_data.get_info_from_tmon()

        elif 'g9.co.kr' in url or 'g9ro.kr' in url:
            self.item_data.get_info_from_g9()

import datetime
import random
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
# import pymongo


from lxml import etree
import requests


# client = pymongo.MongoClient('localhost',27017)
# shidai = client['shidai']
# comments = shidai['comments']




COOKIES ='cy=169; cye=xuchang; _lxsdk_cuid=168b1d8dfbdc8-0827ed78ae6184-58422116-100200-168b1d8dfbfb5; _lxsdk=168b1d8dfbdc8-0827ed78ae6184-58422116-100200-168b1d8dfbfb5; _hc.v=b038fcd1-b5ff-1599-4adc-5ab38b21bdbe.1549172007; s_ViewType=10; aburl=1; ctu=66a794ac79d236ecce433a9dd7bbb8bf927bfbb880a7e885ad18589eec5e2c5a; dper=0a8e7e4a7aa3a95fba7daa5c62071a475bf6699d665678dfed94828ea388fc2ca18fcf20293e5d31d6abe43665a9483ecb89511a42388703179e87aea4e8072157c350c205ff43f2d41d14c06f57873a2049debc7f37256007623b3fc126c781; ua=18324696214; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=168c6f8264d-304-0a6-c08%7C%7C639'


class DianpingComment:
    font_size = 14
    start_y = 23


    def __init__(self, shop_id, cookies, delay=7, handle_ban=True):
        self.shop_id = shop_id
        self._delay = delay
        self.num = 1
        self._cookies = self._format_cookies(cookies)
        self._css_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        self._default_headers = {
            'Connection': 'keep-alive',
            'Host': 'www.dianping.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        self._cur_request_url = 'http://www.dianping.com/shop/{}/review_all/p{}'.format(shop_id,self.num)
        if handle_ban:
            print('不想写跳过验证了')
            # self._browser = self._init_browser()
            # self._handle_ban()

    def run(self):
        self._css_link = self._get_css_link(self._cur_request_url)
        self._font_dict = self._get_font_dict(self._css_link)
        self._get_conment_page()


    def _delay_func(self):
        delay_time = random.randint((self._delay - 2) * 10, (self._delay + 2) * 10) * 0.1
        time.sleep(delay_time)

    def _init_browser(self):
        """
            初始化游览器
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(self._cur_request_url)
        for name, value in self._cookies.items():
            browser.add_cookie({'name': name, 'value': value})
        browser.refresh()
        return browser

    def _handle_ban(self):
        """
            爬取速度过快，出现异常时处理验证
        """
        try:
            self._browser.refresh()
            time.sleep(1)
            button = self._browser.find_element_by_id('yodaBox')
            move_x_offset = self._browser.find_element_by_id('yodaBoxWrapper').size['width']
            webdriver.ActionChains(self._browser).drag_and_drop_by_offset(
                button, move_x_offset, 0).perform()
        except:
            pass

    def _format_cookies(self, cookies):
        cookies = {cookie.split('=')[0]: cookie.split('=')[1]
                   for cookie in cookies.replace(' ', '').split(';')}
        return cookies

    def _get_conment_page(self):
        """
            请求评论页，并将<span></span>样式替换成文字
        """
        while self._cur_request_url:
            self._delay_func()
            print('[{now_time}] {msg}'.format(now_time=datetime.datetime.now(), msg=self._cur_request_url))

            res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=self._cookies)
            while res.status_code !=200:
                cookie = random.choice(COOKIES)
                cookies = self._format_cookies(cookie)
                res = requests.get(self._cur_request_url, headers=self._default_headers, cookies=cookies)
                if res.status_code == 200:
                    break

            html = res.text
            class_set = set()
            for span in re.findall(r'<span class="([a-zA-Z0-9]{5,6})"></span>', html):
                class_set.add(span)
            for class_name in class_set:
                try:
                    html = re.sub('<span class="%s"></span>' % class_name, self._font_dict[class_name], html)

                except:
                    html = re.sub('<span class="%s"></span>' % class_name, '', html)
            doc = etree.HTML(str(html))

            self._parse_comment_page(doc)

            try:
                self._default_headers['Referer'] = self._cur_request_url
                next_page_url = 'http://www.dianping.com' + doc.xpath('.//a[@class="NextPage"]/@href')[0]
                print('next_url:{}'.format(next_page_url))
            except IndexError:
                next_page_url = None
            print('next_page_url:{}'.format(next_page_url))
            self._cur_request_url = next_page_url
            # self.num = self.num + 1


    def _data_pipeline(self, data):
        """
            处理数据
        """
        print(data)

    def _parse_comment_page(self, doc):
        """
            解析评论页并提取数据
        """
        for li in doc.xpath('//*[@class="reviews-items"]/ul/li'):



                if li.xpath('.//a[@class="name"]/text()'):
                    name = li.xpath('.//a[@class="name"]/text()')[0].strip('\n\r \t')
                else:
                    name = li.xpath('.//span[@class="name"]/text()')[0].strip('\n\r \t')

                try:
                    star = li.xpath('.//span[contains(./@class, "sml-str")]/@class')[0]
                    star = re.search(r'sml-str(\d+)', star)[1]
                except IndexError:
                    star = 0
                time = li.xpath('.//span[@class="time"]/text()')[0].strip('\n\r \t')
                score = ' '.join(map(lambda s: s.strip('\n\r \t'), li.xpath('.//span[@class="score"]//text()')))
                comment = ''.join(li.xpath('.//div[@class="review-words Hide"]/text()')).strip('\n\r \t')
                if not comment:
                    comment = ''.join(li.xpath('.//div[@class="review-words"]/text()')).strip('\n\r \t')
                data = {
                    'name': name,
                    'comment': comment,
                    'star': star,
                    'score': score,
                    'time': time,
                }
                # if comments.find_one({'name':name}):
                #     print('Insert  Error!')
                # else:
                #     comments.insert(data)
                #     print(data)
                self._data_pipeline(data)



    def _get_css_link(self, url):
        """
            请求评论首页，获取css样式文件
        """
        try:
            print(url)
            res = requests.get(url, headers=self._default_headers, cookies=self._cookies)
            html = res.text
            css_link = re.search(r'<link re.*?css.*?href="(.*?svgtextcss.*?)">', html)
            print(css_link)
            assert css_link
            css_link = 'http:' + css_link[1]

            return css_link
        except:
            None

    def _get_font_dict(self, url):
        """
            获取css样式对应文字的字典
        """
        res = requests.get(url, headers=self._css_headers)
        html = res.text
        print(html)
        background_image_link = re.search(r'background-image:.*?\((.*?svg)\)', html)
        assert background_image_link
        background_image_link = 'http:' + background_image_link[1]
        print('----------' * 40)
        print(background_image_link)
        print('---------------' * 40)
        html = re.sub(r'span.*?\}', '', html)
        group_offset_list = re.findall(r'\.([a-zA-Z0-9]{5,6}).*?round:(.*?)px (.*?)px;', html)
        font_dict_by_offset = self._get_font_dict_by_offset(background_image_link)
        font_dict = {}
        for class_name, x_offset, y_offset in group_offset_list:
            x_offset = x_offset.replace('.0', '')
            y_offset = y_offset.replace('.0', '')


            try:
                font_dict[class_name] = font_dict_by_offset[int(y_offset)][int(x_offset)]

            except:
                font_dict[class_name] = ''
        return font_dict

    def _get_font_dict_by_offset(self, url):
        """
            获取坐标偏移的文字字典, 会有最少两种形式的svg文件（目前只遇到两种）
        """
        res = requests.get(url, headers=self._css_headers)
        html = res.text
        font_dict = {}
        y_list = re.findall(r'd="M0 (\d+?) ', html)
        if y_list:
            font_list = re.findall(r'<textPath .*?>(.*?)<', html)
            for i, string in enumerate(font_list):
                y_offset = self.start_y - int(y_list[i])

                sub_font_dict = {}
                for j, font in enumerate(string):
                    x_offset = -j * self.font_size
                    sub_font_dict[x_offset] = font

                font_dict[y_offset] = sub_font_dict

        else:
            font_list = re.findall(r'<text.*?y="(.*?)">(.*?)<', html)

            for y, string in font_list:
                y_offset = self.start_y - int(y)
                sub_font_dict = {}
                for j, font in enumerate(string):
                    x_offset = -j * self.font_size
                    sub_font_dict[x_offset] = font

                font_dict[y_offset] = sub_font_dict
        print(font_dict)




        return font_dict



class Customer(DianpingComment):
    def _data_pipeline(self, data):

        print(data)




if __name__ == "__main__":
    dianping = Customer('4114867', cookies=COOKIES)
    dianping.run()
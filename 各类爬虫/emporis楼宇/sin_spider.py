"""
参数带完整了 拿不到数据 content-lenth 为空
"""
import time

import pymysql
import requests
from bs4 import BeautifulSoup

from schedule.chaojiying import Chaojiying_Client


class SinSpider:
    def __init__(self, booking):
        self.booking = booking
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='123456',
                                  db='gdy')
        self.db.autocommit(True)  # 设置自动commit
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)  # 设置返回的结果集用字典来表示，默认是元祖
        # 设置是否打印调试语句 1→开启  0→关闭
        self.debug_flag = 1
        self.chaojiying = Chaojiying_Client('gdy8888', 'Gdy****8888',
                                            'bf0834722c1a6dbe859dc46a05397f1e')  # 用户中心>>软件ID 生成一个替换 96001
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'ebusiness.sinolines.com.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        res = requests.get(url='http://ebusiness.sinolines.com.cn/snlebusiness/TrackingCargoByBlno.aspx',
                           headers=headers)
        # res = requests.get(url='http://m.sinolines.com.cn/m/iTrackingByBlno.aspx', headers=headers)
        soup = BeautifulSoup(res.content, 'lxml')
        self.eventtarget = soup.select('#__EVENTTARGET')[0].attrs['value']
        self.eventargument = soup.select('#__EVENTARGUMENT')[0].attrs['value']
        self.viewstate = soup.select('#__VIEWSTATE')[0].attrs['value']
        self.viewstategenerator = soup.select('#__VIEWSTATEGENERATOR')[0].attrs['value']
        self.scrollpositionx = soup.select('#__SCROLLPOSITIONX')[0].attrs['value']
        self.scrollpositiony = soup.select('#__SCROLLPOSITIONY')[0].attrs['value']
        self.viewstateencrypted = soup.select('#__VIEWSTATEENCRYPTED')[0].attrs['value']
        self.eventvalidation = soup.select('#__EVENTVALIDATION')[0].attrs['value']
        self.cookie = res.headers['Set-Cookie'].split(';')[0]
        print(self.cookie)

    def run(self):
        self.debugging('run      ↓↓↓↓↓↓↓↓↓↓↓↓        单号 {}'.format(self.booking))
        datas = self.parse()
        return None

    # 解析页面拿到所有数据
    def parse(self):
        self.debugging('parse        ↓↓↓↓↓↓↓↓↓↓↓↓↓↓')
        code_res = self.captcha()
        while code_res['err_str'] != 'OK':
            print('验证码重试')
            code_res = self.captcha()
        pic_str = code_res['pic_str']
        print(pic_str)
        pic_id = code_res['pic_id']
        url = 'http://ebusiness.sinolines.com.cn/snlebusiness/TrackingCargoByBlno.aspx'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '27835',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '{}'.format(self.cookie),
            'Host': 'ebusiness.sinolines.com.cn',
            'Origin': 'http://ebusiness.sinolines.com.cn',
            'Referer': 'http://ebusiness.sinolines.com.cn/snlebusiness/TrackingCargoByBlno.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        data = {
            '__EVENTTARGET:': '{}'.format(self.eventtarget),
            '__EVENTARGUMENT:': '{}'.format(self.eventvalidation),
            '__VIEWSTATE': '{}'.format(self.viewstate),
            '__VIEWSTATEGENERATOR': '{}'.format(self.viewstategenerator),
            '__SCROLLPOSITIONX': '{}'.format(self.scrollpositionx),
            '__SCROLLPOSITIONY': '{}'.format(self.scrollpositiony),
            '__VIEWSTATEENCRYPTED:': '{}'.format(self.viewstateencrypted),
            '__EVENTVALIDATION': '{}'.format(self.eventvalidation),
            'dl_seltype': 'blno',
            'TbBlno': self.booking,
            'ValidateCodeTXT': pic_str,
            'BlnoListRetrieveBT': '查询'
        }
        response = requests.post(url=url, headers=headers, data=data)
        print('请求页面')
        print(headers)
        print(data)
        print(response.status_code)
        print(response.cookies)
        print(response.headers)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')
        print(soup.prettify())

    def captcha(self):
        url = 'http://ebusiness.sinolines.com.cn/snlebusiness/ValidateImage.aspx'
        # url = 'http://m.sinolines.com.cn/m/iValidateImage.aspx'
        headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': '{}'.format(self.cookie),
            'Host': 'ebusiness.sinolines.com.cn',
            'Referer': 'http://ebusiness.sinolines.com.cn/snlebusiness/TrackingCargoByBlno.aspx',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        print(headers)
        response = requests.get(url=url, headers=headers)
        print(response.headers)
        print(response.cookies)
        now_time = int(time.time())
        with open('{}{}.png'.format(self.booking, now_time), 'wb') as f:
            f.write(response.content)
        im = open('{}{}.png'.format(self.booking, now_time), 'rb').read()
        code_res = self.chaojiying.PostPic(im, 1902)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        return code_res

    # 调试语句
    def debugging(self, string):
        (lambda x, y: print(y) if x else None)(self.debug_flag, string)


if __name__ == '__main__':
    SinSpider('SNL9CQKX0000015').run()

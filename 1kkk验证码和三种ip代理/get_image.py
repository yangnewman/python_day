import time
import random
import pymysql

from urllib.parse import quote

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class GetImage():
    def __init__(self):
        self.url = 'http://www.1kkk.com/image3.ashx?t=1540801567000'
        self.headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
        }

    def response(self):
        response = requests.get(self.url, headers=self.headers)
        # text = response.content.decode('urf-8')
        return response

    def write_images(self, num):
        filename = 'image0%s.jpg' % num
        with open('./images01/%s' % filename, 'wb') as f:
            r = requests.get(self.url)
            f.write(r.content)

    def main(self):
        html = self.response()
        for i in range(10):
            print(i)
            self.write_images(i)
        print(html)


if __name__ == '__main__':
    image = GetImage()
    image.main()




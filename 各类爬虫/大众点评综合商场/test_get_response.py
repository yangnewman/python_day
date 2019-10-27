from random import choice

import requests
from lxml import etree


def get_one_page(url):
    headers = {'Host': 'www.dianping.com',
               'Referer': 'http://www.dianping.com',
               # 'Referer': url,
               'Upgrade-Insecure-Requests': '1',
               'Connection': 'keep-alive'}
    headers_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36']
    headers['User-Agent'] = choice(headers_list)
    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(response.status_code)
        if response.status_code == 200:
            text = response.content.decode('utf-8')
            return text
    except:
        print('得不到响应')
        return None


def test_response():
    url = 'http://www.dianping.com/wuhan/ch20/g119p12'
    html = get_one_page(url)
    print(html)
    # shop_etree = etree.HTML(html)
    # logo = shop_etree.xpath('//div[@id="not-found-tip"]')
    # if logo:
    #     text = logo[0].xpath('text()')
    #     print(text)


if __name__ == '__main__':
    test_response()

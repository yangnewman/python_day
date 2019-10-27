import re
from random import choice

import requests


def get_info_response(url):
    with open('ip.txt') as f:
        ip_list = f.readlines()
        ip_list = [i.strip() for i in ip_list]
        if ip_list:
            ip = choice(ip_list)
            print(ip)
            proxies = {
                'http': 'http://' + ip}
            headers = {'Host': 'www.dianping.com',
                       'Referer': 'http://www.dianping.com/',
                       'Upgrade-Insecure-Requests': '1',
                       'Connection': 'keep-alive'}
            headers_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36']
            headers['User-Agent'] = choice(headers_list)
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            print(response.headers)


def getCookie(url):
    response = requests.post(url)
    set_cookie = response.headers['Set-Cookie']
    array = re.split('[;,]',set_cookie)
    cookieValue = ''
    for arr in array:
        if arr.find('DZSW_SESSIONID') >= 0 or arr.find('bl0gm1HBTB') >= 0:
            cookieValue += arr + ';'
    print(cookieValue)


if __name__ == '__main__':
    # a, b = -112.2331233235, -36.29567892397
    url = 'http://www.dianping.com/chengdu/ch20/g119p2'
    url2 = 'http://www.dianping.com/shop/128566696'
    get_info_response(url)
    # getCookie(url2)





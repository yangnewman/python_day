import json
from random import choice

import requests


def get_zhima_ip():
    url = 'http://webapi.http.zhimacangku.com/getip?num=2&type=2&pro=0&city=0&yys=0&port=1&pack=56316&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
    headers = {}
    headers_list = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']
    headers['User-Agent'] = choice(headers_list)
    try:
        response = requests.get(url, headers=headers)
        # print(response)
        if response.status_code == 200:
            text = response.content.decode('utf-8')
            path = 'ip.txt'
            json_html = json.loads(text)
            print(json_html)
            if json_html['success']:
                for ip_dict in json_html['data']:
                    ip = ip_dict['ip'] + ':' + str(ip_dict['port'])
                    write(path=path, text=ip)
                return
    except:
        return None


def write(path,text):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')


if __name__ == '__main__':
    get_zhima_ip()
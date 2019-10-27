
import requests
from random import choice
from pybloom_live import BloomFilter

def get_one_page(url):
    headers = {"User-Agent": ""}
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
        if response.status_code == 200:
            text = response.content.decode('utf-8')
            return text
    except:
        return None


def test02():
    for _ in range(3):
        print(bloom.add(3))
        print(bloom.add(21))
        print(bloom.add(21))
        yield bloom


if __name__ == '__main__':
    # url = 'http://www.66ip.cn/'
    # html = get_one_page(url)
    # print(html)
    a = [i for i in range(20)]
    bloom = BloomFilter(500000, 0.000001)
    for i in a:
        bloom.add(i)
    b = test02()
    for i in b:
        print('sss')


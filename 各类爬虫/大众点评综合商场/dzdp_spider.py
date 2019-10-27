import ast
import json
import re
import sqlite3
from random import choice
from threading import Thread

from lxml import etree
import requests
from pybloom_live import BloomFilter

from get_lng_lat import get_gaode_lng_lat
from lng_lat_to_gps import transfer
from proxy_ip import get_zhima_ip


def get_one_page(url):
    with open('ip.txt') as f:
        ip_list = f.readlines()
        ip_list = [i.strip() for i in ip_list]
        if ip_list:
            ip = choice(ip_list)
            print(ip)
            proxies = {
                'http': 'http://' + ip}
            headers = {'Host': 'www.dianping.com',
                       'Referer': 'www.dianping.com',
                       'Upgrade-Insecure-Requests': '1',
                       'Connection': 'keep-alive'}
            # headers_list = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            #                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            #                 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            #                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
            #                 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
            #                 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0']
            headers_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36']
            headers['User-Agent'] = choice(headers_list)
            try:
                # first_response = requests.get('http://www.dianping.com', headers=headers, proxies=proxies)
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                # print(first_response.status_code)
                print(response.status_code)
                if response.status_code == 200:
                    text = response.content.decode('utf-8')
                    etree_t = etree.HTML(text)
                    url_true = etree_t.xpath('//div[@id="logo"]')
                    print(url_true)
                    if url_true:
                        print('这个IP需要验证，再重试')
                        print(text)
                        ip_list.remove(ip)
                        with open('ip.txt', 'w') as f2:
                            for write_ip in ip_list:
                                f2.writelines(write_ip)
                                f2.write('\n')
                        text = get_one_page(url)
                        return text
                    else:
                        return text
                else:
                    ip_list.remove(ip)
                    with open('ip.txt', 'w') as f2:
                        for write_ip in ip_list:
                            f2.writelines(write_ip)
                            f2.write('\n')
                    text = get_one_page(url)
                    return text
            except:
                print('得不到响应')
                ip_list.remove(ip)
                with open('ip.txt', 'w') as f2:
                    for write_ip in ip_list:
                        f2.writelines(write_ip)
                        f2.write('\n')
                text = get_one_page(url)
                return text
        else:
            print('添加新IP')
            get_zhima_ip()
            text = get_one_page(url)
            return text


def get_info_response(url, city, refer_url):
    with open('ip.txt') as f:
        ip_list = f.readlines()
        ip_list = [i.strip() for i in ip_list]
        if ip_list:
            ip = choice(ip_list)
            print(ip)
            proxies = {
                'http': 'http://' + ip}
            # headers = {}
            headers = {
                        'Host': 'www.dianping.com',
                        'Referer': refer_url,
                        'Upgrade-Insecure-Requests': '1',
                        'Connection': 'keep-alive'}
                        # 'Cookie': 's_ViewType=10;'}
            headers_list = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36']
            headers['User-Agent'] = choice(headers_list)
            try:
                response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
                if response.status_code == 200:
                    text = response.content.decode('utf-8')
                    etree_t = etree.HTML(text)
                    url_true = etree_t.xpath('//div[@id="logo"]')
                    print(url_true)
                    if url_true:
                        print('这个IP需要验证，再重试')
                        print(text)
                        ip_list.remove(ip)
                        with open('ip.txt', 'w') as f2:
                            for write_ip in ip_list:
                                f2.writelines(write_ip)
                                f2.write('\n')
                        text = get_info_response(url, city, refer_url)
                        return text
                    else:
                        return text
                else:
                    print('状态码不是200')
                    print(response.status_code)
                    text = response.content.decode('utf-8')
                    print(text)
                    ip_list.remove(ip)
                    with open('ip.txt', 'w') as f2:
                        for write_ip in ip_list:
                            f2.writelines(write_ip)
                            f2.write('\n')
                    text = get_info_response(url, city, refer_url)
                    return text
            except:
                print('得不到响应')
                ip_list.remove(ip)
                with open('ip.txt', 'w') as f2:
                    for write_ip in ip_list:
                        f2.writelines(write_ip)
                        f2.write('\n')
                text = get_info_response(url, city, refer_url)
                return text
        else:
            print('添加新IP')
            get_zhima_ip()
            text = get_info_response(url, city, refer_url)
            return text


def get_shop_url():
    bloom = BloomFilter(200000, 0.000001)
    db = sqlite3.connect('shop_data.db')
    cursor = db.cursor()
    sql = 'select shop_url from dzdp_shop'
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    db.close()
    for data in datas:
        bloom.add(data[0])
    return bloom


def write_db(items):
    db = sqlite3.connect('shop_data.db')
    numb = 0
    cursor = db.cursor()
    for item in items:
        table = 'dzdp_shop'
        keys = ', '.join(item.keys())
        values = ', '.join(['?'] * len(item))
        sql = "REPLACE INTO {table}({keys}) VALUES ({values})".format(table=table, keys=keys, values=values)
        try:
            if cursor.execute(sql, tuple(item.values())):
                print('Success')
                db.commit()
                numb += 1
        except:
            print('Failed')
            db.rollback()
    cursor.close()
    db.close()
    return numb


def parse_page_response(html, url, bloom, city):
    etree_city = etree.HTML(html)
    next_page = etree_city.xpath('//a[@title="下一页"]')
    print(next_page)
    if next_page:
        page = etree_city.xpath('//div[@class="page"]/a[last()-1]/text()')[0]
        print(page)
        page_last = int(page)
    else:
        page_last = 1
    shop_url_list = one_page_shop_url(page_last, url)
    for shop_url in shop_url_list:
        # print(shop_url)
        if not bloom.add(shop_url):
            shop_dict = {}
            shop_dict['shop_url'] = shop_url
            shop_html = get_info_response(shop_url, city, url)
            # print(shop_html)
            etree_shop = etree.HTML(shop_html)
            # 省份和城市
            province_and_city = etree_shop.xpath('//meta[@name="location"]/@content')
            # print(province_and_city)
            if province_and_city:
                province = province_and_city[0].split(';')[0].split('=')[-1]
                # print(province)
                city = province_and_city[0].split(';')[1].split('=')[-1]
                # print(city)
                shop_dict['shop_province'] = province
                shop_dict['shop_city'] = city
            # 评论、消费、设施、环境、服务
            num_dict = {'&#xec2d;': '0', '无': '1', '&#xe4ff;': '2', '&#xf70d;': '3', '&#xe6ec;': '4',
                        '&#xf404;': '5', '&#xe65d;': '6', '&#xe284;': '7', '&#xf810;': '8', '&#xe27b;': '9'}
            # 评论
            shop_comment_info_1 = re.compile('<span id="reviewCount" class="item"(.*?)/span>', re.S)
            shop_comment_info_list_1 = re.findall(shop_comment_info_1, shop_html)
            # print(shop_comment_info_list_1)
            if shop_comment_info_list_1:
                shop_comment_info_2 = re.compile('>(.*?)<', re.S)
                shop_comment_info_list_2 = re.findall(shop_comment_info_2, shop_comment_info_list_1[0])
                # print(shop_comment_info_list_2)
                shop_comment_info_list = [num_dict[com] if com in num_dict else com.strip() for com in shop_comment_info_list_2]
                # print(shop_comment_info_list)
                shop_comment = ''.join(shop_comment_info_list).split('条')[0]
                shop_dict['shop_comment'] = shop_comment
                # print(shop_comment)
            # 消费
            shop_consume_info_1 = re.compile('<span id="avgPriceTitle" class="item"(.*?)/span>', re.S)
            shop_consume_info_list_1 = re.findall(shop_consume_info_1, shop_html)
            # print(shop_consume_info_list_1)
            if shop_consume_info_list_1:
                shop_consume_info_2 = re.compile('>(.*?)<', re.S)
                shop_consume_info_list_2 = re.findall(shop_consume_info_2, shop_consume_info_list_1[0])
                # print(shop_consume_info_list_2)
                shop_consume_info_list = [num_dict[com] if com in num_dict else com.strip() for com in
                                          shop_consume_info_list_2]
                # print(shop_consume_info_list)
                shop_consume = ''.join(shop_consume_info_list).split(':')[-1].strip()
                shop_dict['shop_consume'] = shop_consume
                # print(shop_consume)
            # 设施、环境、服务
            shop_quality_info_1 = re.compile('<span id="comment_score">(.*?)</div>', re.S)
            shop_quality_info_list_1 = re.findall(shop_quality_info_1, shop_html)
            # print(shop_quality_info_list_1)
            # print(len(shop_quality_info_list_1))
            if shop_quality_info_list_1:
                shop_quality_info_2 = re.compile('>(.*?)<', re.S)
                shop_quality_info_list_2 = re.findall(shop_quality_info_2, shop_quality_info_list_1[0])
                # print(shop_quality_info_list_2)
                # shop_info_list = [info.strip() for info in shop_quality_info_list_2 if info.strip()]
                shop_info_list = [num_dict[com] if com in num_dict else com.strip() for com in shop_quality_info_list_2]
                # print(shop_info_list)
                shop_info = ''.join(shop_info_list)
                # print(shop_info)
                # 设施
                shop_quality = shop_info.split(':')[1].split('环境')[0]
                # print(shop_quality)
                # 环境
                shop_env = shop_info.split(':')[2].split('服务')[0]
                # print(shop_env)
                # 服务
                shop_service = shop_info.split(':')[-1]
                # print(shop_service)
                shop_dict['shop_quality'] = shop_quality
                shop_dict['shop_env'] = shop_env
                shop_dict['shop_service'] = shop_service
            # 获取商场名字、地址、星级、图片
            get_some_shop = re.compile('window.shop_config=(.*?) </script>', re.S)
            shop_some_info_list = re.findall(get_some_shop, shop_html)
            # print(shop_some_info_list)
            if shop_some_info_list:
                shop_some_info = shop_some_info_list[0]
                # print(shop_some_info)
                # 商场名称
                shop_name = re.compile('shopName: "(.*?)",', re.S)
                shop_name_list = re.findall(shop_name, shop_some_info)
                if shop_name_list:
                    shop_name = shop_name_list[0]
                    shop_dict['shop_name'] = shop_name
                    # print(shop_name)
                # 星级
                shop_level = re.compile('shopPower:(.*?),', re.S)
                shop_level_list = re.findall(shop_level, shop_some_info)
                if shop_level_list:
                    shop_level = shop_level_list[0]
                    shop_dict['shop_level'] = shop_level
                    # print(shop_level)
                # 地址
                shop_address = re.compile('address: "(.*?)",', re.S)
                shop_address_list = re.findall(shop_address, shop_some_info)
                if shop_address_list:
                    shop_address = shop_address_list[0]
                    shop_dict['shop_address'] = shop_address
                    if shop_address:
                        shop_dict['g_longitude'], shop_dict['g_latitude'] = get_gaode_lng_lat(province, city, shop_address, shop_name)
                        tr = transfer()
                        shop_dict['gps_longitude'], shop_dict['gps_latitude'] = tr.gcj02_to_wg84(float(shop_dict['g_longitude']), float(shop_dict['g_latitude']))
                # 图片
                shop_image = re.compile('defaultPic:"(.*?)",', re.S)
                shop_image_list = re.findall(shop_image, shop_some_info)
                if shop_image_list:
                    shop_image = shop_image_list[0]
                    shop_dict['shop_image'] = shop_image
                    # print(shop_image)
            # print(shop_dict)
            yield shop_dict


def one_page_shop_url(page_last, url):
    # for page in range(1, page_last+1):
    #     url += f'p{page}'
    url += f'p{1}'
    html = get_one_page(url)
    # print(html)
    etree_one_page_shop = etree.HTML(html)
    shop_url_list = etree_one_page_shop.xpath('//div[@class="pic"]/a/@href')
    print(shop_url_list)
    for shop_url in shop_url_list:
        print(shop_url)
        yield shop_url


def get_first_url():
    url = 'http://www.dianping.com/citylist'
    html = get_info_response(url)
    # print(html)
    city_name_list = parse_city_url(html)
    return city_name_list


def parse_city_url(html):
    etree_html = etree.HTML(html)
    city_url_list2 = ['hongkong', 'macau', 'taipei']
    city_url_list = etree_html.xpath('//div[@class="findHeight"]/a/@href')
    city_url_list = [url.split('/')[-1] for url in city_url_list]
    city_url_list += city_url_list2
    print(city_url_list)
    print(len(city_url_list))
    return city_url_list


def start_thread():
    bloom = get_shop_url()
    city_name_list = get_first_url()
    city_urls = [city_name_list[i:i + 235] for i in range(0, len(city_name_list), 235)]
    # print(city_urls)
    # print(len(city_urls))
    threads = []
    for name_list in city_urls:
        # print(len(urls))
        t = Thread(target=start_shop_spider, args=(name_list, bloom))
        t.start()
        threads.append(t)
    # 先执行完所有线程再执行主进程
    for t in threads:
        t.join()
    print('大众点评爬取完毕！！')


def start_shop_spider():
    # for city_name in name_list:
    city_name = 'wuhan'
    bloom = get_shop_url()
    url = f'http://www.dianping.com/{city_name}/ch20/g119'
    shop_page_html = get_one_page(url)
    # print(shop_page_html)
    items = parse_page_response(shop_page_html, url, bloom, city_name)
    num = write_db(items)
    print(f'这个城市更新了{num}条商家')


if __name__ == '__main__':
    # get_first_url()
    start_shop_spider()
    # start_thread()











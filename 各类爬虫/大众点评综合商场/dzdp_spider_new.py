import ast
import json
import re
import sqlite3
from random import choice
from threading import Thread

from lxml import etree
import requests
from pybloom_live import BloomFilter

from get_lng_lat import get_gaode_lng_lat, get_province_city
from lng_lat_to_gps import transfer
from proxy_ip import get_zhima_ip


def get_one_page(url):
    with open('ip.txt') as f:
        ip_list = f.readlines()
        ip_list = [i.strip() for i in ip_list]
        if ip_list:
            ip = choice(ip_list)
            print(ip)
        else:
            print('添加新IP')
            get_zhima_ip()
            text = get_one_page(url)
            return text
    proxies = {
        'http': 'http://' + ip,
        'https': 'https://' + ip}
    headers = {'Host': 'www.dianping.com',
               'Referer': 'http://www.dianping.com',
               # 'Referer': url,
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
            # print(url_true)
            if url_true:
                print('这个IP需要验证，再重试')
                # print(text)
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
        # print(item)
        table = 'dzdp_shop'
        keys = ', '.join(item.keys())
        values = ', '.join(['?'] * len(item))
        sql = "INSERT INTO {table}({keys}) VALUES ({values})".format(table=table, keys=keys, values=values)
        # print(sql)
        try:
            if cursor.execute(sql, tuple(item.values())):
                db.commit()
                print('Success')
                numb += 1
        except:
            print('Failed')
            db.rollback()
    cursor.close()
    db.close()
    return numb


def parse_page_response(html, url, bloom, shop_info):
    etree_city = etree.HTML(html)
    next_page = etree_city.xpath('//a[@title="下一页"]')
    # print(next_page)
    if next_page:
        page = etree_city.xpath('//div[@class="page"]/a[last()-1]/text()')[0]
        # print(page)
        page_last = int(page)
    else:
        page_last = 1
    print(f'这个城市有{page_last}页')
    # shop_url_list = one_page_shop_url(page_last, url)
    for page in range(1, page_last + 1):
        page_url = url + f'p{page}'
        shop_html = get_one_page(page_url)
        etree_one_page_shop = etree.HTML(shop_html)
        li_list = etree_one_page_shop.xpath('//div[@id="shop-all-list"]/ul/li')
        print(len(li_list))
        if not li_list:
            continue
        for index, li in enumerate(li_list):
            shop_dict = {}
            # 链接
            shop_url = li.xpath('div[@class="pic"]/a/@href')
            # print(shop_url[0])
            if not bloom.add(shop_url[0]):
                shop_dict['shop_url'] = shop_url[0]
                # 省份
                shop_dict['shop_province'] = shop_info[0]
                # print(shop_dict['shop_province'])
                # 城市
                shop_dict['shop_city'] = shop_info[1]
                # print(shop_dict['shop_city'])
                # 点评给的城市
                shop_dict['shop_city_dp'] = shop_info[2]
                # print(shop_dict['shop_city_dp'])
                # 名字
                shop_name = li.xpath('div[@class="pic"]/a/img/@title')
                print(shop_name)
                if shop_name:
                    shop_dict['shop_name'] = shop_name[0]
                # 地址
                shop_address = li.xpath('div[@class="operate J_operate Hide"]/a[2]/@data-address')
                # print(shop_address)
                if shop_address:
                    shop_dict['shop_address'] = shop_address[0]
                # 图片
                shop_pic = li.xpath('div[@class="pic"]/a/img/@data-src')
                # print(shop_pic)
                if shop_pic:
                    shop_dict['shop_image'] = shop_pic[0]
                # 等级
                shop_level = li.xpath('div[@class="txt"]/div[@class="comment"]/span/@title')
                # print(shop_level)
                if shop_level:
                    shop_dict['shop_level'] = shop_level[0]
                # 点评数
                shop_comment_info = re.compile('<a .*? data-click-name="shop_iwant_review_click".*?>(.*?)</a>', re.S)
                shop_comment_info_list = re.findall(shop_comment_info, shop_html)
                # print(shop_comment_info_list)
                # print(len(shop_comment_info_list))
                if shop_comment_info_list:
                    num_str = shop_comment_info_list[index].strip()
                    # print(num_str)
                    if '<b>' in num_str:
                        shop_comment_info2 = re.compile('<b>(.*?)</b>', re.S)
                        shop_comment_info_list2 = re.findall(shop_comment_info2, num_str)
                        shop_comment = get_replace_num(shop_comment_info_list2[0])
                        shop_dict['shop_comment'] = shop_comment
                        # print(shop_comment)
                # 消费
                shop_consume_info1 = re.compile('<a .*? class="mean-price".*?>(.*?)</span>', re.S)
                shop_consume_info_list1 = re.findall(shop_consume_info1, shop_html)
                if shop_consume_info_list1:
                    shop_consume_info2 = re.compile('<b>(.*?)</b>', re.S)
                    shop_consume_info_list2 = re.findall(shop_consume_info2, shop_consume_info_list1[index])
                    # print(shop_consume_info_list2)
                    # print(len(shop_consume_info_list2))
                    if shop_consume_info_list2:
                        num_str = shop_consume_info_list2[0]
                        shop_consume = get_replace_num(num_str)
                        shop_dict['shop_consume'] = shop_consume
                        # print(shop_consume)
                # 部分打分
                shop_some_info1 = re.compile('<span class="addr">(.*?)<div class="operate J_operate Hide">', re.S)
                shop_some_info_list1 = re.findall(shop_some_info1, shop_html)
                # print(shop_some_info_list1)
                # print(len(shop_some_info_list1))
                if shop_some_info_list1:
                    some_info_str = shop_some_info_list1[index].strip()
                    # print(some_info_str)
                    if '<b>' in some_info_str:
                        # 质量
                        shop_quality_info = re.compile('<span >质量(.*?)</span>', re.S)
                        shop_quality_info_list = re.findall(shop_quality_info, some_info_str)
                        shop_quality = get_replace_num(shop_quality_info_list[0])
                        shop_dict['shop_quality'] = shop_quality
                        # print(shop_quality)
                        # 环境
                        shop_env_info = re.compile('<span >环境(.*?)</span>', re.S)
                        shop_env_info_list = re.findall(shop_env_info, some_info_str)
                        shop_env = get_replace_num(shop_env_info_list[0])
                        shop_dict['shop_env'] = shop_env
                        # print(shop_env)
                        # 服务
                        shop_service_info = re.compile('<span >服务(.*?)</span>', re.S)
                        shop_service_info_list = re.findall(shop_service_info, some_info_str)
                        shop_service = get_replace_num(shop_service_info_list[0])
                        shop_dict['shop_service'] = shop_service
                        # print(shop_service)
                # 经纬度
                try:
                    address = shop_info[0] + shop_info[1] + shop_dict['shop_address'] + shop_dict['shop_name']
                except:
                    address = shop_info[2] + shop_dict['shop_address'] + shop_dict['shop_name']
                shop_dict['g_longitude'], shop_dict['g_latitude'] = get_gaode_lng_lat(address)
                tr = transfer()
                shop_dict['gps_longitude'], shop_dict['gps_latitude'] = tr.gcj02_to_wg84(float(shop_dict['g_longitude']), float(shop_dict['g_latitude']))
                # print(shop_dict)
                if shop_name[0] == '紫金源购物广场':
                    print(shop_dict)
                yield shop_dict


def get_replace_num(num_str):
    num_str = num_str.replace('￥', '')
    num_str = num_str.replace('<b>', '')
    num_str = num_str.replace('</b>', '')
    num_str = num_str.replace('<svgmtsi class="ehrrn5"></svgmtsi>', '0')
    num_str = num_str.replace('<svgmtsi class="ehr146"></svgmtsi>', '2')
    num_str = num_str.replace('<svgmtsi class="ehr1oj"></svgmtsi>', '3')
    num_str = num_str.replace('<svgmtsi class="ehrnt7"></svgmtsi>', '4')
    num_str = num_str.replace('<svgmtsi class="ehryf0"></svgmtsi>', '5')
    num_str = num_str.replace('<svgmtsi class="ehr8ys"></svgmtsi>', '6')
    num_str = num_str.replace('<svgmtsi class="ehrd2x"></svgmtsi>', '7')
    num_str = num_str.replace('<svgmtsi class="ehrz7r"></svgmtsi>', '8')
    num_str = num_str.replace('<svgmtsi class="ehr2kb"></svgmtsi>', '9')
    return num_str


def get_first_url():
    url = 'http://www.dianping.com/citylist'
    html = get_one_page(url)
    # print(html)
    city_url_list, city_name_list = parse_city_url(html)
    return city_url_list, city_name_list


def parse_city_url(html):
    etree_html = etree.HTML(html)
    city_list2 = ['hongkong', 'macau', 'taipei']
    city_list3 = ['香港', '澳门', '台北']
    city_url_list = etree_html.xpath('//div[@class="findHeight"]/a/@href')
    # # print(city_url_list)
    city_url_list = [url.split('/')[-1] for url in city_url_list]
    # print(len(city_url_list))
    city_name_list = etree_html.xpath('//div[@class="findHeight"]/a/text()')
    # print(city_name_list)
    # print(len(city_name_list))
    city_name_list += city_list3
    city_url_list += city_list2
    # print(city_url_list)
    # print(len(city_url_list))
    return city_url_list, city_name_list


def get_shop_name():
    db = sqlite3.connect('shop_data.db')
    cursor = db.cursor()
    sql = 'select distinct shop_city_dp from dzdp_shop'
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    db.close()
    filter_list = []
    for data in datas:
        filter_list.append(data[0])
    return filter_list


def get_filter_name(list_url, list_name):
    filter_list = get_shop_name()
    print(filter_list)
    # filter_list = []
    print(list_url)
    print(list_name)
    list3 = []
    for index, li_list in enumerate(list_name):
        li_list2 = li_list[::-1]
        index2 = 0
        for shop_name in li_list2:
            if shop_name in filter_list:
                index2 = li_list.index(shop_name)
                break
        if index2:
            li_list = list_url[index][index2:]
        else:
            li_list = list_url[index]
        # print(li_list)
        list3.append(li_list)
    return list3


def start_thread():
    bloom = get_shop_url()
    city_url_list, city_name_list = get_first_url()
    city_url_list = [city_url_list[i:i + 800] for i in range(0, len(city_url_list), 800)]
    city_name_list = [city_name_list[i:i + 800] for i in range(0, len(city_name_list), 800)]
    # print(city_urls)
    # print(len(city_urls))
    city_urls = get_filter_name(city_url_list, city_name_list)
    # city_urls = [city_urls[0]]
    for city in city_urls:
        print(city)
        print(len(city))
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


def start_shop_spider(name_list, bloom):
    for city_name in name_list:
        # city_name = 'anshan'
        # bloom = get_shop_url()
        url = f'http://www.dianping.com/{city_name}/ch20/g119'
        # print(url)
        shop_page_html = get_one_page(url)
        etree_page = etree.HTML(shop_page_html)
        city_name = etree_page.xpath('//a[@data-ga-index="1"]/span/text()')[0]
        city_name = city_name.strip().split('购物')[0]
        print(city_name)
        province, city = get_province_city(city_name)
        # print(province, city)
        shop_info = [province, city]
        # print(shop_info)
        shop_info.append(city_name)
        # # print(shop_page_html)
        items = parse_page_response(shop_page_html, url, bloom, shop_info)
        num = write_db(items)
        print(f'{city_name}城市更新了{num}条商家')


if __name__ == '__main__':
    # get_first_url()
    # start_shop_spider()
    start_thread()
    # test_db()











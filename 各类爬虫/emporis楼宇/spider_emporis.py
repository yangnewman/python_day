
import re
import sqlite3
import requests
from lxml import etree
from random import choice
from threading import Thread
from pybloom_live import BloomFilter

from proxy_ip2 import getip
from proxy_zhima import get_zhima_ip


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
        else:
            text = get_page(url)
            return text
    except:
        print('请求已中断，再尝试重新连接...')
        text = get_page(url)
        return text


def get_page(url):
    with open('ip.txt') as f:
        ip_list = f.readlines()
        ip_list = [i.strip() for i in ip_list]
        if ip_list:
            ip = choice(ip_list)
            print(ip)
            proxies = {
                'http': 'http://' + ip,
                'https': 'https://' + ip}
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
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    text = response.content.decode('utf-8')
                    return text
                else:
                    ip_list.remove(ip)
                    with open('ip.txt', 'w') as f2:
                        for write_ip in ip_list:
                            f2.writelines(write_ip)
                            f2.write('\n')
                    text = get_page(url)
                    return text
            except:
                print('得不到响应')
                ip_list.remove(ip)
                with open('ip.txt', 'w') as f2:
                    for write_ip in ip_list:
                        f2.writelines(write_ip)
                        f2.write('\n')
                text = get_page(url)
                return text
        else:
            # path = 'ip.txt'  # 存放爬取ip的文档path
            # # targeturl = 'https://www.emporis.com'  # 验证ip有效性的指定url
            # targeturl = 'https://www.baidu.com'  # 验证ip有效性的指定url
            # getip(targeturl, path)
            # text = get_page(url)
            get_zhima_ip()
            text = get_page(url)
            return text


def parse_with_xpath(html):
    empories_url = 'https://www.emporis.com'
    etree_html = etree.HTML(html)
    # 所有国家
    country = etree_html.xpath('//ul[@class="list noicon-list two-columns"]')[0]
    # country_names = country.xpath('li/a/text()')
    country_urls = country.xpath('li/a/@href')
    # print(country_names)
    # print(country_urls)
    # 获取国家URL
    urls_country = get_country_urls(country_urls, empories_url)
    for city_urls in urls_country:
        # 获取城市url
        url_city_buildings = get_city_url(city_urls, empories_url)
        for url_city_building in url_city_buildings:
            # 获取建筑url
            one_page_building_url_list = get_one_page_building_url(url_city_building)
            # print('******')
            # print(one_page_building_url_list)
            for one_page_building_url in one_page_building_url_list:
                one_building_url = empories_url + one_page_building_url
                # 获取已爬取URL
                bloom = get_building_url()
                if not bloom.add(one_building_url):
                    html_building = get_one_page(one_building_url)
                    etree_html_building = etree.HTML(html_building)
                    empories_dict = {}
                    building_url_dict = {}
                    # 洲名字
                    position_div = etree_html_building.xpath('//div[@class="position_bar"]/ol')[0]
                    continent_name = position_div.xpath('li[2]/a/span/text()')[0]
                    empories_dict['continent_name'] = continent_name
                    # 国家名字
                    country_name_list = etree_html_building.xpath(
                        '//label[text()="Country"]/../following-sibling::span/span/text()')
                    empories_dict['country_name'] = parse_field(country_name_list)
                    # 城市名字
                    city_name_list = etree_html_building.xpath(
                            '//label[text()="City"]/../following-sibling::span/span/text()')
                    empories_dict['city_name'] = parse_field(city_name_list)
                    # 建筑名字
                    building_name_list = etree_html_building.xpath('//label[text()="Name"]/../following-sibling::span/text()')
                    empories_dict['building_name'] = parse_field(building_name_list)
                    # 建筑曾用名
                    alternative_name_list = etree_html_building.xpath('//label[text()="Alternative name"]/../following-sibling::span/text()')
                    empories_dict['alternative_name'] = parse_field(alternative_name_list)
                    # 建筑类型
                    building_type_list = etree_html_building.xpath(
                        '//label[text()="Building type"]/../following-sibling::span/text()')
                    empories_dict['building_type'] = parse_field(building_type_list)
                    # 建筑状态
                    building_status_list = etree_html_building.xpath(
                        '//label[text()="Building status"]/../following-sibling::span/text()')
                    empories_dict['building_status'] = parse_field(building_status_list)
                    # 主要用途
                    main_usage_list = etree_html_building.xpath(
                        '//label[text()="Main Usage"]/../following-sibling::span/span/text()')
                    empories_dict['main_usage'] = parse_field(main_usage_list)
                    # 副功能
                    side_usage_list = etree_html_building.xpath(
                        '//label[text()="Side Usage"]/../following-sibling::span/span/text()')
                    empories_dict['side_usage'] = parse_field(side_usage_list, interval=',')
                    # 建筑地址
                    address_list = etree_html_building.xpath(
                        '//label[text()="Address as text"]/../following-sibling::span/span/text()')
                    empories_dict['address'] = parse_field(address_list)
                    # 建筑高度
                    height_architectural_list = etree_html_building.xpath(
                        '//label[text()="Height (architectural)"]/../following-sibling::span/text()')
                    height_estimated_list = etree_html_building.xpath(
                        '//label[text()="Height (estimated)"]/../following-sibling::span/text()')
                    if height_architectural_list:
                        height = height_architectural_list[0].strip().split('.')[0]
                        print(height)
                        empories_dict['height'] = height
                    elif height_estimated_list:
                        height = height_estimated_list[0].strip().split('.')[0]
                        empories_dict['height'] = height
                    # 建筑地上楼层
                    above_floor_list = etree_html_building.xpath(
                        '//label[text()="Floors (above ground)"]/../following-sibling::span/text()')
                    empories_dict['above_floor'] = parse_field(above_floor_list)
                    # 建筑地下楼层
                    below_floor_list = etree_html_building.xpath(
                        '//label[text()="Floors (below ground)"]/../following-sibling::span/text()')
                    empories_dict['below_floor'] = parse_field(below_floor_list)
                    # 建筑开始施工时间
                    start_time_list = etree_html_building.xpath(
                        '//label[text()="Construction start"]/../following-sibling::span/text()')
                    empories_dict['start_time'] = parse_field(start_time_list)
                    # 建筑结束施工时间
                    end_time_list = etree_html_building.xpath(
                        '//label[text()="Construction end"]/../following-sibling::span/text()')
                    empories_dict['end_time'] = parse_field(end_time_list)
                    # 建筑的特色和便利设施
                    features_amenities_list = etree_html_building.xpath(
                        '//h2[text()="Features & Amenities"]/following-sibling::ul/li/text()')
                    empories_dict['features_amenities'] = parse_field(features_amenities_list, interval=',')
                    # 建筑经纬度
                    latitudes = re.compile('<meta itemprop="latitude" content="(.*?)"/>', re.S)
                    longitudes = re.compile('<meta itemprop="longitude" content="(.*?)"/>', re.S)
                    latitude_list = re.findall(latitudes, html_building)
                    longitude_list = re.findall(longitudes, html_building)
                    if latitude_list and longitude_list:
                        empories_dict['latitude'] = latitude_list[0]
                        empories_dict['longitude'] = longitude_list[0]
                    # 图片地址
                    image_div = re.compile('<div id="singlerow-justified-search-gallery".*?">(.*?)</div>', re.S)
                    image_div_list = re.findall(image_div, html_building)
                    if image_div_list:
                        image_a = re.compile('<a href="(.*?)" rel=', re.S)
                        a_list = re.findall(image_a, image_div_list[0])
                        image_address = empories_url + a_list[0]
                        empories_dict['image_address'] = image_address
                    # 返回爬取的可迭代对象数据
                    yield empories_dict
                    # 当成功插入数据后添加该数据的URL
                    building_url_dict['building_url'] = one_building_url
                    write_building_url(building_url_dict)


def parse_field(field_list, interval=' '):
    if field_list:
        # print(field_list)
        field = interval.join([name.strip() for name in field_list if name.strip() != ''])
        field = field.strip()
        # print(field)
        return field
    else:
        return ''


def get_one_page_building_url(url_city_building):
    # 获取全部建筑URL页面
    for i in range(1, 10000):
    # while
        url_building = url_city_building + f'/{i}'
        # print(url_building)
        html4 = get_one_page(url_building)
        etree_html4 = etree.HTML(html4)
        building_list = etree_html4.xpath('//table[@class="table table-striped table-condensed no-margin "]')[0]
        building_list_content = building_list.xpath('tbody/tr/td[1]/text()')
        if not building_list_content:
            print(i)
            break
        one_page_building_url_list = building_list.xpath('tbody/tr//a/@href')
        for url in one_page_building_url_list:
            yield url


def get_city_url(city_urls, empories_url):
    """
    获取城市url
    """
    for city_url in city_urls:
        url_city = empories_url + city_url
        print(url_city)
        html3 = get_one_page(url_city)
        etree_html3 = etree.HTML(html3)
        building_table = etree_html3.xpath('//table[@class="table table-striped table-small"]')[0]
        all_building_url = building_table.xpath('//td[@class="text-left"]')[0].xpath('a/@href')[0]
        url_city_building = empories_url + all_building_url
        yield url_city_building


def get_country_urls(country_urls, empories_url):
    # 获取国家URL
    for country_url in country_urls:
        url2 = empories_url + country_url
        print(url2)
        html2 = get_one_page(url2)
        etree_html2 = etree.HTML(html2)
        # 所有城市
        city_list = etree_html2.xpath('//ul[@class="list noicon-list two-columns"]')
        print(len(city_list))
        if len(city_list) > 1:
            city_list = etree_html2.xpath('//ul[@class="list noicon-list two-columns"]')[1]
        else:
            city_list = etree_html2.xpath('//ul[@class="list noicon-list two-columns"]')[0]
        city_names = city_list.xpath('li/a/text()')
        city_urls = city_list.xpath('li/a/@href')
        print(city_names)
        yield city_urls


def write_db(items):
    db = sqlite3.connect('spider_emporis.db')
    numb = 0
    cursor = db.cursor()
    for item in items:
        table = 'empories_building'
        keys = ', '.join(item.keys())
        values = ', '.join(['?'] * len(item))
        sql = "INSERT INTO {table}({keys}) VALUES ({values})".format(table=table, keys=keys, values=values)
        try:
            if cursor.execute(sql, tuple(item.values())):
                print('Successful')
                db.commit()
                numb += 1
        except:
            print('Failed')
            db.rollback()
    cursor.close()
    db.close()
    return numb


def get_building_url():
    bloom = BloomFilter(500000, 0.000001)
    db = sqlite3.connect('spider_emporis.db')
    cursor = db.cursor()
    sql = 'select building_url from building_url'
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    db.close()
    for data in datas:
        bloom.add(data[0])
    return bloom


def write_building_url(item):
    db = sqlite3.connect('spider_emporis.db')
    numb = 0
    cursor = db.cursor()
    table = 'building_url'
    keys = ', '.join(item.keys())
    values = ', '.join(['?'] * len(item))
    sql = "INSERT INTO {table}({keys}) VALUES ({values})".format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(item.values())):
            print('Successful')
            db.commit()
            numb += 1
    except:
        print('Failed')
        db.rollback()
    cursor.close()
    db.close()


def thread_start():
    # urls_list = ['/continent/100002/africa', '/continent/100004/asia', '/continent/100001/europe',
    urls_list = ['/continent/100007/north-america', '/continent/100006/oceania', '/continent/100003/south-america']
    print(len(urls_list))
    # 线程组
    threads = []
    for urls in urls_list:
        print(urls)
        # print(len(urls))
        t = Thread(target=emporis_start, args=(urls,))
        t.start()
        threads.append(t)
    # 先执行完所有线程再执行主进程
    for t in threads:
        t.join()
    print('success')


def emporis_start(continent):
    url = 'https://www.emporis.com'
    url += continent
    html = get_one_page(url)
    items = parse_with_xpath(html)
    num = write_db(items)
    continent_name = continent.split('/')[-1]
    print(f'{continent_name}的数据已经爬取完毕！！数据库更新了'+str(num)+'条')


if __name__ == '__main__':
    # continent = '/continent/100001/europe'
    # emporis_start(continent)
    # item = {'building_url': a}
    # write_building_url(item)
    thread_start()



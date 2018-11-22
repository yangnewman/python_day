


import json
import re
import pymysql
import requests
from lxml import etree


def get_one_page(url):

    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    try:
        response = requests.get(url, headers=headers)
    except:
        print('请求已中断，再尝试重新连接...')
        return None
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None

def parse_with_xpath(html):
    etree_html = etree.HTML(html)
    # print(etree_html)
    # result = etree_html.xpath('//div[@id="mod-impnews"]/div[2]/ul/li/a/span/text()')
    # print(result)

    # 搞个图片
    # result = etree_html.xpath('//ul[@class="scrollImg-content"]/li/a/img/@src')
    # print(result)
    nums = etree_html.xpath('//div[@class="col-xs-12"]/a/@title')
    # print(nums[0].strip())
    titles = etree_html.xpath('//div[@class="col-xs-12"]/a/text()')
    # print(title)
    urls = etree_html.xpath('//div[@class="col-xs-12"]/a/@href')
    # # print(len(urls))
    # print(urls)

    json_list = []
    for i in range(len(titles)):
        dicts = {}
        dicts['nums'] = nums[i].strip().split('字')[-1].split('个')[0]
        dicts['title'] = titles[i].split('姓名')[0]
        dicts['url'] = 'http:' + urls[i]
        json_list.append(dicts)

    return json_list


def write_db(items):
    db = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                         db='crawler01', charset='utf8')
    numb = 0
    cursor = db.cursor()

    for item in items:

        table = 'hundred_name'

        keys = ', '.join(item.keys())

        values = ', '.join(['%s'] * len(item))

        sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table,
                                                                                         keys=keys,
                                                                                         values=values)
        update = ', '.join(["{key} = %s".format(key=key) for key in item])
        sql += update
        try:
            if cursor.execute(sql, tuple(item.values())*2):
                # print(sql, tuple(item.values())*2)
                print('Successful')
                db.commit()
                numb += 1
        except:
            print('Failed')
            db.rollback()
    db.close()
    return numb


def main():
    url = 'http://www.resgain.net/xmdq.html'
    html = get_one_page(url)
    print(html)
    items = parse_with_xpath(html)
    num = write_db(items)
    print('数据库更新了'+str(num)+'条')


if __name__ == '__main__':
    main()




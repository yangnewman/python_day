

import pymysql
import requests
from lxml import etree
from threading import Thread


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


def parse_with_xpath(html, data_url):
    etree_html = etree.HTML(html)
    # 所有姓名
    names = etree_html.xpath('//div[@class="col-xs-12"]/a/text()')
    # 所有路由
    print('***')
    print(names)
    urls = etree_html.xpath('//div[@class="col-xs-12"]/a/@href')

    for i in range(len(urls)):

        url = data_url.split('name')[0] + urls[i]
        htmls = get_one_page(url)
        etree_html2 = etree.HTML(htmls)
        # print(htmls)
        # 男用概率
        sex_man = etree_html2.xpath('//div[@class="col-xs-12"]//div[@class="progress-bar"]/text()')[0].strip().split('情')[0]
        # 女用概率
        sex_woman = etree_html2.xpath('//div[@class="col-xs-12"]//div[@class="progress-bar progress-bar-warning"]/text()')[0].strip().split('情')[0]
        # 姓名总解
        try:
            name_explain = etree_html2.xpath('//div[@class="panel-body"]/strong/text()')[0]
        except:
            name_explain = ''
        # 姓名诗
        name_poetry_list = etree_html2.xpath('//div[@style="text-align: center;"]/h4/text()')
        name_poetry = ', '.join(name_poetry_list)
        # 五行
        name_five_lines = etree_html2.xpath('//div[@class="col-xs-6"]/blockquote/text()')[0]
        # 三才配置
        name_three = etree_html2.xpath('//div[@class="col-xs-6"]/blockquote/text()')[1]
        wuge = ['天格', '地格', '人格', '总格', '外格']
        name_wuge = etree_html2.xpath('//div[@class="col-xs-12"]/blockquote/text()')[1:6]
        name_configure_list = []
        name_analysis_list = []
        name_analysis_wuge = etree_html2.xpath('//div[@class="col-xs-12"]/blockquote/div/text()')
        # print(name_analysis_wuge)
        for j in range(5):
            name_configure_list.append(wuge[j] + name_wuge[j].strip())
            name_analysis_list.append(wuge[j] + name_analysis_wuge[j])
        # 名字五格
        name_configure = ', '.join(name_configure_list)
        # 五格分析
        name_analysis = ', '.join(name_analysis_list)

        dicts = {}
        # print(names[i])
        dicts['name'] = names[i]
        dicts['url'] = url
        dicts['sex_man'] = sex_man
        dicts['sex_woman'] = sex_woman
        dicts['name_explain'] = name_explain
        dicts['name_poetry'] = name_poetry
        dicts['name_five_lines'] = name_five_lines
        dicts['name_three'] = name_three
        dicts['name_configure'] = name_configure
        dicts['name_analysis'] = name_analysis
        yield dicts


def write_db(items):
    db = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                         db='crawler01', charset='utf8')
    numb = 0
    cursor = db.cursor()

    for item in items:

        table = 'names'

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


def db_open():
    db = pymysql.connect(host='localhost', port=3306, user='root', password='123456',
                         db='crawler01', charset='utf8')
    cursor = db.cursor()
    sql = 'select url from hundred_name;'
    cursor.execute(sql)
    datas = cursor.fetchall()
    db.close()
    return datas


def fen_url():
    urls = db_open()
    big_list = [url for url in urls]
    n = 15
    url_list = [big_list[i:i + n] for i in range(0, len(big_list), n)]
    return url_list


def main(urls):
    # url = 'http://zhao.resgain.net/name_list.html'
    # urls = db_open()
    for url in urls:
        # 跑完分页
        for i in range(1, 11):
            if i == 1:
                print(url[0])
                html = get_one_page(str(url[0]))
                items = parse_with_xpath(html, str(url[0]))
                num = write_db(items)
            else:
                l = str(url[0])
                r = str(url[0])
                l_split = l.split('.')[0:3]
                r_split = r.split('.')[-1]
                re_url = '.'.join(l_split) + '_{}.'.format(i) + r_split
                print(re_url)
                html = get_one_page(re_url)
                items = parse_with_xpath(html, re_url)
                num = write_db(items)


def thread_start():
    urls_list = fen_url()
    print(len(urls_list))
    # 线程组
    threads = []
    for urls in urls_list:
        print(urls)
        # print(len(urls))
        t = Thread(target=main, args=(urls,))
        t.start()
        threads.append(t)
    # 先执行完所有线程再执行主进程
    for t in threads:
        t.join()
    print('success')


if __name__ == '__main__':
    thread_start()



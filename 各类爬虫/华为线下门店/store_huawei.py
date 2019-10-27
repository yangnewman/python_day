import json
import sqlite3
import requests
from lng_lat_to_gps import transfer


class HwSpider(object):

    def __init__(self):
        self.url = 'https://openapi.vmall.com/mcp/offlineshop/getShopList'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'text/plain',
            'CsrfToken': '56281CE7688305EE123CB28FCCF730BC747FDFF5D8D3F243',
            'Referer': 'https://www.vmall.com/offshop/hwshoplist',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.data = {"lang": "zh-CN", "country": "CN", "portal": 1, "brand": 2,
                     "province": "", "city": "", "dist": "", "pageNo": 1, "pageSize": 16}

    def get_response(self):
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
        if response.status_code == 200:
            print(response.text)
            print(type(response.text))
            res_data = json.loads(response.text)
            print(type(res_data))
            print(len(res_data['shopInfos']))
            return res_data['shopInfos']

    @staticmethod
    def clean_data(res_data):
        tr = transfer()
        for data in res_data:
            item = dict()
            item['name'] = data['name']
            item['address'] = data['address']
            item['province'] = data['province']
            item['city'] = data['city']
            item['dist'] = data['dist']
            item['bd_longitude'] = data['longitude']
            item['bd_latitude'] = data['latitude']
            item['gps_longitude'], item['gps_latitude'] = tr.bd09_to_wg84(float(data['longitude']),
                                                                          float(data['latitude']))
            item['image'] = data['starShopPic']
            yield item

    @staticmethod
    def write_db(items):
        db = sqlite3.connect('huawei_shop.db')
        numb = 0
        cursor = db.cursor()
        for item in items:
            # print(item)
            table = 'store_huawei'
            keys = ', '.join(item.keys())
            values = ', '.join(['?'] * len(item))
            sql = "REPLACE INTO {table}({keys}) VALUES ({values})".format(table=table, keys=keys, values=values)
            # print(sql)
            try:
                if cursor.execute(sql, tuple(item.values())):
                    db.commit()
                    print('Success')
                    numb += 1
            except Exception:
                print('Failed')
                db.rollback()
        cursor.close()
        db.close()
        return numb

    def start_crawler(self):
        for i in range(1, 2):
            self.data["pageNo"] = i
            res_data = self.get_response()
            items = self.clean_data(res_data)
            self.write_db(items)
            print(f'第{i}页已爬完')


if __name__ == '__main__':
    my_spider = HwSpider()
    my_spider.get_response()
    # my_spider.start_crawler()

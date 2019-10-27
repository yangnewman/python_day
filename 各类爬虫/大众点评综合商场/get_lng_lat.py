from random import choice
import requests


def get_gaode_lng_lat(address):
    # shop_address = pro + city + address + name
    with open('gaode_key.txt') as f:
        key_list = f.readlines()
        key_list = [i.strip() for i in key_list]
        if key_list:
            key = choice(key_list)
    par = {'address': address, 'key': key}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    try:
        response = requests.get(base, par, timeout=5)
        answer = response.json()
        # print(answer)
        GPS = answer['geocodes'][0]['location'].split(",")
        return GPS[0], GPS[1]
    except:
        return 0, 0


def get_tengxun_lng_lat(address):
    key = 'QXMBZ-E2ICI-QTXGX-5SHLN-BXC2O-QSF3W'
    base = f'https://apis.map.qq.com/ws/geocoder/v1/?address={address}&key={key}'
    response = requests.get(base)
    answer = response.json()
    print(answer)
    if not answer['status']:
        lng = answer['result']['location']['lng']
        lat = answer['result']['location']['lat']
        print(lng, lat)
        return lng, lat
    # print(answer)


def get_gaode_city(address):
    with open('gaode_key.txt') as f:
        key_list = f.readlines()
        key_list = [i.strip() for i in key_list]
        if key_list:
            key = choice(key_list)
            par = {'address': address, 'key': key}
            base = 'http://restapi.amap.com/v3/geocode/geo'
            response = requests.get(base, par)
            answer = response.json()
            # print(answer)
            try:
                province = answer['geocodes'][0]['province']
                city = answer['geocodes'][0]['city']
                return province, city
            except:
                return 0, 0


def get_province_city(address):
    key = 'QXMBZ-E2ICI-QTXGX-5SHLN-BXC2O-QSF3W'
    base = f'https://apis.map.qq.com/ws/geocoder/v1/?address={address}&key={key}'
    response = requests.get(base)
    answer = response.json()
    # print(answer)
    try:
        # if not answer['status']:
        province = answer['result']['address_components']['province']
        city = answer['result']['address_components']['city']
        # print(province)
        return province, city
    except:
        province, city = get_gaode_city(address)
        return province, city


if __name__ == '__main__':
    address = '茫崖市'
    # print(get_gaode_lng_lat(address))
    # get_tengxun_lng_lat(address)
    print(get_province_city(address))




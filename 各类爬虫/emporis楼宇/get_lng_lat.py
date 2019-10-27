

import requests
from geopy.geocoders import Nominatim

#使用高德API
def geocodeG(address):
    par = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, par)
    answer = response.json()
    GPS=answer['geocodes'][0]['location'].split(",")
    return GPS[0],GPS[1]

#使用百度API
def geocodeB(address):
    base = url = "http://api.map.baidu.com/geocoder?address=" + address + "&output=json&key=f247cdb592eb43ebac6ccd27f796e2d2"
    response = requests.get(base)
    answer = response.json()
    return answer['result']['location']['lng'],answer['result']['location']['lat']


#使用geopy查询
def geocodeN(address):
    gps=Nominatim(user_agent="specify_your_app_name_here")
    location=gps.geocode(address)
    print(location)
    return location.longitude,location.latitude


import urllib
from urllib.request import urlopen
import json


def getGeoForAddress(address):
    # address = "上海市中山北一路121号"
    addressUrl = "http://maps.googleapis.com/maps/api/geocode/json?address=" + address
    # 中文url需要转码才能识别
    addressUrlQuote = urllib.parse.quote(addressUrl, ':?=/')
    response = urlopen(addressUrlQuote).read().decode('utf-8')
    responseJson = json.loads(response)
    lat = responseJson.get('results')[0]['geometry']['location']['lat']
    lng = responseJson.get('results')[0]['geometry']['location']['lng']
    print(address + '的经纬度是: %f, %f' % (lat, lng))
    return [lat, lng]


def test():
    serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
    # serviceurl = 'http://python-data.dr-chuck.net/geojson?'

    while True:
        address = input('Enter location:')
        if len(address) < 1: break
        url = serviceurl + urllib.parse.urlencode({'sensor': 'false', 'address': address})
        print('Retrieving:', url)
        uh = urllib.request.urlopen(url)
        data = uh.read()
        print('Retrieved:', len(data), 'characters')

        print(str(data))
        # 接受过来的数据都是字节型数据需要进行decode（）操作
        try:
            js = json.loads(data.decode())
        except:
            js = None
        # try:js = json.loads(str(data))
        # except: js = None
        print(js)
        if 'status' not in js or js['status'] != 'OK':
            print('===Failed To Retrieve===')
            print(data)
            continue
        print(json.dumps(js, indent=4))

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        print('lat:', lat, 'lng:', lng)
        location = js['results'][0]['formatted_address']
        print(location)


if __name__ == '__main__':
    address = 'Algiers El Hamma Tours II'
    test()


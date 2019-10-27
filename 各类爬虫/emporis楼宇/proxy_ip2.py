
import re
import random
import requests,threading,datetime
from lxml import etree
from bs4 import BeautifulSoup
"""
1、抓取西刺代理网站的代理ip
2、并根据指定的目标url,对抓取到ip的有效性进行验证
3、最后存到指定的path
"""

# ------------------------------------------------------文档处理--------------------------------------------------------
# 写入文档
def write(path,text):
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(text)
        f.write('\n')
# 清空文档
def truncatefile(path):
    with open(path, 'w', encoding='utf-8') as f:
        f.truncate()
# 读取文档
def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        txt = []
        for s in f.readlines():
            txt.append(s.strip())
    return txt
# ----------------------------------------------------------------------------------------------------------------------
# 计算时间差,格式: 时分秒
def gettimediff(start,end):
    seconds = (end - start).seconds
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    diff = ("%02d:%02d:%02d" % (h, m, s))
    return diff
# ----------------------------------------------------------------------------------------------------------------------
# 返回一个随机的请求头 headers
def getheaders():
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers


# -----------------------------------------------------检查ip是否可用----------------------------------------------------
def checkip(targeturl, ip):
    headers =getheaders()  # 定制请求头
    proxies = {"http": "http://"+ip, "https": "http://"+ip}  # 代理ip
    try:
        response=requests.get(url=targeturl,proxies=proxies,headers=headers, timeout=10).status_code
        if response == 200 :
            return True
        else:
            return False
    except:
        return False

#-------------------------------------------------------获取代理方法----------------------------------------------------
# 免费代理 XiciDaili
def find_xiciip(type, pagenum, targeturl, path): # ip类型,页码,目标url,存放ip的路径
    list_dict={'1': 'http://www.xicidaili.com/nt/', # xicidaili国内普通代理
          '2': 'http://www.xicidaili.com/nn/', # xicidaili国内高匿代理
          '3': 'http://www.xicidaili.com/wn/', # xicidaili国内https代理
          '4': 'http://www.xicidaili.com/wt/'} # xicidaili国外http代理
    # list_dict = {'1': 'http://www.xicidaili.com/nn/'}
    url=list_dict[str(type)]+str(pagenum) # 配置url
    headers = getheaders() # 定制请求头
    html=requests.get(url=url,headers=headers, timeout=10).text
    soup=BeautifulSoup(html,'lxml')
    all=soup.find_all('tr',class_='odd')
    for i in all:
        t=i.find_all('td')
        ip=t[1].text+':'+t[2].text
        is_avail = checkip(targeturl,ip)
        if is_avail == True:
            write(path=path,text=ip)
            print(ip)


def find_6ip(pagenum,targeturl,path): # ip类型,页码,目标url,存放ip的路径
    url = f'http://www.66ip.cn/{pagenum}.html'
    headers = getheaders()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            text = response.content.decode('gbk')
            table_re = re.compile('<tr>(.*?)</tr>', re.S)
            table = re.findall(table_re, text)[2:]
            for table_text in table:
                td_re = re.compile('<td>(.*?)</td>', re.S)
                td = re.findall(td_re, table_text)[:2]
                ip = td[0] + ':' + td[1]
                is_avail = checkip(targeturl, ip)
                if is_avail == True:
                    write(path=path, text=ip)
                    print(ip)
        else:
            print('66IP无法获取')
    except:
        print('66IP无法获取')
        return None


#-----------------------------------------------------多线程抓取ip入口---------------------------------------------------
def getip(targeturl, path):
     truncatefile(path) # 爬取前清空文档
     start = datetime.datetime.now() # 开始时间
     threads = []
     for pagenum in range(5):   # 四种类型ip,每种类型取前三页,共12条线程
         t2 = threading.Thread(target=find_6ip, args=(pagenum + 1, targeturl, path))
         t2.start()  # 开启多线程爬取
         threads.append(t2)
         for type in range(4):
             t1=threading.Thread(target=find_xiciip,args=(type+1, pagenum+1, targeturl, path))
             t1.start() # 开启多线程爬取
             threads.append(t1)
     print('开始爬取代理ip')
     for e in threads: # 等待所有线程结束
         e.join()
     print('爬取完成')
     end = datetime.datetime.now() # 结束时间
     diff = gettimediff(start, end)  # 计算耗时
     ips = read(path)  # 读取爬到的ip数量
     print(ips)
     print('一共爬取代理ip: %s 个,共耗时: %s \n' % (len(ips), diff))


# def proxy_ip(url):
#     with open('ip.txt') as f:
#         ip_list = f.readlines()
#         ip_list_copy = ip_list
#         for ip in ip_list:
#             if ip_list_copy:
#                 print(ip)
#                 proxies = {
#                     'http': 'http://' + ip,
#                     'https': 'https://' + ip
#                 }
#                 user_agent_list = [
#                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
#                     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
#                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
#                     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
#                     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
#                     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
#                     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
#                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#                     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#                     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
#                     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
#                     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
#                 ]
#                 UserAgent = random.choice(user_agent_list)
#                 headers = {'User-Agent': UserAgent}
#                 print('------')
#                 try:
#                     print('+++++++++')
#                     response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
#                     print(response.status_code)
#                     if response.status_code == 200:
#                         text = response.content.decode('utf-8')
#                         return text
#                     else:
#                         ip_list_copy.remove(ip)
#                 except:
#                     print('IP失效')
#                 finally:
#                     ip_list_copy.remove(ip)
#     return None
        # if not ip_list:
        #     path = 'ip.txt'  # 存放爬取ip的文档path
        #     targeturl = 'https://www.emporis.com'  # 验证ip有效性的指定url
        #     getip(targeturl, path)
        #     proxy_ip(url)


def get_ip_list():
    with open('ip.txt') as f1:
        ip_list= f1.readlines()
        print(ip_list, len(ip_list))
        ip_list = [i.strip() for i in ip_list]
        ip = random.choice(ip_list)
        print(ip)
        ip_list.remove(ip)
        print(ip_list, len(ip_list))
        with open('ip.txt', 'w') as f2:
            for i in ip_list:
                f2.writelines(i)
                f2.write('\n')

#-------------------------------------------------------启动-----------------------------------------------------------
if __name__ == '__main__':
    # path = 'ip.txt' # 存放爬取ip的文档path
    # # targeturl = 'http://www.cnblogs.com/TurboWay/' # 验证ip有效性的指定url
    # targeturl = 'https://www.emporis.com' # 验证ip有效性的指定url
    # getip(targeturl,path)
    # read_ip(path)
    get_ip_list()
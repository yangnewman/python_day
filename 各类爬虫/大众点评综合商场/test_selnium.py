from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree

# 无头浏览器
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()
browser.set_window_size(1400, 700)
# 显示等待,针对某个节点的等待
wait = WebDriverWait(browser, 10)
KEYWORD = '编程机器人'


def test_sel():
    browser.get('http://www.dianping.com/shop/69421139')




if __name__ == '__main__':
    test_sel()


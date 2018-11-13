import time
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree
from PIL import Image
from io import BytesIO

from compare_helper import get_compare_loop, getImgHash, getMH

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()
browser.set_window_size(1400, 700)
# 显示等待,针对某个节点的等待
wait = WebDriverWait(browser, 10)


def index_page():
    # if page == 1:
    url = 'http://www.1kkk.com/register/'
    # print(url)
    browser.get(url)
    page_source = browser.page_source

    return page_source


# 取游览器窗口的图片
def get_big_image():
    # scroll_to = 'window.scrollTo(0, 300)'
    # browser.execute_script(scroll_to)
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    return screenshot


def save_image(image_site):
    # etree_html = etree.HTML(page_source)
    big_image = get_big_image()
    big_image.save('big_image.png')
    # x1, y1, x2, y2 = get_position()
    crop_image = big_image.crop(image_site)
    filename = 'yang_ma.png'
    crop_image.save(filename)

# 去验证码坐标位置（左上角和右下角）
def get_position():
    """
    获取验证码位置
    :return: 验证码位置元组
    """
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
    # print(img)
    location = img.location
    size = img.size
    print(location)
    print(size)
    x1 = location['x']+1
    y1 = location['y']
    x2 = location['x'] + size['width']+1
    y2 = location['y'] + size['height']
    return (x1, y1, x2, y2)


def if_image_next(list_pic, image_site):
    save_image(image_site)
    for pic in list_pic:
        image_hash = getImgHash('./yang_ma.png')
        pic_hash = list(pic.values())[0]
        compare = getMH(image_hash, pic_hash)
        if compare >= 90:
            return True
    return False

def get_image_position():
    img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
    location = img.location
    size = img.size
    print(location)
    print(size)
    image_list = []
    for i in range(4):
        x1 = location['x'] + 1+(i*78)
        y1 = location['y']
        x2 = location['x'] + size['width'] + 1+(i*78)
        y2 = location['y'] + size['height']
        image_list.append((x1, y1, x2, y2))
    print(image_list)
    return image_list


def click_image(list_pic, image_site, num_image):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rotate-background')))
    for i in range(4):
        flag = if_image_next(list_pic, image_site)
        if flag:
            return True
        submit = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rotate-background')))[num_image]
        time.sleep(1)
        submit.click()
    return False


def main():
    index_page()
    list_pic = get_compare_loop()
    image_sites = get_image_position()
    num_image = 0
    for image_site in image_sites:
        print(image_site)
        # save_image(image_site)
        result = click_image(list_pic, image_site, num_image)
        print(result)
        if result:
            num_image += 1



if __name__ == '__main__':
    main()
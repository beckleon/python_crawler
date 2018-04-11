from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from bs4 import BeautifulSoup
import pymongo
import re

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
KEYWORD = 'iPad'

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """
    try:
        if db[MONGO_COLLECTION].insert_one(result):
            pass
            # print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def get_products():
    """
    提取商品数据
    """
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    itemlist_soup = soup.find("div", class_="m-itemlist")
    itemlist = itemlist_soup.find_all("div", class_="item")
    for item in itemlist:
        image = item.find("img", class_="img")["data-src"].strip()
        price = item.find("div", class_="price").get_text().strip()
        deal = item.find("div", class_="deal-cnt").get_text().strip()
        title = item.find("div", class_="title").get_text().strip()
        shop = item.find("a", class_="shopname").get_text().strip()
        location = item.find("div", class_="location").get_text().strip()

        product = {
            'image': image,
            'price': price,
            'deal': deal,
            'title': title,
            'shop': shop,
            'location': location
        }
        save_to_mongo(product)


def search():
    '''
    抓取搜索结果首页，获取搜索结果总页数
    '''
    try:
        browser.get('https://s.taobao.com/search?q=' + quote(KEYWORD))
        total = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="total"]')))
        page = total.text
        # 获取首页的结果列表
        get_products()
        # 获取总页数
        page_num = re.search('(\d+)', page).group()
        return int(page_num)
    except TimeoutError:
        print("timeout...")
        return search()


def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.input.J_Input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.btn.J_Submit')))
        # 清空输入框
        input.clear()
        # 输入目标页数
        input.send_keys(page_number)
        # 点击确认
        submit.click()
        # 确定目标页面的当前页码与预想的一致
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutError:
        next_page(page_number)


def main():
    total = search()
    print(total)
    if total > 1:
        for i in range(2, total + 1):
            print(i)
            next_page(i)


if __name__ == '__main__':
    main()
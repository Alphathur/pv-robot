#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random
import time
import traceback

import requests
from bs4 import BeautifulSoup

# 这里覆盖你的百度文库商店ID
SHOP_ID = "f3b219e8b8f67c1cfad6b85c"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}
cookies = None


def find_all_page():
    global cookies
    page = "https://wenku.baidu.com/user/interface/shopsearchdoc?shopId=" + SHOP_ID + "&pn=0&rn=12&docClass=-1&sortType=2"
    resp = requests.get(page, headers=headers)
    if resp.status_code != 200:
        return None
    cookies = resp.cookies.get_dict()
    total_count = resp.json()['data']['totalCount']
    return math.ceil(total_count / 12)


def wenku_visit(pn):
    page = "https://wenku.baidu.com/user/interface/shopsearchdoc?shopId=" + SHOP_ID + "&pn=" + str(pn) + "&rn=12&docClass=-1&sortType=2"
    js = requests.get(page, headers=headers).json()
    time.sleep(2)
    content = js['data']['content']
    if not len(content):
        return
    for index, con in enumerate(content):
        try:
            url = "https://wenku.baidu.com/view/" + con['sourceId']
            print(str(index), con['title'], url)
            resp = requests.get(url, headers=headers, cookies=cookies)
            if resp.status_code != 200:
                print('Invalid url:', url, "; current response:", resp)
                continue
            page_content = resp.content
            soup = BeautifulSoup(page_content, features="html.parser")
            blog_title = str(soup.title.string)
            print(blog_title)
            time.sleep(random.randint(1, 3))
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(3)


if __name__ == '__main__':
    while True:
        total_page = find_all_page()
        if total_page is None or total_page <= 0:
            print("请检查SHOP_ID")
            break
        time.sleep(2)
        for i in range(total_page):
            wenku_visit(i)
        print("开始休息...")
        time.sleep(random.randint(60, 360))

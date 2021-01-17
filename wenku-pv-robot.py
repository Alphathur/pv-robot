#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import math
import random
import time
import urllib.request

from bs4 import BeautifulSoup

# 这里覆盖你的百度文库商店ID
SHOP_ID = "f3b219e8b8f67c1cfad6b85c"

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent',
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'),
                     ('Cookie',
                      'BAIDUID=A2C8E006AAB89C9C54DB98D08E8F34A7:FG=1')]


def wenku_visit(pn):
    page = "https://wenku.baidu.com/user/interface/shopsearchdoc?shopId=" + SHOP_ID + "&pn=" + str(pn) + "&rn=12&docClass=-1&sortType=2"
    res = opener.open(page).read().decode('utf-8')
    js = json.loads(res)
    content = js['data']['content']
    if not len(content):
        return
    for index, con in enumerate(content):
        try:
            url = "https://wenku.baidu.com/view/" + con['sourceId']
            print(str(index), con['title'], url)
            page_content = opener.open(url).read()
            soup = BeautifulSoup(page_content, features="html.parser")
            blog_title = str(soup.title.string)
            print(blog_title)
            time.sleep(random.randint(1, 3))
        except urllib.error.HTTPError:
            print('urllib.error.HTTPError')
            time.sleep(3)
        except urllib.error.URLError:
            print('urllib.error.URLError')
            time.sleep(5)


if __name__ == '__main__':
    page = "https://wenku.baidu.com/user/interface/shopsearchdoc?shopId=" + SHOP_ID + "&pn=0&rn=12&docClass=-1&sortType=2"
    res = opener.open(page).read().decode('utf-8')
    js = json.loads(res)
    total_count = js['data']['totalCount']
    total_page = math.ceil(total_count / 12)
    print(total_page)
    time.sleep(5)
    while True:
        for i in range(total_page):
            wenku_visit(i)
            print("开始休息...")
            time.sleep(random.randint(60, 360))

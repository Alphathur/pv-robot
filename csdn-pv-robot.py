#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import re
import time
import traceback

import requests
from bs4 import BeautifulSoup

# 这里覆盖你的csdn博客用户ID
USER_ID = "m0_38106923"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}


def find_all_url():
    url = "http://blog.csdn.net/" + USER_ID + "/article/list"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None
    resp_text = requests.get(url, headers=headers).text
    end_url = "/" + USER_ID + "/article/details/\d*"
    p = re.compile(end_url)
    urls = list(set(p.findall(resp_text)))  # 去重
    base_url = "http://blog.csdn.net"  # 合并地址
    for i in range(len(urls)):
        urls[i] = base_url + urls[i]
    return urls


def csdn_visit(urls):
    for index, page in enumerate(urls):
        try:
            print(str(index), page)
            resp = requests.get(page, headers=headers)
            if resp.status_code != 200:
                print('Invalid url:', page, "; current response:", resp)
                continue
            page_content = resp.text
            soup = BeautifulSoup(page_content, features="html.parser")
            blog_title = str(soup.title.string)
            blog_title = blog_title[0:blog_title.rfind('_')]
            print(blog_title)
            time.sleep(random.randint(1, 3))
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(3)


if __name__ == '__main__':
    while True:
        all_url = find_all_url()
        if all_url is None or not len(all_url):
            print("请检查用户ID是否正确")
            break
        csdn_visit(all_url)
        print("开始休息...")
        time.sleep(random.randint(60, 360))

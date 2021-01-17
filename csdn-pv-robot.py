#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import re
import time
import urllib.request

from bs4 import BeautifulSoup

# 这里覆盖你的csdn博客用户名
USER_NAME = "m0_38106923"

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent',
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')]


def find_all_url():
    url = "http://blog.csdn.net/" + USER_NAME + "/article/list"
    html = opener.open(url).read().decode('utf-8')
    end_url = "/" + USER_NAME + "/article/details/\d*"
    p = re.compile(end_url)
    urls = list(set(p.findall(html)))  # 去重
    base_url = "http://blog.csdn.net"  # 合并地址
    for i in range(len(urls)):
        urls[i] = base_url + urls[i]
    return urls


def csdn_visit(urls):
    for index, page in enumerate(urls):
        try:
            print(str(index), page)
            page_content = opener.open(page).read().decode('utf-8')
            soup = BeautifulSoup(page_content, features="html.parser")
            blog_title = str(soup.title.string)
            blog_title = blog_title[0:blog_title.rfind('-')]
            print(blog_title)
            time.sleep(random.randint(1, 3))
        except urllib.error.HTTPError:
            print('urllib.error.HTTPError')
            time.sleep(3)
        except urllib.error.URLError:
            print('urllib.error.URLError')
            time.sleep(5)


if __name__ == '__main__':
    all_url = find_all_url()
    if not len(all_url):
        print("请检查用户名是否正确")
    while True:
        csdn_visit(all_url)
        print("开始休息...")
        time.sleep(random.randint(60, 360))

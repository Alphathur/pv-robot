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
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')
                     ('Cookie',
                      'murmur=undefined--Win32; BIDUPSID=24C13F70A7F50E4E727DC8762512C13D; PSTM=1605710093; BAIDUID=24C13F70A7F50E4EB8DC2C02CF16E271:FG=1; _click_param_reader_query_ab=-1; _click_param_pc_rec_doc_2017_testid=4; layer_show_times_total_2_d65f1901b526fdc2dfbf7532ea24eed1=3; __yjs_duid=1_8afc482d77d10f521585e93053a895951608817448244; BDUSS=50flg1TXhtblR3M2hkeEZRUTlkRHFJOWRGTXZqZmF6UkUxOGhQaEl4ZHZSQ0ZnSVFBQUFBJCQAAAAAAAAAAAEAAACjhUIssKK2-7eoyaoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG-3-V9vt~lfQX; BDUSS_BFESS=50flg1TXhtblR3M2hkeEZRUTlkRHFJOWRGTXZqZmF6UkUxOGhQaEl4ZHZSQ0ZnSVFBQUFBJCQAAAAAAAAAAAEAAACjhUIssKK2-7eoyaoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG-3-V9vt~lfQX; Hm_lvt_f06186a102b11eb5f7bcfeeab8d86b34=1610201232,1610206534,1610274578,1610379776; MCITY=-340%3A; BAIDUID_BFESS=D0F5F312F510454F5257F8945A3A6726:FG=1; BDRCVFR[shF0fZW8Lss]=mk3SLVN4HKm; delPer=0; PSINO=6; H_PS_PSSID=; Hm_lvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1610548459,1610553187,1610814162,1610872019; BDRCVFR[n9IS1zhFc9f]=mk3SLVN4HKm; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BA_HECTOR=04ala10g042g2g8ht31g0827l0r; Hm_lpvt_d8bfb560f8d03bbefc9bdecafc4a4bf6=1610880691; ab_sr=1.0.0_ZTU3NmEyYzViZDFjMzdiYWYzZjZkNWI1MWIzYmZiMTFmZjI1N2I3ZGIyYWMwYmMwNWQ3MWIxNzVjMGI0NzM2YTM0YzU3MDhkMTJmYzE3OTZhZDY3NDEyOWMyMGNjMGNh; bcat=a4684860a551532d799673f35bde4cfe2177d7ddfe1ee70929ab2f5780e708ad9cee86365417abd420eb0097821fdef68e5bb6830021df22ce330616b1d4c699a2400eb405359cdfa1c1d648dd62cb188f9529a68b42bad0ed14a858da3c8959924a87dde9e170459ceb577afcf67ff9aadea34f2725312ea94ec1f6fd456972')]


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
    while True:
        for i in range(total_page):
            wenku_visit(i)
            print("开始休息...")
            time.sleep(random.randint(60, 360))

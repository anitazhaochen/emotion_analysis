#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import json
import pymongo
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",
           "Cookie": "_s_tentry=-; Apache=8783038250691.375.1555929990353; SINAGLOBAL=8783038250691.375.1555929990353; ULV=1555929990358:1:1:1:8783038250691.375.1555929990353:; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; SUB=_2AkMr4Smbf8NxqwJRmfkdy2vnZYp1yAzEieKdvdhAJRMxHRl-yT9jqnMOtRB6AGEHdKk-wGaPegstO-A_YXw5BPFI6CuU; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFcuE0NE594WJhzSbVzYIUp; WBStorage=201904221934|undefined; YF-Page-G0=c948c7abbe2dbb5da556924587966312|1555932858|1555932840; TC-Page-G0=8518b479055542524f4cf5907e498469|1555932878|1555932877"}

client = pymongo.MongoClient(host='localhost', port=27017)

def goindexpage(keywords):
    # url = 'https://twitter.com/search?src=typd&q=belt%20and%20road'
    url = 'https://twitter.com/search?src=typd&q='+keywords
    # url = quote(url, "utf-8")
    html = requests.get(url, headers=headers).text
    return html

def getfirstposition(html):
    position = re.search(r"data-max-position=.+ ?", html).group(0)[19:-1]
    return position

def parse_page_and_save(html):
    tree = etree.HTML(html)
    result = tree.xpath('//div/div[2]/div[2]/p')
    #result = tree.xpath('//*[@data-item-type="tweet"]//p')
    for r in result:
        info = r.xpath('string(.)').strip()
        save(info)

def save(comment):
    db = client.zjn
    twitter_col = db.twitter
    print(comment + "   已存入 mongo ")
    twitter_col.insert({'comment': comment})


def getmorepage(position,keywords):
    # nexurl = 'https://twitter.com/i/search/timeline?vertical=news&q=belt%20and%20road&src=typd&include_available_features=1&include_entities=1&max_position='+position+'&reset_error_state=false'
    nexurl = 'https://twitter.com/i/search/timeline?vertical=news&q='+keywords+'&src=typd&include_available_features=1&include_entities=1&max_position='+position+'&reset_error_state=false'
    # nexurl = quote(nexurl, "utf-8")
    html = requests.get(nexurl, headers=headers).text
    return html

def getposition(html):
    j = json.loads(html)
    position = j['min_position']
    return position

def handler_page(position,keywords):
    # nexurl = 'https://twitter.com/i/search/timeline?vertical=news&q=belt%20and%20road&src=typd&include_available_features=1&include_entities=1&max_position='+position+'&reset_error_state=false'
    nexurl = 'https://twitter.com/i/search/timeline?vertical=news&q='+keywords+'&src=typd&include_available_features=1&include_entities=1&max_position='+position+'&reset_error_state=false'
    # nexurl = quote(nexurl, "utf-8")
    html = requests.get(nexurl, headers=headers).text
    head = "<!DOCTYPE html><html><head><title></title></head><body>"
    tail = "</body></html>"
    position = json.loads(html)['min_position']
    html = json.loads(html)['items_html']
    html = head + html + tail
    return html, position


def main():
    print(" 进入主页访问 ")
    keywords = "一带一路"
    html = goindexpage(keywords)
    print("处理主页数据，并准备存入数据库")
    parse_page_and_save(html)
    print(" 主页处理完毕，开始获取第一个 position  ")
    position = getfirstposition(html)
    print("开始循环进行下拉操作, 获取更多数据")
    i = 1
    while True:
        print("[循环]     拿到主页 position 开始获取 下拉 html")
        try:
            html, position = handler_page(position,keywords)
        except Exception:
            print("[循环]  position 报错!!!!!!!!!!!!")
        print("[循环]     开始处理并存储数据")
        try:
            parse_page_and_save(html)
        except Exception:
            print("[循环]     解析 error")

        print("[循环]     获取position 数量   " + str(i))
        # position = getposition(html)
        time.sleep(20)
        i += 1

if __name__ == "__main__":
        main()

# tree = etree.HTML(html)
#print(html)
# print(len(result))

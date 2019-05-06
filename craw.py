#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import time
import pymongo


# 获取 页面的所有 标题 和 url 地址
def geturlandtitle():
    for page in range(1,14):
        url = 'https://s.weibo.com/article?q=%E4%B8%80%E5%B8%A6%E4%B8%80%E8%B7%AF&Refer=weibo_article&page='+str(page)
        html = requests.get(url).text
        tree = etree.HTML(html)
        posttitle = tree.xpath('//*[@id="pl_feedlist_index"]/div/div/div/h3/a/@title')
        posturl = tree.xpath('//*[@id="pl_feedlist_index"]/div/div/div/h3/a/@href')
        # for i in range(len(title)): print(title[i]+'    '+posturl[i])
        postcontent = getpostcontent(posturl)
        print("开始爬取网页 url"+ str(page)+"页，  共 "+str(len(posturl)))
        for i in range(len(posttitle)):
            savetomongo(posturl[i], posttitle[i], postcontent[i])

# 爬取url 正文内容
def getpostcontent(urls=None):
    # for url in urls:
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "en-us",
               "Connection": "keep-alive",
               "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7",
               "Cookie":"_s_tentry=-; Apache=8783038250691.375.1555929990353; SINAGLOBAL=8783038250691.375.1555929990353; ULV=1555929990358:1:1:1:8783038250691.375.1555929990353:; YF-V5-G0=d30fd7265234f674761ebc75febc3a9f; SUB=_2AkMr4Smbf8NxqwJRmfkdy2vnZYp1yAzEieKdvdhAJRMxHRl-yT9jqnMOtRB6AGEHdKk-wGaPegstO-A_YXw5BPFI6CuU; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFcuE0NE594WJhzSbVzYIUp; WBStorage=201904221934|undefined; YF-Page-G0=c948c7abbe2dbb5da556924587966312|1555932858|1555932840; TC-Page-G0=8518b479055542524f4cf5907e498469|1555932878|1555932877"}


    list = []
    for url in urls:
        print("开始爬取 "+ url +"   内容")
        html = requests.get(url,headers=headers).text
        tree = etree.HTML(html)
        content = tree.xpath('//*[@id="plc_main"]/div/div/div/div[2]/div[3]//p/text()')
        content = ''.join(content)
        list.append(content)
        time.sleep(5)
    return list

# 连接 MongoDB,并且存储
def savetomongo(posturl, posttitle, postcontent):
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.zjn
    weibo_col = db.weibo
    post = {
       'posttitle': posttitle,
        'posturl': posturl,
        'postcontent': postcontent
    }
    weibo_col.insert_one(post)
    print(posttitle + "     插入成功")


def main():
    geturlandtitle()

main()

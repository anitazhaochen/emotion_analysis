#!/usr/bin/env python
# -*- coding: utf-8 -*-

from snownlp import SnowNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
import pymongo
import time

# 获取处理后的 数据 new_twitter
Mongo_HOST = "localhost"
Mongo_PORT = 27017

def get_result(comment):
    s = SnowNLP(u'这个东西真心很不好')
    print(s.words)
    print(s.sentiments)

def wordcloud(words_count):
    matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
    wordcloud = WordCloud(font_path="./data/simfang.ttf",
                          background_color="white", max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_count.head(100).values}
    wordcloud = wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)
    # 输出词云图片
    plt.show()

# def getdata_from_mongo():
#     client = pymongo.MongoClient(host=Mongo_HOST, port=Mongo_PORT)
#     zjn = client.zjn
#     result = zjn.new_twitter.find()
#     i = 0
#    for r in result:
#        s =  SnowNLP(r['comment'])
#        print(s.words)
#        print(s.sentiments)

    # str = ""
    # for r in result:
    #     str+= "".join(r['comment'])

    # wordcloud = WordCloud(font_path="./data/simfang.ttf",
    #                       background_color="white", max_font_size=80).generate(str)
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.show()

#getdata_from_mongo()



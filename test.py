#!/usr/bin/env python
# -*- coding: utf-8 -*-

from snownlp import SnowNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
import pymongo
import time

s =  SnowNLP(u'这个东西很恶心')
print(s.words)
print(s.sentiments)
#mytext = "Just before I stepped out onto the glass panel portion of the Gatlinburg SkyBridge, my feet and my brain were having a friendly disagreement about the idea."
#wordcloud = WordCloud().generate(mytext)


#plt.imshow(wordcloud, interpolation='bilinear')
#plt.show()

def wordcloud(words_count):
    matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
    wordcloud = WordCloud(font_path="./data/simfang.ttf",
                          background_color="white", max_font_size=80)
    word_frequence = {x[0]: x[1] for x in words_count.head(100).values}
    wordcloud = wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)
    # 输出词云图片
    plt.show()

def getdata_from_mongo():
    client = pymongo.MongoClient(host='localhost', port=27017)
    zjn = client.zjn
    result = zjn.new_twitter.find()
    i = 0
#    for r in result:
#        s =  SnowNLP(r['comment'])
#        print(s.words)
#        print(s.sentiments)

    str = ""
    for r in result:
        str+= "".join(r['comment'])

    wordcloud = WordCloud(font_path="./data/simfang.ttf",
                          background_color="white", max_font_size=80).generate(str)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.show()

#getdata_from_mongo()



    #!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import matplotlib.pyplot as plt

from wordcloud import WordCloud
import matplotlib
import pymongo
import csv
from snownlp import SnowNLP

class utils(object):
    client = pymongo.MongoClient(host="localhost", port=27017)
    db =client.zjn
    twitter = db.twitter
    new_twitter = db.new_twitter

    # 去除原始数据库里面的 url,并建立 new_twitter 数据库
    def remove_url(self):
        self.new_twitter.drop()
        data = self.twitter.find()
        for text in data:
            comment = text['comment']
            index = re.search("http", comment)
            if index is not None:
                comment = comment[:index.start()]
            del text["_id"]
            new_text = text
            new_text["comment"] = comment
            self.new_twitter.insert_one(new_text)

        for text in self.new_twitter.find():
            #print(text['comment'])
            pass

    def save_to_csv(self,filename,fieldnames,data):
        positive = []
        negative = []
        with open(filename, 'w') as f:
            w = csv.writer(f)
            w.writerow(fieldnames)
            line_sum = []
            for line in data:
                w.writerow(line)
                line_sum.append(line[-1])
                if line[-1] < 0.5:
                    negative.append(line)
                else:
                    positive.append(line)
            w.writerow(["正面个数："+ str(len(positive))])
            w.writerow(["负面个数："+ str(len(negative))])
            w.writerow(["大众态度："+ str(sum(line_sum)/len(line_sum))])


    # 从mongoDB 获取原始 数据， 经过处理过的数据，去除了 评论里的 url
    def MongoData_to_csv(self):
        with open("原始数据.csv", 'w') as f:
            w = csv.writer(f)
            w.writerow("评论")
            for line in self.twitter.find():
                line = []
                line.append(line['comment'])
                w.writerow(line)

    # 去除重复的评论
    def remove_same_comment(self):
        s = set()
        for text in self.new_twitter.find():
            s.add(text['comment'])
        self.new_twitter.drop()
        for text in s:
            self.new_twitter.insert_one({"comment": text})

    # 绘制词云
    def wordcloud(self,words_count):
        matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
        wordcloud = WordCloud(font_path="./data/simfang.ttf",
                              background_color="white", max_font_size=80)
        word_frequence = {x[0]: x[1] for x in words_count.head(100).values}
        wordcloud = wordcloud.fit_words(word_frequence)
        plt.imshow(wordcloud)
        # 输出词云图片
        plt.show()

    '''
    越接近1表示正面情绪

    越接近0表示负面情绪
    '''
    def get_result(self,comment):
        s = SnowNLP(comment)
        #print(s.words)
        #print(s.sentiments)
        return s
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from Clean_stopwords import clean_punctuation, clean_stopwords
import pandas as pd
import numpy
import utils

MONGO_HOST = "localhost"
MONGO_PORT = 27017

if __name__ == "__main__":
    util = utils.utils()
    client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT)
    db = client.zjn
    new_twitter = db.new_twitter
    data = new_twitter.find()
    contents = []
    for text in data:
        comment = clean_punctuation(text)
        if len(comment) != 0:
            contents.append(comment)

    contents_clean, all_words = clean_stopwords(contents,"stopWord.txt")

    df_content_Clean = pd.DataFrame({'contents_clean': contents_clean})
    # print(df_content.head())
    df_all_words = pd.DataFrame({"all_words": all_words})
    # print(df_all_words.head())
    words_count = df_all_words.groupby(by=['all_words'])['all_words'].agg({"count": numpy.size})
    words_count = words_count.reset_index().sort_values(by=["count"],
                                                        ascending=False)
    print(words_count.head())

    # 输出 词云
    util.wordcloud(words_count)


    list = df_content_Clean.contents_clean.values.tolist()
    all_lines = []
    for line in list:
        line_text = []
        text = ' '.join(line)
        s = util.get_result(text)

        # 正负面也测值
        sentiments = s.sentiments

        # 关键词抽取
        keywords = s.keywords(limit=10)

        # 概括性总结文章
        summary = s.summary(limit=4)

        line_text.append(text)
        line_text.append(keywords)
        line_text.append(summary)
        line_text.append(sentiments)
        all_lines.append(line_text)

    print(len(all_lines))
    util.save_to_csv("twitter_analysis.csv",['评论','关键字','概括','情感偏向'],all_lines )


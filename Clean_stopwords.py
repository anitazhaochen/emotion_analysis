#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jieba
import pandas as pd
import pymongo
import test
import numpy
import re
from zhon.hanzi import punctuation
from zhon.hanzi import non_stops
from zhon.hanzi import stops

def clean_stopwords(contents, path):
    stopwords = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]
    contents_clean = []
    all_words = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords or word is ' ':
                # print(word)
                continue
            line_clean.append(word)
            all_words.append(str(word))
        if len(line_clean) != 0:
            contents_clean.append(line_clean)
    return contents_clean, all_words

def clean_punctuation(text):
    comment = re.sub(r"[%s]+" % punctuation, "", text["comment"])
    comment = re.sub(r"[%s]+" % stops, "", comment)
    comment = re.sub(r"[%s]+" % non_stops, "", comment)
    punc = '[,.!\'\/#@$-:：\?？]'
    comment = re.sub(punc, '', comment)
    comment = comment.strip().replace("\n",'')
    comment = jieba.lcut(comment)
    return comment


if __name__ == "__main__":
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client.zjn
    new_twitter = db.new_twitter
    data = new_twitter.find()
    contents = []
    for text in data:
        comment = clean_punctuation(text)
        if len(comment) != 0:
            contents.append(comment)
    contents_clean, all_words = clean_stopwords(contents,"stopWord.txt")

    df_content = pd.DataFrame({'contents_clean': contents_clean})
    # print(df_content.head())
    df_all_words = pd.DataFrame({"all_words": all_words})
    # print(df_all_words.head())
    words_count = df_all_words.groupby(by=['all_words'])['all_words'].agg({"count": numpy.size})
    words_count = words_count.reset_index().sort_values(by=["count"],
                                                        ascending=False)
    print(words_count.head())
    test.wordcloud(words_count)


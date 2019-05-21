#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pymongo
import time
import csv

client = pymongo.MongoClient(host="localhost", port=27017)
db =client.zjn
twitter = db.twitter
new_twitter = db.new_twitter
new_twitter.drop()

def remove_url():
    data = twitter.find()
    for text in data:
        comment = text['comment']
        index = re.search("http", comment)
        if index is not None:
            comment = comment[:index.start()]
        del text["_id"]
        new_text = text
        new_text["comment"] = comment
        new_twitter.insert_one(new_text)

    for text in new_twitter.find():
        #print(text['comment'])
        pass

def save_to_csv():
    fieldnames = ['comment']
    with open("twitter.csv", 'w') as f:
        w = csv.writer(f)
        w.writerow(fieldnames)
        for di in new_twitter.find():
            line = []
            line.append(di['comment'])
            w.writerow(line)

def remove_same_comment():
    s = set()
    for text in new_twitter.find():
        s.add(text['comment'])
    new_twitter.drop()
    for text in s:
        new_twitter.insert_one({"comment":text})

if __name__ == "__main__":
    remove_url()
    remove_same_comment()
    save_to_csv()


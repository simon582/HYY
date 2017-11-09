# coding:utf-8

import jieba
import pymongo
import pdb
from jieba import analyse
import json

jieba.initialize()

conn = pymongo.MongoClient()
hyy_db = conn['hyy']

stopwords = set()
for line in open('stopwords.txt'):
    stopwords.add(line.strip())

def handle_text(text):
    global stopwords
    type_words = jieba.posseg.cut(text)
    text_list = [w.word for w in type_words if len(w.word) > 1 and ('n' in w.flag or 'v' in w.flag)]
    word_dict = {}
    for word in text_list:
        if word in stopwords:
            continue
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    return word_dict

cnt = 0
for prod in hyy_db.work.find({}):
    #print prod
    doc_id = prod['doc_id']
    text = prod['text'].replace('<p>','').replace('</p>','')
    text_dict = handle_text(prod['text'])
    title_dict = handle_text(prod['title'])
    for word, word_cnt in title_dict.items():
        if word in text_dict:
            text_dict[word] += 100 * word_cnt
        else:
            text_dict[word] = 100 * word_cnt

    for prefix, word_cnt in text_dict.items():
        resp = hyy_db.index.find_one({'prefix':prefix})
        if resp:
            # update
            existed = False
            for doc in resp['doc_list']:
                if doc_id == doc[0]:
                    existed = True
                    break
            if existed:
                continue
            resp['doc_list'].append((doc_id, word_cnt))
            del(resp['_id'])
            hyy_db.index.update({'prefix':prefix},{'$set':resp})
        else:
            # create
            new_prod = {}
            new_prod['prefix'] = prefix
            new_prod['doc_list'] = [(doc_id, word_cnt)]
            hyy_db.index.save(new_prod)
    del(prod['_id'])
    #hyy_db.work.save(prod)
    #hyy_db.temp.remove(prod)
    cnt += 1
    print doc_id, cnt

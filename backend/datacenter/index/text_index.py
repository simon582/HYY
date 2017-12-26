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

def main():
    cnt = 0
    for prod in hyy_db.temp.find({}):
        #print prod
        doc_id = prod['doc_id']
        text = prod['text'].replace('<p>','').replace('</p>','')
        text_dict = handle_text(prod['text'])
        title_dict = handle_text(prod['title'])
        for word, word_cnt in title_dict.items():
            if word in text_dict:
                text_dict[word] += 1000 + 10 * (word_cnt - 1)
            else:
                text_dict[word] = 1000 + 10 * (word_cnt - 1)

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
        try:
            hyy_db.work.save(prod)
        except Exception as e:
            print e
        try:
            hyy_db.temp.remove({'doc_id':prod['doc_id']})
        except Exception as e:
            print e
        cnt += 1
        print doc_id, cnt

if __name__ == "__main__":
    main()
    '''
    text = '关于湖南省第二类医疗器械注册申请项目临床试验监督抽查有关情况的公告（湘食药监公告〔2016〕第33号）'
    d = handle_text(text)
    for k,v in d.items():
        print k,v
    '''

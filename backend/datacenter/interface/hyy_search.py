# -*- coding:utf-8 -*-

import sys
import datetime
import time
import json
import socket
import traceback
import random
import copy
import jieba
from jieba import analyse
import pymongo
sys.path.append('./gen-py/')
sys.path.append('./base/')
sys.path.append('../spider/dxy/')
sys.path.append('../spider/baidu/')
reload(sys)
sys.setdefaultencoding('utf-8')

import dxy_search
from utils import WriteLog
from data import HyySearchService
from data import ttypes
from data import constants

class HYYSearcher(object):

    def __init__(self):

        try:
            jieba.initialize()
        except Exception as e:
            print e
            exit(-1)
        try:
            self.mongo_conn = pymongo.MongoClient()
            self.hyy_db = self.mongo_conn['hyy']
        except Exception as e:
            print e
            exit(-1)

    def _get_words(self, query):

        type_words = jieba.posseg.cut(query)
        w_list = [w.word for w in type_words if len(w.word) > 1 and ('n' in w.flag or 'v' in w.flag)]
        return w_list

    def _handle_recent_value(self, datetime):

        try:
            pub_time = time.mktime(time.strptime(datetime, '%Y-%m-%d'))
            delta_time = time.time() - pub_time
            delta_days = delta_time / 3600 / 24
            base = 365 * 2
            return (base - delta_days) / base * 500
        except:
            return 0

    def _get_doc_from_index(self, query, word_list, topN=50):

        stat_doc = {}
        for word in word_list:
            prod = self.hyy_db.index.find_one({'prefix':word})
            if not prod:
                continue
            for doc in prod['doc_list']:
                doc_id = doc[0]
                doc_cnt = doc[1]
                prod = self.hyy_db.work.find_one({'doc_id':doc_id})
                if doc_id in stat_doc:
                    stat_doc[doc_id] += doc_cnt
                    # 全字匹配
                    if prod['title'].find(query) != -1:
                        stat_doc[doc_id] += 1000
                else:
                    stat_doc[doc_id] = doc_cnt + self._handle_recent_value(prod['datetime'])
                #print word, doc_id, stat_doc[doc_id]
        doc_list = sorted(stat_doc.iteritems(), key=lambda d:d[1], reverse=True)
            
        top_list = []
        rest_list = [] 
        for doc_id, cnt in doc_list[:topN]:
            hyy_doc = copy.copy(ttypes.HyyDoc())
            prod = self.hyy_db.work.find_one({'doc_id':doc_id})
            hyy_doc.title = prod['title'].encode('utf-8')
            hyy_doc.doc_id = prod['doc_id']
            hyy_doc.author = prod['author']
            hyy_doc.datetime = prod['datetime']
            hyy_doc.source = prod['source']
            hyy_doc.source_icon = prod['source_icon']
            hyy_doc.source_desc = prod['source_desc']
            hyy_doc.detail_url = prod['detail_url']
            hyy_doc.text = prod['text'].encode('utf-8')
            # for test
            #print hyy_doc.title, hyy_doc.datetime, cnt
            if stat_doc[prod['doc_id']] >= 1000:
                top_list.append(hyy_doc)
            else:
                rest_list.append(hyy_doc)
        return top_list, rest_list

    def _get_query(self, query_dict):
        '''
        doc = ttypes.HyyDoc()
        doc.doc_id = '123'
        doc.title = '肚子疼怎么回事'
        doc.author = '妖刀5VY'
        doc.datetime = '2013-12-04 09:19'
        doc.source = '百度'
        doc.source_icon = 'http://iknowpc.bdimg.com/static/question/widget/sample/top-nav-bar/img/zhidao-logo_b9ec675.png'
        doc.source_desc = '百度知道'
        doc.text = open('mock.txt').read().strip()
        return [doc, doc, doc, doc]
        '''
        dxy_list = dxy_search.query(query_dict['query'])
        n_list = self._get_words(query_dict['query'])
        top_list, rest_list = self._get_doc_from_index(query_dict['query'], n_list)
        #top_list = sorted(top_list, key=lambda d:d.datetime, reverse=True)

        WriteLog('NOTICE', 'dxy size:%d, top size:%d, rest size:%d' % (len(dxy_list), len(top_list), len(rest_list)))
        
        return top_list + dxy_list + rest_list
 
    def _get_result(self, query):
        '''
        if query.find('query=') != -1:
            keyword = query.split('query')[1]
            return self._get_query(keyword) 
        '''
        parts = query.split('&')
        query_dict = {}
        for p in parts:
            k, v = p.split('=')
            query_dict[k] = v
        if not 'query' in query_dict:
            return []
        return self._get_query(query_dict)

    def GetSearchResult(self, hyy_search_request):

        try:
            hyy_search_response = ttypes.HyySearchResponse()
            hyy_search_response.qid = hyy_search_request.qid
            hyy_search_response.doc_list = self._get_result(hyy_search_request.data)
            WriteLog('NOTICE', 'qid:%s, data:%s' % (hyy_search_request.qid, hyy_search_request.data))
            return hyy_search_response   
        except:
            traceback.print_exc()
            return None

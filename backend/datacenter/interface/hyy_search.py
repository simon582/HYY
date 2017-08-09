# -*- coding:utf-8 -*-

import sys
import datetime
import time
import json
import socket
import traceback
sys.path.append('./gen-py/')
sys.path.append('./base/')
sys.path.append('../spider/dxy/')
sys.path.append('../spider/baidu/')
reload(sys)
sys.setdefaultencoding('utf-8')

import dxy_search
import baidu_search
from utils import WriteLog
from data import HyySearchService
from data import ttypes
from data import constants

class HYYSearcher(object):

    def __init__(self):

        pass

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
        #doc_list = dxy_search.query(keyword)
        if 'site' in query_dict:
            if query_dict['site'] == 'baidu':
                doc_list = baidu_search.query(query_dict)
        WriteLog('NOTICE', 'query size:%d' % len(doc_list))
        return doc_list
    
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
        if not 'page' in query_dict:
            query_dict['page'] = 1
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

# -*- coding:utf-8 -*-

import sys
import datetime
import time
import json
import socket
import traceback
import MySQLdb
import jieba
from jieba import analyse
sys.path.append('./gen-py/')
sys.path.append('./base/')
reload(sys)
sys.setdefaultencoding('utf-8')
from utils import WriteLog
from data import CoreQueryService
from data import ttypes
from data import constants

class CoreQueryer(object):

    def __init__(self, cnf_dict):
        
        jieba.initialize()
        self.textrank = analyse.textrank
        self.cursor = self.create_connection(cnf_dict)

    def create_connection(self, cnf_dict):
        
        try:
            conn = MySQLdb.connect(host=cnf_dict['mysql_host'], user=cnf_dict['mysql_user'],
                                   passwd=cnf_dict['mysql_passwd'], db=cnf_dict['mysql_db'], charset='utf8')
            cur = conn.cursor()
            WriteLog('NOTICE', 'MySQL connection created successfully')
            return cur
        except MySQLdb.Error, e:
            WriteLog('ERROR', 'MySQL occur an error: %d: %s' % (e.args[0], e.args[1]))

    def _utf8(self, word_list):

        return [w.encode('utf-8') for w in word_list]

    def _get_mapping(self):
        
        map_dict = {}
        try:
            cnt = self.cursor.execute('select folknik,pro from professional')
            results = self.cursor.fetchall()
            for row in results:
                if not row[0] in map_dict:
                    map_dict[row[0]] = [row[1]]
                else:
                    map_dict[row[0]].append(row[1])
        except MySQLdb.Error, e:
            WriteLog('WARN', 'MySQL query error: %d: %s' % (e.args[0], e.args[1]))
        return map_dict 
        
        
    def _get_result(self, query):

        word_list = []
        map_dict = self._get_mapping()
        for nik, pro in map_dict.items():
            if nik in query:
                word_list += pro
        word_list = self._utf8(word_list)
        print 'pro:' + '|'.join(word_list)
        tr_list = self._utf8(self.textrank(query))
        print 'textrank:' + '|'.join(tr_list)
        tag_list = self._utf8(analyse.extract_tags(query, topK=3))
        print 'TF-IDF:' + '|'.join(tag_list)
        type_words = jieba.posseg.cut(query)
        n_list = self._utf8([w.word for w in type_words if 'n' in w.flag or 'v' in w.flag])
        print 'nous:' + '|'.join(n_list)
        return list(set(word_list + tr_list + tag_list + n_list))

    def GetCoreWords(self, core_query_request):

        try:
            core_query_response = ttypes.CoreQueryResponse()
            core_query_response.qid = core_query_request.qid
            core_query_response.word_list = self._get_result(core_query_request.data)
            WriteLog('NOTICE', 'qid:%s, data:%s' % (core_query_request.qid, core_query_request.data))
            return core_query_response
        except:
            traceback.print_exc()
            return None

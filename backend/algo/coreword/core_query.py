# -*- coding:utf-8 -*-

import sys
import datetime
import time
import json
import socket
import traceback
import MySQLdb
import re
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
        self.cnf_dict = cnf_dict
        self.cursor = self.create_connection(cnf_dict)
        self.stopwords = self._get_stopwords(cnf_dict)

    def _get_stopwords(self, cnf_dict):

        stopwords = set()
        for line in open(cnf_dict['stopword_path']):
            stopwords.add(line.strip())
        return stopwords

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

        return [w.encode('utf-8') for w in word_list if len(w) > 1]

    def _get_mapping(self):
        
        map_dict = {}
        try:
            cnt = self.cursor.execute('select synonym from synonym')
            results = self.cursor.fetchall()
            for row in results:
                '''
                if not row[0] in map_dict:
                    map_dict[row[0]] = [row[1]]
                else:
                    map_dict[row[0]].append(row[1])
                '''
                items = row[0].strip().split('|')
                for i in range(len(items)):
                    for j in range(len(items)):
                        if i == j:
                            continue
                        if not items[i] in map_dict:
                            map_dict[items[i]] = [items[j]]
                        else:
                            map_dict[items[i]].append(items[j])
        except MySQLdb.Error, e:
            WriteLog('WARN', 'MySQL query error: %d: %s' % (e.args[0], e.args[1]))
        
        try:
            cnt = self.cursor.execute('select word, result from word_distinguish where type=10')
            results = self.cursor.fetchall()
            for row in results:
                word = row[0]
                result = row[1].strip().split('|')
                if not word in map_dict:
                    map_dict[word] = result
                else:
                    map_dict[word] += result
        except MySQLdb.Error, e:
            WriteLog('WARN', 'MySQL query error: %d: %s' % (e.args[0], e.args[1]))

        return map_dict 
        
    def _get_distinguish(self):

        dist_dict = {}
        try:
            cnt = self.cursor.execute('select word,result from word_distinguish where type<>10')
            results = self.cursor.fetchall()
            for row in results:
                if not row[0] in dist_dict:
                    dist_dict[row[0]] = [row[1]]
                else:
                    dist_dict[row[0]].append(row[1])
        except MySQLdb.Error, e:
            WriteLog('WARN', 'MySQL query error: %d: %s' % (e.args[0], e.args[1]))
        pattern_list = dist_dict.keys()
        pattern_list.sort(key=lambda x:len(x), reverse=True)
        return dist_dict, pattern_list

    def _get_search_index(self):

        index_dict = {}
        try:
            cnt = self.cursor.execute('select field_name,value from search_index')
            results = self.cursor.fetchall()
            for row in results:
                try:
                    index_dict[row[1].encode('utf-8')] = row[0].enocde('utf-8')
                except:
                    pass
        except MySQLdb.Error, e:
            WriteLog('WARN', 'MySQL query error: %d: %s' % (e.args[0], e.args[1]))
        return index_dict

    def _find_distinguish(self, query, dist_dict, pattern_list, word_list):

        for pattern in pattern_list:
            results = dist_dict[pattern]
            try:
                p = re.compile(pattern.encode('utf-8'))
                match = re.search(p, query)
                if match:
                    if len(results) == 1 and pattern == results[0]:
                        word_list.append(match.group())
                    else:
                        word_list += results
                    query = p.sub('', query)
            except:
                WriteLog('WARN', 'Cannot analyze pattern:%s' % pattern)
        return query

    def _add_word(self, word_list, word):

        existed = False
        word = word.encode('utf-8')
        for word_set in word_list:
            if word in word_set:
                existed = True
                break
        if not existed:
            word_list.append([word])

    def _add_pro(self, word_list, nik, pro):

        existed = False
        nik = nik.encode('utf-8')
        pro = self._utf8(pro)
        for sub_list in word_list:
            if nik in sub_list:
                sub_list += pro
                existed = True
                break
        if not existed:
            word_list.append(pro+[nik])

    def _pre_process(self, query):

        query = query.replace('（', '(')
        query = query.replace('）', ')')
        return query

    def _get_result(self, query):

        query = self._pre_process(query)
        word_list = []
        self.cursor = self.create_connection(self.cnf_dict)
        map_dict = self._get_mapping()
        dist_dict, pattern_list = self._get_distinguish()
        #index_dict = self._get_search_index()

        temp_list = []
        query = self._find_distinguish(query, dist_dict, pattern_list, temp_list)
        for w in temp_list:
            word_list.append([w.encode('utf-8')])
            w = w.decode('utf-8')
            if w in map_dict:
                self._add_pro(word_list, w, map_dict[w])
        for nik, pro in map_dict.items():
            if nik in query:
                self._add_pro(word_list, nik, pro)

        temp_list = []        
        tr_list = self._utf8(self.textrank(query))
        print 'textrank:' + '|'.join(tr_list)
        tag_list = self._utf8(analyse.extract_tags(query, topK=3))
        print 'TF-IDF:' + '|'.join(tag_list)
        type_words = jieba.posseg.cut(query)
        n_list = self._utf8([w.word for w in type_words if 'n' in w.flag or 'v' in w.flag])
        print 'nous:' + '|'.join(n_list)
        sum_list = list(set(temp_list + tr_list + tag_list + n_list) - self.stopwords)
        for w in sum_list:
            self._add_word(word_list, w)
       
        ''' 
        for word_set in word_list:
            for i in range(len(word_set)):
                if word_set[i] in index_dict:
                    word_set[i] += '&' + index_dict[word_set[i]]
                else:
                    word_set[i] += '&null'
        '''

        res_list = []
        for word_set in word_list:
            res_list.append('|'.join(word_set))
        print res_list
        #import pdb;pdb.set_trace()
        return res_list

    '''
    def _get_result(self, query):
        
        word_list = []
        self.cursor = self.create_connection(self.cnf_dict)
        map_dict = self._get_mapping()
        dist_dict = self._get_distinguish()

        query = self._find_distinguish(query, dist_dict, word_list)
        print 'distinguish:' + '|'.join(word_list)

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
        return list(set(word_list + tr_list + tag_list + n_list) - self.stopwords)
    '''

    def GetCoreWords(self, core_query_request):

        try:
            core_query_response = ttypes.CoreQueryResponse()
            core_query_response.qid = core_query_request.qid
            core_query_response.word_list = self._get_result(core_query_request.data)
            WriteLog('NOTICE', 'qid:%s, query:%s, core:%s' % (core_query_request.qid, core_query_request.data,
                                                              '|'.join(core_query_response.word_list)))
            return core_query_response
        except:
            traceback.print_exc()
            return None

# -*- coding:utf-8 -*-
# Copyright: Zhejiang Tachao Technology Inc.
# Author: Shao Xinqi
# Date: 2016-07-20
# Description: simple decision engine

import sys
import datetime
import time
import json
import socket
import traceback
sys.path.append('./gen-py/')
sys.path.append('./base/')

from utils import WriteLog
from data import HyySearchService
from data import ttypes
from data import constants

class HYYSearcher(object):

    def __init__(self):

        pass

    def _get_result(self, query):

        return []

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

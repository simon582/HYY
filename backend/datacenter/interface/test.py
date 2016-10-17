# -*- coding:utf-8 -*-
# Copyright: Zhejiang Tachao Technology Inc.
# Author: Shao Xinqi
# Date: 2016-07-20
# Description: start SDE via thrift

import traceback
import sys
import datetime
import time
import json
import copy
import socket
sys.path.append('./gen-py/')
sys.path.append('./base/')

from utils import WriteLog
from data import HyySearchService
from data import ttypes
from data import constants

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

transport = TSocket.TSocket('127.0.0.1', 8080)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = HyySearchService.Client(protocol)
transport.open()
print 'create client successfully'

request = ttypes.HyySearchRequest()
request.qid = '123'
request.data = 'cat=123&query=胃病'
try:
    response = client.GetSearchResult(request)
    print response.qid
    print response.doc_list
except:
    print 'refused'
    traceback.print_exc()

transport.close()

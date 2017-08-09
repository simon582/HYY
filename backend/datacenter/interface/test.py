# -*- coding:utf-8 -*-

import traceback
import sys
import datetime
import time
import json
import copy
import socket
sys.path.append('./gen-py/')
sys.path.append('./base/')

from data import HyySearchService
from data import ttypes
from data import constants

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

#transport = TSocket.TSocket('101.200.175.121', 8080)
transport = TSocket.TSocket('127.0.0.1', 8080)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = HyySearchService.Client(protocol)
transport.open()
print 'create client successfully'

request = ttypes.HyySearchRequest()
request.qid = '123'
request.data = 'query=网络安全法&site=baidu&page=1'
try:
    response = client.GetSearchResult(request)
    print response.qid
    print len(response.doc_list)
    for doc in response.doc_list:
        print doc.doc_id
        print doc.title
except:
    print 'refused'
    traceback.print_exc()

transport.close()

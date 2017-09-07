# -*- coding:utf-8 -*-

import traceback
import sys
import datetime
import time
import json
import copy
import socket
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('./gen-py/')
sys.path.append('./base/')

from data import CoreQueryService
from data import ttypes
from data import constants

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

transport = TSocket.TSocket('101.200.175.121', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = CoreQueryService.Client(protocol)
transport.open()
print 'create client successfully'

request = ttypes.CoreQueryRequest()
request.qid = '123'
#request.data = 'anca(+)'
request.data = '红斑'
#request.data = '带状疱疹存在哪些虚假医疗或过度诊疗的现象'
#request.data = '克罗恩病存在哪些虚假医疗或过度诊疗的现象'
#request.data = '拉肚子会是什么疾病呢'
#request.data = '抗dsDNA抗体阳性病因'
#request.data = '脸上有红斑、关节疼会是什么疾病？'
print 'query:' + request.data
try:
    response = client.GetCoreWords(request)
    print 'qid:' + response.qid
    print 'core:' + ','.join(response.word_list)
except:
    traceback.print_exc()
transport.close()

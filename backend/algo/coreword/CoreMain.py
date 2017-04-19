# -*- coding:utf-8 -*-

import sys
import datetime
import time
import json
import socket
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('./gen-py/')
sys.path.append('./base/')

import utils
from data import CoreQueryService
from data import ttypes
from data import constants
from core_query import CoreQueryer

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

def run(cnf_file_path):

    cnf_keys = ['thrift_server']
    cnf_dict = utils.ReadCnf(cnf_file_path, cnf_keys)
    
    queryer = CoreQueryer(cnf_dict)
    processor = CoreQueryService.Processor(queryer)
    addr = cnf_dict['thrift_server'].split(':')[0].strip()
    port = cnf_dict['thrift_server'].split(':')[1].strip()
    transport = TSocket.TServerSocket(addr, port)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    
    # Create a TThreadedServer
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    utils.WriteLog('NOTICE', 'Core Queryer start with TThreadedServer') 
    server.serve()
    
def usage():

    print 'python main.py cnf_file_path'
    exit(-1)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        usage()

    run(sys.argv[1])

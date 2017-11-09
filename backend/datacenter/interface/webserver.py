# -*- coding:utf-8 -*-

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import SimpleHTTPServer
import traceback
import sys
import datetime
import time
import json
import copy
import socket
import shutil
import io
import urllib, urllib2
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

class TestHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def init(self):
        self.transport = TSocket.TSocket('101.200.175.121', 8080)
        #transport = TSocket.TSocket('127.0.0.1', 8080)
        self.transport = TTransport.TBufferedTransport(self.transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = HyySearchService.Client(self.protocol)
        self.transport.open()
        print 'create client successfully'

    def do_GET(self):
        self.init()
        request = ttypes.HyySearchRequest()
        request.qid = '123'
        print 'path:', self.path
        try:
            request.data = urllib.unquote(self.path).split('?')[1].strip()
            print 'data:', request.data
        except:
            return None
        parts = request.data.split('&')
        query_dict = {}
        for p in parts:
            k, v = p.split('=')
            query_dict[k] = v
        if not 'page' in query_dict:
            query_dict['page'] = 1
        else:
            query_dict['page'] = int(query_dict['page'])
        if not 'perpage' in query_dict:
            query_dict['perpage'] = 10
        else:
            query_dict['perpage'] = int(query_dict['perpage'])
        try:
            response = self.client.GetSearchResult(request)
            print response.qid
            print 'size:', len(response.doc_list)
            res_dict = {}
            res_dict['total_size'] = len(response.doc_list)
            res_dict['doc_list'] = []
            st = query_dict['perpage'] * (query_dict['page'] - 1)
            ed = st + query_dict['perpage'] + 1
            for doc in response.doc_list[st:ed]:
                docd = {}
                docd['doc_id'] = doc.doc_id
                docd['title'] = doc.title
                docd['author'] = doc.author
                docd['datetime'] = doc.datetime
                docd['source'] = doc.source
                docd['text'] = doc.text
                docd['short_text'] = doc.short_text
                docd['source_icon'] = doc.source_icon
                docd['source_desc'] = doc.source_desc
                docd['detail_url'] = doc.detail_url
                res_dict['doc_list'].append(docd)
                print doc.title
                print doc.detail_url
                print '-----'
            self.do_response(res_dict)
        except:
            print 'refused'
            traceback.print_exc()

    def do_response(self, res_dict):
        enc = 'UTF-8'
        content = json.dumps(res_dict, ensure_ascii=False, indent=4)
        f = io.BytesIO()
        f.write(content)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc) 
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
        #shutil.copyfileobj(f, self.wfile)   

    def __del__(self):
        self.transport.close()

if __name__ == "__main__":

    http_server = HTTPServer(('101.200.175.121', 9000), TestHTTPHandler)
    http_server.serve_forever()

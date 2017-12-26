# -*- coding:utf-8 -*-

# Copyright: Zhejiang Tachao Technology Inc.
# Author: Shao Xinqi
# Date: 2016-07-14
# Description: some base functions of spiders

import datetime
import requests
import time
import urllib
import urllib2
import cookielib
import os
import traceback
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
Summary: Get HTML document via url
Parameters:
  crawl_url: destination of url
  cookie_file_path: if the page needs cookie to be crawled, put the cookie file path in cookie_file
  post_data: if the page needs post data in form, put the dict value in post_data
  decode: decode, default is GBK
Return:
  HTML document, string type
'''
def GetHTML(crawl_url, cookie_file_path='', post_data={}, ext_headers={}, decode='gbk'):

    timeout_limit = 10
    cookie_jar = cookielib.CookieJar()
    build_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
    request = urllib2.Request(crawl_url)
    request.add_header('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36')
    for key, value in ext_headers.items():
        request.add_header(str(key), str(value))

    if cookie_file_path != '':
        with open(cookie_file_path, 'r') as cookie_file:
            cookie = cookie_file.read().strip()
        request.add_header('Cookie', cookie)

    html_document = ''
    try:
        html_document = build_opener.open(request, timeout = timeout_limit).read().decode(decode)
    except:
        traceback.print_exc()

    with open('test_GetHTML.html', 'w') as test_file:
        print >> test_file, html_document

    return html_document

'''
Summary: Write log
Parameters:
  level: from top to bottom: ERROR > WARN > NOTICE > DEBUG
  log_text: log string
  log_path: log file location
Return:
  Boolean value stand for whether the log is written
'''
g_log_level = {
    'DEBUG' : 0,
    'NOTICE' : 1,
    'WARN' : 2,
    'ERROR' : 3,
}
def WriteLog(level, log_text, screen = True, log_path = './log/'):

    global g_log_level
    output_threshold = 'DEBUG'
    
    if g_log_level[level] < g_log_level[output_threshold]:
        return
    
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    current_datetime = datetime.datetime.now()
    current_date = current_datetime.strftime('%Y-%m-%d')
    current_time = current_datetime.strftime('%H:%M:%S')
    out_line = '[%s][%s]%s' % (current_time, level, log_text)

    if screen:
        print out_line
    try:
        with open(log_path + 'corequery.%s.log' % current_date, 'a') as log_file:
            print >> log_file, out_line
    except:
        print 'Write failed!'
        traceback.print_exc()
        return False
    return True

def ReadCnf(cnf_file_path, cnf_keys):
    
    cnf_dict = {}

    if not os.path.exists(cnf_file_path):
        print 'Cnf file does not exist! path:%s' % cnf_file_path
        exit(-1)
    with open(cnf_file_path, 'r') as cnf_file:
        for line in cnf_file.readlines():
            line = line.strip()
            if line == "" or line[0] == '#':
                continue
            parts = line.split('=')
            cnf_dict[parts[0].strip()] = parts[1].strip()

    # judge all need keys
    for key in cnf_keys:
        if not key in cnf_dict:
            print 'Cannot find key %s in cnf!' % key
            exit(-1)

    return cnf_dict

# -*- coding:utf-8 -*-

import requests
import traceback
import scrapy
import urllib
import urllib2
import cookielib
import hashlib
import copy
import sys
sys.path.append('../../interface/gen-py/')
from data import ttypes
from data import constants
reload(sys)
sys.setdefaultencoding('utf-8')

def GetHTML(crawl_url, cookie_file_path='', post_data={}, ext_headers={}, decode='utf-8'):

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

def GetDetail(url):

    headers = {
        'Host':'search.dxy.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    }
    url = url.split('?')[0]
    #hxs = scrapy.Selector(text=GetHTML(url, cookie_file_path='cookie', ext_headers=headers))
    hxs = scrapy.Selector(text=GetHTML(url))
    text = ''
    for p in hxs.xpath('//div[@class="editor-body"]/p/text() \
                        |//div[@class="editor-body"]/h2/text() \
                        |//div[@class="editor-body"]/div/text()'):
        text += p.extract().strip() + '\n'
    return text

'''
    Input:
        keyword
    Output:
        List of docs
'''
def query(keyword):

    headers = {
        'Host':'search.dxy.cn',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
    }
    request_url = 'http://search.dxy.cn/?words=%s&source=DXYS&limit=15' % urllib.quote(keyword)
    hxs = scrapy.Selector(text=GetHTML(request_url, ext_headers=headers))
    doc_list = []
    div_list = hxs.xpath('//div[@class="main-list"]/div')
    if len(div_list) == 0:
        return []
    for div in div_list:
        if len(doc_list) > 7:
            break
        doc = copy.copy(ttypes.HyyDoc())
        t_list = div.xpath('./h3/a/text()|./h3/a/em/text()')
        doc.title = ''.join([t.extract() for t in t_list]).encode('utf-8')
        #print 'title:' + doc.title
        url = div.xpath('./h3/a/@href')[0].extract()
        #print 'url:' + url
        doc.detail_url = url
        doc.source = '丁香园'
        doc.source_desc = '丁香医生'
        doc.source_icon = 'http://assets.dxycdn.com/app/dxy/img/logo@2x2.png'
        doc.author = '丁香医生'
        doc.datetime = ''
        t_list = div.xpath('.//p[@class="it-author"]/text()')
        for t in t_list:
            t = t.extract()
            if t.find('201') != -1:
                doc.datetime = t.strip()
        #print 'datetime:' + doc.datetime
        doc.doc_id = hashlib.md5(url).hexdigest()
        doc.text = GetDetail(url).encode('utf-8')
        #print 'text:' + doc.text
        if doc.doc_id == None:
            continue
        doc_list.append(doc)
    #print doc_list   
    return doc_list

if __name__ == "__main__":
   query('肚子疼') 

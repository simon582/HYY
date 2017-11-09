# -*- coding:utf-8 -*-

import requests
import pymongo
import scrapy
import hashlib
import json
import sys
sys.path.append('../proxy/')
from abuyun import abuyunGet
reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):

    headers = {
        'Host':'www.sda.gov.cn',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Referer':'http://www.sda.gov.cn/WS01/CL1103/index_1.html',
    }
    retry_times = 0
    while retry_times < 5:
        try:
            #r = requests.get(url, headers=headers, timeout=10)
            r = abuyunGet(url, headers=headers)
            html = r.content.decode('gb2312','ignore')
            if len(html.strip()) == 0:
                print 'invalid html length: 0'
                continue
            with open('test.html','w') as f:
                print >> f, html
            return html
        except Exception as e:
            print e
            retry_times += 1
            print 'retry times:', retry_times
    return ''

def crawl_detail(prod):

    prod['author'] = 'CFDA'
    prod['source'] = 'CFDA'
    prod['source_desc'] = '国家食品药品监督管理总局'
    prod['text'] = ''
    prod['short_text'] = ''
    prod['source_icon'] = 'http://www.ythaian.com/UpFile/Image/2015-12/Ew_20151221085022502.png'
    prod['doc_id'] = hashlib.md5(prod['detail_url']).hexdigest()

    hxs = scrapy.Selector(text=get_html(prod['detail_url']))
    text_list = []
    for text in hxs.xpath('//td[@class="articlecontent3"]/p/text()'):
        text = text.extract().strip()
        if len(text) == 0:
            continue
        text_list.append(text)
        prod['text'] += '<p>%s</p>' % text
    #print json.dumps(prod, indent=4)


try:
    mongo_conn = pymongo.MongoClient()
    news_db = mongo_conn['hyy']
except Exception as e:
    print e
    exit(0)

def save_db(prod):

    global news_db
    try:
        news_db.temp.save(prod)
    except Exception as e:
        print e
    
def crawl_list(cat, cur_url):

    print '===' + cur_url + '==='
    #import pdb;pdb.set_trace()
    try:
        hxs = scrapy.Selector(text=get_html(cur_url))
    except Exception as e:
        print e
        print 'requests error, skip:' + cur_url
        return False
    tr_list = hxs.xpath('//td[@class="2016_erji_content"]/table/tbody/tr')
    if len(tr_list) == 0:
        print 'no items, skip:' + cur_url
        return False
    for tr in tr_list:
        try:
            prod = {}
            prod['title'] = tr.xpath('./td/a/font/text()')[0].extract()
            prod['detail_url'] = 'http://www.sda.gov.cn/WS01' + tr.xpath('./td/a/@href')[0].extract().split('..')[1]
            prod['datetime'] = tr.xpath('./td/span[@class="listtddate15"]/text()')[0].extract().strip()[1:-1]
            crawl_detail(prod)
            save_db(prod)
        except Exception as e:
            print e
    return True

if __name__ == "__main__":

    for line in open('guide.txt'):
        cat, url = line.strip().split(',')
        page = 0
        while True:
            if page == 0:
                cur_url = url
            else:
                cur_url = url + 'index_%d.html' % page
            if not crawl_list(cat, cur_url):
                break
            page += 1

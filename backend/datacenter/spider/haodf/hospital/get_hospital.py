# coding:utf-8

import scrapy
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
}

def work(province, url):

    print province, url
    headers['Host'] = url.split('/')[-1]
    r = requests.get(url, headers=headers)
    html = r.text
    with open('test.html', 'w') as f:
        print >> f, html
    hxs = scrapy.Selector(text=html)
    for tr in hxs.xpath('//table[@class="jblb"]/tr'):
        for td in tr.xpath('./td'):
            try:
                hospital = td.xpath('./a/text()')[0].extract()
                url = td.xpath('./a/@href')[0].extract()
                line =  province + ',' + hospital + ',' + url
                with open('hospital.txt', 'a') as f:
                    print >> f, line
            except Exception as e:
                print e

for line in open('province.txt'):
    province, url = line.strip().split(',')
    work(province, url)

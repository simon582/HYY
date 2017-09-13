# coding:utf-8

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

html = open('test.html', 'r').read()
hxs = scrapy.Selector(text=html)

for tr in hxs.xpath('//table/tbody/tr'):
    for td in tr.xpath('./td'):
        try:
            url = td.xpath('./a/@href')[0].extract()
            city = td.xpath('./a/text()')[0].extract()
            print city + ',' + url
        except:
            continue

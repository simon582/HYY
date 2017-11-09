# coding:utf-8

import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('guide.html', 'r') as f:
    html = f.read()

hxs = scrapy.Selector(text=html)

for td in hxs.xpath('//td[@class="menucont"]'):

    for a in td.xpath('./a'):
        try:
            title = a.xpath('./@title')[0].extract()
            url = a.xpath('./@href')[0].extract()
            url = 'http://www.sda.gov.cn/WS01' + url.split('..')[1]
            print title + ',' + url
        except:
            pass

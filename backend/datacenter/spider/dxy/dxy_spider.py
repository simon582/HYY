# -*- coding:utf-8 -*-

from dxy_search import GetHTML
import scrapy
import datetime
import time
import BeautifulSoup

def crawl_detail(prod):

    print 'start crawl detail:' + prod['detail_url']
    html_text = GetHTML(prod['detail_url'])
    hxs = scrapy.Selector(text=html_text)
    prod['datetime'] = hxs.xpath('//div[@class="x_box13"]/div[@class="sum"]/span[@class="it"]/text()')[0].extract().strip()
    prod['datetime'] = datetime.datetime.strptime(prod['datetime'], '%Y-%m-%d %H:%M')
    print 'datetime:' + str(prod['datetime'])
    prod['text'] = ''
    soup = BeautifulSoup(html_text)
    
    
def crawl_list(cat, cur_url):

    print 'start crawl cat:' + cat + ', ' + cur_url
    hxs = scrapy.Selector(text=GetHTML(cur_url))
    dl_list = hxs.xpath('//div[@class="x_wrap1 fl"]/dl')
    print 'cnt:' + str(len(dl_list))
    if len(dl_list) == 0:
        return False

    for dl in dl_list:
        prod = {}
        prod['title'] = dl.xpath('.//a[@class="h4"]/@title')[0].extract()
        print 'title:' + prod['title']
        prod['detail_url'] = dl.xpath('.//a[@class="h4"]/@href')[0].extract()
        print 'detail_url:' + prod['detail_url']
        crawl_detail(prod)
        save(prod)

    import pdb;pdb.set_trace()
    return True

def save(prod):

    pass

def work(cat, start_url):

    for page in range(1, 101):
        cur_url = start_url + 'p-' + str(page)
        if not crawl_list(cat, cur_url):
            break

if __name__ == "__main__":

    for line in open('crawl_list.cnf'):
        cat, start_url = line.strip().split(',')
        work(cat, start_url)

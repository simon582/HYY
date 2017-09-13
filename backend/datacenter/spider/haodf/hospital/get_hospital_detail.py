# coding:utf-8

import scrapy
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    'Host':'www.haodf.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
}

def get_desc(url):

    r = requests.get(url, headers=headers)
    html = r.text
    with open('test.html', 'w') as f:
        print >> f, html
    hxs = scrapy.Selector(text=html)
    desc = ''
    for text in hxs.xpath('//table[@class="czsj"]/tr/td/text()'):
        desc += text.extract().strip()
    return desc
 
def work(province, hospital, url):

    print province, hospital, url
    r = requests.get(url, headers=headers)
    html = r.text
    with open('test.html', 'w') as f:
        print >> f, html
    hxs = scrapy.Selector(text=html)
    title = ''
    try:
        title = hxs.xpath('//div[@class="toptr"]/ul/li[@class="item"]/p/text()')[1].extract().strip()
        title = title[1:-1]
    except:
        pass
    addr = ''
    tel = ''
    for tr in hxs.xpath('//table[@id="hosabout"]/tr'):
        try:
            key = tr.xpath('./td[2]/nobr/text()')[0].extract()
        except:
            continue
        if key.find('地　　址：') != -1:
            try:
                addr = tr.xpath('./td[2]/text()')[0].extract().strip()
            except:
                pass
        if key.find('电　　话：') != -1:
            try:
                tel = tr.xpath('./td[2]/text()')[0].extract().strip()
            except:
                pass
    print title, addr, tel
    desc_url = url.split('.htm')[0] + '/jieshao.htm' 
    desc = get_desc(desc_url)
    print desc
    with open('hospital_detail.csv', 'a') as f:
        line = '|'.join([province, hospital, title, url, addr, tel, desc])
        print >> f, line

for line in open('hospital.txt'):
    res = line.strip().split(',')
    province = res[0]
    hospital = res[1]
    url = res[-1]
    work(province, hospital, url)

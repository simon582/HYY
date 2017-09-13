# coding:utf-8

import scrapy
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):
    headers = {
        'Host':'www.haodf.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
    }
    r = requests.get(url, headers=headers)
    html = r.text
    with open('test.html','w') as f:
        print >> f, html
    return html

def get_offices(province, hospital, url):

    print province, hospital, url
    hxs = scrapy.Selector(text=get_html(url))
    offices = []

    for tr in hxs.xpath('//div[@class="lt"]/table[@id="hosbra"]/tr'):
        res = tr.xpath('./td[@class="font14"]/text()')
        if len(res) == 0:
            continue
        office = res[0].extract()
        for td in tr.xpath('./td/table/tr/td'):
            url = td.xpath('./a/@href')[0].extract()
            sub_office = td.xpath('./a/text()')[0].extract()
            print office + ',' + sub_office + ',' + url
            offices.append((office, sub_office, url))

    return offices

def get_doctor_by_page(baseinfo, page):

    url = baseinfo['office_url'].split('.htm')[0] + '/menzhen_%d.htm' % page
    print baseinfo['office'], url
    hxs = scrapy.Selector(text=get_html(url))

    for tr in hxs.xpath('//table[@id="doc_list_index"]/tr'):
        prod = {}
        prod['name'] = tr.xpath('.//a[@class="name"]/text()')[0].extract()
        print prod['name']
        prod['doctor_url'] = tr.xpath('.//a[@class="name"]/@href')[0].extract()
        print prod['doctor_url']
        prod['title'] = tr.xpath('.//td[@class="tdnew_a"]/li/p/text()')[0].extract().strip()
        print prod['title']
        
        print '-----------------------'


def get_doctor(province, hospital, office_tuple, hospital_url):

    office, sub_office, url = office_tuple
    print province, hospital, office, sub_office
    hxs = scrapy.Selector(text=get_html(url))
    
    baseinfo = {}
    baseinfo['province'] = province
    baseinfo['hospital'] = hospital
    baseinfo['hospital_url'] = hospital_url
    baseinfo['office'] = office
    baseinfo['sub_office'] = sub_office
    baseinfo['office_url'] = url

    max_page = 1
    try:
        text = hxs.xpath('//div[@class="p_bar"]/a[@rel="true"]/text()')[1].extract()
        max_page = int(text.split(u'\xa0')[1].strip())
    except:
        pass
    print 'max page:', max_page

    for page in range(1, max_page + 1):
        get_doctor_by_page(baseinfo, page)
     
if __name__ == "__main__":

    for line in open('hospital.txt'):
        province, hospital, url = line.strip().split(',')
        offices = get_offices(province, hospital, url)
        for office in offices:
            get_doctor(province, hospital, office, url)
            exit(0)

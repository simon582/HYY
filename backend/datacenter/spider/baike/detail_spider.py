# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json
import scrapy

headers = {
    'Cookie':'BDUSS=VN6V2dxTTN2UEo3fld4VzIwVm1oVEN0dUw1emk0Y0lRNldOMDhFeUVFdW9Id3haSVFBQUFBJCQAAAAAAAAAAAEAAAAQgwcARmlyZV9QS0MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKiS5FiokuRYa; __cfduid=d629381a51d6b09f0ec307f71f80789501499067036; BAIDUID=87C0C5107AC4A665EB3B2AC0E2761228:FG=1; PSTM=1499915970; BIDUPSID=8F33C4CAA0B745872C4172B5C6D82833; MCITY=-179%3A; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; PSINO=5; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=23948_1425_21091_24093; pgv_pvi=2766683136; pgv_si=s6770791424; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1502069364,1502160586,1502243166,1502431032; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1502431510',
    'Host':'baike.baidu.com',
    'Referer':'https://baike.baidu.com/wikitag/taglist?tagId=75953',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}

for line in open('treatment.csv', 'r'):
    name, url = line.strip().split(';')
    print name, url
    prod = {}
    prod['name'] = name
    prod['url'] = url
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    html = r.text
    hxs = scrapy.Selector(text=html)
    prod['summary'] = ''
    for text in hxs.xpath('//div[@class="lemma-summary"]/div/text()|//div[@class="lemma-summary"]/text()'):
        prod['summary'] += text.extract().strip()
    print prod['summary']
    bi_list = []
    for dl in hxs.xpath('//div[@class="dl-baseinfo"]/dl'):
        key = dl.xpath('./dt/text()')[0].extract()
        val = dl.xpath('./dd/text()')[0].extract()
        bi_list.append(key.strip() + ':' + val.strip())
    prod['baseinfo'] = '|'.join(bi_list)
    print prod['baseinfo']
    line = ';'.join([prod['name'],prod['url'],prod['baseinfo'],prod['summary']])
    with open('result.csv', 'a') as f:
        print >> f, line

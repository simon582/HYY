# -*- coding:utf-8 -*-

import requests
import pymongo
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''
    网站采用动态session验证，需要依赖selenium获取最新cookie记录后才能访问
'''

def get_html(url):

    headers = {
        'Host':'www.nhfpc.gov.cn',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Referer':'http://www.nhfpc.gov.cn/zhuz/xwzx/xwzx.shtml',
        'Cookie':'FSSBBIl1UgzbN7N80S=XrohQTBRHbW4amgPPBJ3lc9kfonsPI6vOpKioE3cwM1UYyeLiOrBfIbj_JaZydiv; yunsuo_session_verify=fc0366b87fd33e646f6a9e2b7ff4e12b; banggoo.nuva.cookie=0|Wd3WH|Wd3Sf; FSSBBIl1UgzbN7N80T=1Sh5IPl1AVJ_YACP7X7JGh_pSqCZ9zjYtkHPE4Hdiy1AWGK0Oyk6rawUT4PdiFCX8xgRJJGGMHJWmhVzMPCep1oRCY_VcXqBVaNcvus1W_W_ozGMEFx.8N5S_IrSDB7eIbgRKr7Y3GY6W1t4phuQvHg8ZYpc3JSrlKkK.zGlbWaNJE4XJc.5lxCSfjN4ff2rgO1edxbEp9GhFXw1C5kDUiThpfNEMN3GD3FQaUCpBsbTAWetM_msz3m5lMUJdmi9LVIVM1oJZWMHbGtVcDw4c2oby8u9QLIoXe.0Fls7dkpY7Hp5FhT2UUZkI0bFIVVDJf6RVcuAideInlVrNppPNjo7a5cYautIL933qtN6Ge3qAHa',
    }
    retry_times = 0
    while retry_times < 5:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            html = r.text
            with open('test.html','w') as f:
                print >> f, html
            return html
        except Exception as e:
            print e
            retry_times += 1
            print 'retry times:', retry_times
    return ''

def get_list(cat, url):

    hxs = scrapy.Selector(text=get_html(url))
    for li in hxs.xpath('//ul[@class="zxxx_list"]/li'):
        try:
            title = li.xpath('./a/@title')[0].extract()
            print title
        except Exception as e:
            print e
    exit(0)

if __name__ == "__main__":

    urls = [('国务院信息','http://www.nhfpc.gov.cn/zhuz/gwyxx/list.shtml'),
            ('媒体报道','http://www.nhfpc.gov.cn/zhuz/mtbd/list.shtml'),
            ('工作动态','http://www.nhfpc.gov.cn/zhuz/gzdt/list.shtml'),
            ('领导之声','http://www.nhfpc.gov.cn/zhuz/ldzs/list.shtml')]
    for cat, url in urls:
        get_list(cat, url)

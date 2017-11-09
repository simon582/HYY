# coding:utf-8

import scrapy
import requests
import hashlib
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):
    headers = {
        'Host':'www.haodf.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
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

def get_doctor_detail(prod):
    
    #hxs = scrapy.Selector(text=get_html(prod['doctor_url']))
    text = get_html(prod['doctor_url'])
    delim = '<script type="text/javascript">BigPipe.onPageletArrive('
    for part in text.split(delim):
        js_content = part.split(');</script>')[0]
        if js_content.find('bp_doctor_about') != -1:
            js_dict = json.loads(js_content, encoding='utf-8')
            hxs = scrapy.Selector(text=js_dict['content'])
            try:
                prod['profile_pic'] = hxs.xpath('//div[@class="ys_tx"]/table/tr/td/img/@src')[0].extract()
            except:
                prod['profile_pic'] = 'null'
            print 'profile_pic:', prod['profile_pic']

            try:
                prod['be_good_at'] = hxs.xpath('//div[@id="full_DoctorSpecialize"]/text()')[0].extract().strip()
            except:
                prod['be_good_at'] = ''
            print 'be_good_at:', prod['be_good_at']

            try:
                prod['profile'] = ''
                for part in hxs.xpath('//div[@id="full"]/text()'):
                    prod['profile'] += part.extract().strip()
            except:
                prod['profile'] = ''
            #print 'profile:', prod['profile']

            try:
                prod['score'] = hxs.xpath('//p[@class="r-p-l-score"]/text()')[0].extract()
                prod['score'] = float(prod['score'])
            except:
                prod['score'] = 0.0
            print 'score:', prod['score']

            try:
                for text in hxs.xpath('//span[@class="r-p-score"]/text()'):
                    text = text.extract()
                    #import pdb;pdb.set_trace()
                    if text.find('疗效满意度') != -1:
                        prod['treatment_effect_level'] = float(text.split('：')[1].split('%')[0]) / 100.0
                    if text.find('态度满意度') != -1:
                        prod['service_attitute_level'] = float(text.split('：')[1].split('%')[0]) / 100.0
            except:
                prod['treatment_effect_level'] = 0.0
                prod['service_attitute_level'] = 0.0
            print 'treatment_effect_level:', prod['treatment_effect_level']
            print 'service_attitute_level:', prod['service_attitute_level']
            
        if js_content.find('bp_menzhen') != -1:
            js_dict = json.loads(js_content, encoding='utf-8')
            hxs = scrapy.Selector(text=js_dict['content'])
            # TODO 门诊时间

    prod['review'] = ''
    # TODO 前5条评论
 
def write_csv(prod):

    vals = [
        prod['baseinfo']['hid'], 
        prod['baseinfo']['office']+prod['baseinfo']['sub_office'],
        prod['name'],
        prod['profile'],
        prod['good_at'],
        prod['title'],
        prod['title_level'],
        '|||'.join(prod['review']),
        prod['score'],
        prod['treatment_effect_level'],
        prod['service_attitute_level'],
        prod['did'],
            ]

import MySQLdb
dbConn = MySQLdb.connect(host='112.126.81.241', port=3306, user='hemed_hys', passwd='hos_doc@hemEd_2o17', db='hys', charset='utf8')
dbCursor = dbConn.cursor()

def write_sql(prod):

    global dbCursor
    global dbConn
    sqli = "insert into doctors(hid,department,name,profile_pic,profile,be_good_at,job_title,clinical_title,academic_title,review,score,title_level,treatment_effect_level,service_attitute_level,did) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%f','%f','%f','%f','%s')"
    keys = ['hid','department','name','profile_pic','profile','be_good_at','title','clinical_title','academic_title','review','score','title_level','treatment_effect_level','service_attitute_level','did']
    try:
        vals = [prod[key] for key in keys]
        dbCursor.execute(sqli % tuple(vals))
        dbConn.commit()
    except Exception as e:
        print e

def calc_title_level(title):

    res = 0
    if title.find('副主任') != -1:
        res += 4
    elif title.find('主任') != -1:
        res += 5

    if title.find('副教授') != -1:
        res += 4
    elif title.find('教授') != -1:
        res += 5

    if title.find('主治') != -1:
        res +=  4

    if title.find('住院') != -1:
        res += 3
    return res

def get_doctor_by_page(baseinfo, page):

    url = baseinfo['office_url'].split('.htm')[0] + '/menzhen_%d.htm' % page
    print baseinfo['office'], url
    hxs = scrapy.Selector(text=get_html(url))

    for tr in hxs.xpath('//table[@id="doc_list_index"]/tr'):
        prod = {}
        for key,val in baseinfo.items():
            prod[key] = val
        prod['department'] = prod['office'] + ' ' + prod['sub_office']
        prod['name'] = tr.xpath('.//a[@class="name"]/text()')[0].extract()
        print prod['name']
        prod['doctor_url'] = tr.xpath('.//a[@class="name"]/@href')[0].extract()
        print prod['doctor_url']
        prod['did'] = hashlib.md5(prod['doctor_url']).hexdigest().upper()
        prod['title'] = tr.xpath('.//td[@class="tdnew_a"]/li/p/text()')[0].extract().strip()
        print prod['title']
        prod['clinical_title'] = prod['academic_title'] = ''
        for sub_title in prod['title'].split(' '):
            if sub_title.find('医师') != -1:
                prod['clinical_title'] = sub_title
            elif sub_title.find('教授') != -1:
                prod['academic_title'] = sub_title
        prod['title_level'] = calc_title_level(prod['title'])
        print 'title_level:', prod['title_level']
        get_doctor_detail(prod)
        #write_csv(prod)
        write_sql(prod)
        print '-----------------------'
        #exit(0)

def get_doctor(province, hospital, office_tuple, hospital_url):

    office, sub_office, url = office_tuple
    print province, hospital, office, sub_office
    hxs = scrapy.Selector(text=get_html(url))
    
    baseinfo = {}
    baseinfo['province'] = province
    baseinfo['hospital'] = hospital
    baseinfo['hospital_url'] = hospital_url
    baseinfo['hid'] = hashlib.md5(hospital_url).hexdigest().upper()
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

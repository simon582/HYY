# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import json

url = 'https://baike.baidu.com/wikitag/api/getlemmas'

headers = {
    'Cookie':'BDUSS=VN6V2dxTTN2UEo3fld4VzIwVm1oVEN0dUw1emk0Y0lRNldOMDhFeUVFdW9Id3haSVFBQUFBJCQAAAAAAAAAAAEAAAAQgwcARmlyZV9QS0MAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKiS5FiokuRYa; __cfduid=d629381a51d6b09f0ec307f71f80789501499067036; BAIDUID=87C0C5107AC4A665EB3B2AC0E2761228:FG=1; PSTM=1499915970; BIDUPSID=8F33C4CAA0B745872C4172B5C6D82833; BDSFRCVID=XR-sJeCmHGXhn_JZ7c-VhwR_E2K2qHTTHlxjhrLq1w-ruBFSZxyvEG0Ptf8g0Ku-oxF5ogKK0gOTH65P; H_BDCLCKID_SF=JbPO_II5JIvbfP0kMRosbDCShG4ebj3eWDTm_DoabhRMhfoL5bb-MPkWDao72x_85nbI-pPKKlT5VD_9Mpbsqf6LKPOh-x0H3mkjbpcDfn02OPKzMMrdM44syPRiKMRnWgKqbIF5tD-MMItlenC_KJF8KmT22-usWeQmQhcH0KLKDfcjbxRKWR_t5xO3--oCQ2_JLIj9Lfb1MRjvjtOHyjDRMpCqB6L8KHn3Wh5TtUJtSDnTDMRhqfPhDfcyKMniWKv9-pnYJft0hD0wD6_bj5PS-qKX5tcJK6TJW5rJabC3oM_zKU6qLPunQn732qRZyJv2sxQSbMorsDooDRQ13h0nhh7Banjr-R6fs4oa0qQ6o4nw5xonDh83bG7MJUntHCOOKD5O5hvvhb3O3MA-jqOh-p52f60DfnrP; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1501834612,1501834642,1502069364,1502160586; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1502160586; MCITY=-179%3A; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[w2jhEs_Zudc]=I67x6TjHwwYf0; PSINO=5; H_PS_PSSID=',
    'Host':'baike.baidu.com',
    'Referer':'https://baike.baidu.com/wikitag/taglist?tagId=75953',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
}

payload = {
    'limit':'24',
    'timeout':'3000',
    'filterTags': [],
    'tagId': '75955',
    'fromLemma': 'false',
    'contentLength':'40',
    'page':'1',
}

for page in range(1, 101):
    print 'page:' + str(page)
    payload['page'] = str(page)
    r = requests.post(url, headers=headers, data=payload)
    cd = json.loads(r.text)
    for lemma in cd['lemmaList']:
        line = ';'.join([lemma['lemmaTitle'], lemma['lemmaUrl']])
        print line
        with open('result.csv', 'a') as f:
            print >> f, line
    

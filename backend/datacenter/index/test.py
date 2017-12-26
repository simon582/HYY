# coding:utf-8
import pymongo
import hashlib

conn = pymongo.MongoClient()
hyy_db = conn['hyy']

prod = {
    'source_icon':"http://www.ythaian.com/UpFile/Image/2015-12/Ew_20151221085022502.png",
    'detail_url':'http://www.sda.gov.cn/WS01/CL0053/103756.html',
    'title':'《医疗器械注册管理办法》（国家食品药品监督管理总局令第4号）',
    'author':'CFDA',
    'source_desc':'国家食品药品监督管理总局',
    'datetime':'2014-07-30',
    'source':'CFDA',
    'short_text':'',
    'text':open('article.txt','r').read(),
}

prod['doc_id'] = hashlib.md5(prod['detail_url']).hexdigest()

print prod

hyy_db.temp.save(prod)

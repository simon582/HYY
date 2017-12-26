import pymongo

mongo_conn = pymongo.MongoClient()
news_db = mongo_conn['hyy']

id_set = set()

for prod in news_db.temp.find():
    if prod['doc_id'] in id_set:
        news_db.temp.remove({'_id':prod['_id']})
        print prod
    else:
        id_set.add(prod['doc_id'])

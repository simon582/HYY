# coding:utf-8

import MySQLdb
import hashlib

conn = MySQLdb.connect(host='112.126.81.241', port=3306, user='hemed_hys', passwd='hos_doc@hemEd_2o17', db='hys', charset='utf8')
cur = conn.cursor()

sqli = "insert into hospitals(city,name,level,website,address,phone,introduction,level_score,hid) values('%s','%s','%s','%s','%s','%s','%s',%f,'%s')"

def analyze_level(level):

    score_mapping = {'甲等':10,
                     '乙等':7,
                     '丙等':4,
                     '三级':3,
                     '二级':2,
                     '一级':1,
                     '专科':12}
    score = 0
    for l, s in score_mapping.items():
        if level.find(l) != -1:
            score += s
    return float(score)

cnt = 1
for line in open('hospital_detail.csv', 'r'):
    print cnt
    cnt += 1
    res = line.strip().split('|')
    if len(res) != 7:
        continue
    level = res[2]
    level_score = analyze_level(level)
    hid = hashlib.md5(res[3]).hexdigest().upper()
    res += [level_score, hid]
    res = tuple(res)
    #print sqli % res
    try:
        cur.execute(sqli % res)
        conn.commit()
    except Exception as e:
        print e

cur.close()
conn.close()

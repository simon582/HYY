# -*- coding:utf-8 -*-
# Copyright: Zhejiang Tachao Technology Inc.
# Author: Shao Xinqi
# Date: 2016-07-20
# Description: simple decision engine

import sys
import datetime
import time
import json
import socket
import traceback
sys.path.append('./gen-py/')
sys.path.append('./base/')
reload(sys)
sys.setdefaultencoding('utf-8')

from utils import WriteLog
from data import HyySearchService
from data import ttypes
from data import constants

class HYYSearcher(object):

    def __init__(self):

        pass

    def _get_query(self, keyword):

        doc = ttypes.HyyDoc()
        doc.doc_id = '123'
        doc.title = '肚子疼怎么回事'
        doc.author = '妖刀5VY'
        doc.datetime = '2013-12-04 09:19'
        doc.source = '百度'
        doc.source_icon = 'http://iknowpc.bdimg.com/static/question/widget/sample/top-nav-bar/img/zhidao-logo_b9ec675.png'
        doc.source_desc = '百度知道'
        doc.text = '肚子疼是指从肋骨以下到腹股沟以上部分的疼痛。 肚子疼可能是胃肠消化器官肝、胆、胰腺疾病，妇科疾病或泌尿生殖器官的毛病。轻微的肚子疼多半是消化不良等胃肠道小毛病所引起的。持续性严重的肚子疼且无腹泻可能是十分严重的疾病。肚子疼又有呕吐，吐了之后肚子疼并未减轻，腹部软软地膨胀，或者病人昏昏欲睡，神志不清，很可能是由于下列各种十分严重的疾病。
①胃肠方面的疾病：胃溃疡、癌瘤、阑尾炎、肠梗阻、肠穿孔、肠套叠、急性肠溃疡、局部肠炎等。
②泌尿、生殖系统的疾病：肾结石或癌瘤引起的肾绞痛、肾盂肾炎、前列腺炎、膀胱炎。
③多种妇科疾病：宫外孕破裂、卵巢囊肿蒂扭转。
④肝胆疾病：胆囊炎、肝炎、胆石症。
⑤不同原因引起的腹膜炎。 
⑥血栓性的疾病。 
为了病人的安全，要立即去看医生或送医院急诊。 肚子疼时千万不要服阿司匹林或其他麻醉性止痛药止痛。阿司匹林对肚子疼有害无益，麻醉性止痛药可掩盖症状，干扰诊断。 1、症状：肚子疼的部分在腰(肚脐)以下，小便时有灼痛感，小便次数增多。 可能：是膀肮炎。 处理：需用抗生素治疗。但医生也会进一步用肾盂摄影术，查究发炎原因后对症治疗。 
2、症状：肚子疼持续了1小时以上。 可能：肚子疼的原因很多，要靠专家诊断。不论是否伴有其他症状，都要立即去看医生。 处理：在看医生之前不要吃东西。如医生看不出是什么毛病，病人就要住医院，检查出是什么毛病之后才能治疗。持续性的肚子疼，如没有腹泻，很可能是十分严重的疾病。 
3、症状：肚子疼持续了1小时以上，同时呕吐，吐后肚子疼并未见减轻，腹部膨胀。严重的病人可能昏睡或神志不清。 可能：是十分严重的症状。 处理：在见到医生之前，不要吃东西。立即送医院。如果医生不能诊断出是什么病症，可能要用开腹手术，就是打开病人的腹腔直接查看。查出是什么病症之后才能对症治疗。 
4、症状：肚子疼了1小时以上，腹泻。 可能：肚子疼、腹泻多半是吃了不洁净的食物(食物中毒)，引起胃肠道发炎。 处理：在症状未消失时需注意以下几点。 ①不要吃固体食物，不能饮牛奶。 ②至少每天要多饮1升白开水(不能加糖)。 ③如泻的次数太多，要饮淡盐水(1升水中加半茶匙食盐)，补充因腹泻失去的水分。④如发现大便内有红色或无色的鼻涕状粘液，就要去看医生。 
5、症状：肚子疼由腰旁开始，后来向下斜移至腹股沟。 可能：输尿管的毛病，肾脏发炎或结石。 处理：去看医生，要验尿。 ①发炎，用抗生素治疗。病人要多饮水 ②结石，医生可能要为病人做肾盂摄影术，检查结石。视结石的性质，病人要多饮水。可试试服药溶化。有服用别嘌呤醇(是治痛风药)加服钾盐，得到很好效果的，但有待进一步证实。亦有用超声波击碎结石，得到满意的效果。在迫不得已的时候只有动手术治疗。防止结石再生，病人要吃低钙、低嘌呤食物。 
6、症状：女性肚子疼，部位在中下部，突然出现剧烈阵发性疼痛。 可能：可能由于卵巢囊肿蒂扭转。 处理：立即去看医生。医生要做超声波检查，必要时须手术治疗。 
7、症状：育龄妇女突然下肚子疼，有停经史，伴不规则阴道出血、晕厥或休克。 可能：子宫外孕破裂。 处理：立即送医院。如妇科检查后穹窿穿刺，可抽出血性液体。医生要做紧急手术。 
8、症状：在肋骨以下腰部的右边痛。 可能：胆结石。大约在食后两小时痛，恶心，呕吐。 处理：去看医生，医生可能用超声波扫描来诊断。如病人痛得太厉害，医生可能要为病人注射止痛针剂。病人要注意以下几点。 ①少吃油脂食物。 ②吃点肌肉松弛药。 ③必要时吃点止痛药，如对乙酰氨基酚。 ④吃药帮助化解胆石。⑤如上述治疗无效，需手术切除胆囊。
 9、症状：肚子疼的部位在腹部的上部，胸部下面。 可能：消化不良。 处理：去药房买点助消化药吃。每餐不要吃得太多。如经常发作而且愈来愈厉害，去看医生。 
 10、症状：肚子疼了3小时以上，先是在肚脐四周痛，呕吐或者不呕吐。当摸到从胯骨到肚脐的直线中点(阑尾位处)，很痛。 可能：阑尾炎。急性阑尾炎还可能发热。 处理：去看医生。医生要用抗生素治疗，必要时要手术治疗。'
    return [doc, doc, doc, doc]
    
    def _get_result(self, query):
       
        if query.find('query=') != -1:
            keyword = query.split('query')[1]
            return _get_query(keyword) 

    def GetSearchResult(self, hyy_search_request):

        try:
            hyy_search_response = ttypes.HyySearchResponse()
            hyy_search_response.qid = hyy_search_request.qid
            hyy_search_response.doc_list = self._get_result(hyy_search_request.data)
            WriteLog('NOTICE', 'qid:%s, data:%s' % (hyy_search_request.qid, hyy_search_request.data))
            return hyy_search_response   
        except:
            traceback.print_exc()
            return None

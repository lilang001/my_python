# -*- coding: utf-8 -*-
__author__ = 'admin'
import requests
import json
import random
from pyquery import PyQuery as pq
# class Rating(object):
#     def __init__(self,url,user,password):
#         url= self.url

def login(url, user, password):
    try:
        c = requests.get(url)
        par = '/Login/Login?loginName=' + user + '&password=' + password
        d = requests.post(url + par, cookies=c.cookies)
        return d.cookies
    except Exception as e:
        print ('Loginerror,please try later!')

def score_item(url,user,password,ratingSysNo):
    cookies = login(url,user,password)
    rating_url = url+'/Rating/Score?ratingSysNo='+ratingSysNo
    rating_item_list = []
    rating_info = requests.get(rating_url,cookies=cookies).content
    txt= pq(rating_info)('body')('script')[2].text.split('=')[1]
    item = txt[0:txt.rfind(';',1)]
    item = item[item.find('{',0):]
    item_dict= json.loads(item)['RatingCategoryList']
    for i in range(len(item_dict)):
        level2 = item_dict[i]['RatingCategoryList']
        for j in range(len(level2)):
            level3 = level2[j]['RatingCategoryList']
            for h in range(len(level3)):
                rating_item_list.append(level3[h]['RatingItemSysNo'])
    return  rating_item_list,cookies


def score(url,user,password,ratingSysNo):
    score_item_result = score_item(url,user,password,ratingSysNo)
    item_list = score_item_result[0]
    cookies = score_item_result[1]
    score_url = url+'/Rating/Save'
    for i in  range(len(item_list)):
        rating_url = url+'/Rating/Score?ratingSysNo='+ratingSysNo+'&ratingItemSysNo='+str(item_list[i])
        rating_info = requests.get(rating_url,cookies=cookies).content
        print (i,item_list[i],)
        try:
            txt= pq(rating_info)('body')('script')[2].text.split('function()')[0]
            item = txt[0:txt.rfind(';',1)]
            item = item[item.find('{',0):]
            RatingSelfEvaluateIngList = json.loads(item)['RatingSelfEvaluateIngList']
        except:
            print (rating_url,u'打分项设置错误')


        RatingMutualTableItemList = []
        for j in range(len(RatingSelfEvaluateIngList)):
            if RatingSelfEvaluateIngList[0]['MyRating']==None:
                item_type=0
                item_value='0'
            else:
                rang_i = random.randint(0,len(RatingSelfEvaluateIngList[0]['MyRating'])-1)
                item_type = RatingSelfEvaluateIngList[0]['MyRating'][rang_i]['EnumValue']
                try:
                    item_value = RatingSelfEvaluateIngList[0]['MyRating'][rang_i]['ScoreValueList'][random.randint(0,len(RatingSelfEvaluateIngList[0]['MyRating'][rang_i]['ScoreValueList'])-1)]['Text']
                except:
                    print ('test')
            self_item = RatingSelfEvaluateIngList[j]
            item_RatingItemSysNo = self_item['RatingItemSysNo']
            item_OrganizationSysNo = self_item['OrganizationSysNo']
            dict_RatingSelfEvaluateIngList= {}
            dict_RatingSelfEvaluateIngList['RatingItemSysNo']=item_RatingItemSysNo
            dict_RatingSelfEvaluateIngList['OrganizationSysNo']=item_OrganizationSysNo
            dict_RatingSelfEvaluateIngList['RatingTypeValue']=item_type
            dict_RatingSelfEvaluateIngList['RatingScore']=item_value
            RatingMutualTableItemList.append(dict_RatingSelfEvaluateIngList)
        data = {
            'OrganizationSysNo':'null',
            'RatingMutualTableItemList':RatingMutualTableItemList,
            'RatingSysNo':ratingSysNo,
            'sumbit':0
        }

        requests.post(score_url,cookies=cookies,json=data)
        if sum==1:
            print (data)







    data2 = {
            'OrganizationSysNo':'null',
            'RatingMutualTableItemList':[{'RatingItemSysNo': 23430, 'OrganizationSysNo': 30018, 'RatingTypeValue': 3, 'RatingScore': 1.7}],
            'RatingSysNo':20090,
            'sumbit':0
        }
    #
    # print ('')

if __name__ =='__main__':
    score('http://zjpf.yzw.cn.qa/','test3','111111','20090')



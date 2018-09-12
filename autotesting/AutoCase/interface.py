# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

from pyquery import PyQuery as pq
import sqls
import requests
import json
import random
from mysql import  select
from public import equal, Driver, content_deal, time_deal

class InterFace():
    def __init__(self):
        self.url = 'http://192.168.1.16:8081/'

    # 精彩课程，排序：最多播放；不加载广告；默认第一页，每页15条
    def get_excellent_course(self):
        url = self.url + 'v3/getExcellentCourse/?orderBy=2&loadAd=0'
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        for i in txt['data']['list']:
            click_count = i['student_count']  # 课程点击次数
            lesson_count = i['lesson_count']  # 课程视频个数
            course_id = i['course_id']  # 课程id
            name = i['course_name']   # 课程名称
            img = i['img_url'].split('uploads/')[-1]   # 课程图片链接
            teacher = i['teacher']    # 教师昵称
            updating = i['updating']   # 是否更新中，0为不更新
            actual.append((click_count, lesson_count, course_id, name, img, teacher, updating))
        expect = select(sqls.get_excellent_course)
        equal('get_excellent_course', expect, actual)

    # 获取精课程的广告数据
    def get_excellent_course_ad(self):
        url = self.url + 'v3/getExcellentCourse/?orderBy=2&loadAd=1'
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        for i in txt['data']['ad']:
            img = i['url'].split('uploads/')[-1]  # 广告图片
            callback_url = i['out_url']  # 广告回调url
            target_id = i['target_id']  # 目标id，不晓得有毛用
            ad_type = i['ad_type']   # 广告类型
            title = i['name']   # 广告标题
            actual.append((img, callback_url, target_id, ad_type, title))
        expect = select(sqls.get_excellent_course_ad)
        equal('get_excellent_course_ad', expect, actual)

    # 获取直通班课程
    def get_career_course(self):
        url = self.url+'v3/getCareerCourse/?count=0'
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        for i in txt['data']['list']:
            course_count = i['course_count']  # 课程数量
            student_count = i['student_count']  # 学生数量
            name = i['name']  # 直通班课程名
            class_count = i['class_count']  # 开班数量
            career_id = i['career_id']  # 课程id
            img_url = i['img_url'].split('uploads/')[-1]  # 课程图片
            actual.append((course_count, student_count, name, class_count, career_id, img_url))
        expect = select(sqls.get_career_course)
        equal('get_career_course', expect, actual)

    # 获取直通班课程详情：阶段、对应普通课程
    def get_career_detail(self, career_id):
        url = self.url+'v3/getCareerDetail/?careerId='+career_id+'&UUID=a489516c4e73436bbbeb1a695940fdcf&userId=108'
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        course_desc = txt['data']['desc']  # 职业课程介绍
        index_html = txt['data']['index_html']  # 职业课程落地页地址
        for i in txt['data']['stage']:
            stage_desc = i['stage_desc']  # 阶段描述
            stage_id = i['stage_id']  # 阶段id
            stage_name = i['stage_name']  # 阶段名称
            for j in i['list']:
                course_id = j['course_id']  # 课程id
                img_url = j['img_url'].split('uploads/')[-1]  # 课程图片
                name = j['name']  # 课程名称
                updating = j['updating']  # 是否更新中
                actual.append((course_desc, index_html, stage_desc, stage_id,
                              stage_name, course_id, img_url, name, updating))
        expect = select(sqls.get_career_detail.replace('my_id', career_id))
        equal('get_career_detail', expect, actual)

    # 获取直通班课程价格等,目前获取3.0的课程大bug啊
    def get_career_price(self, career_id):
        url = self.url+'v3/getCareerPrice/?careerId='+career_id+'&UUID=a489516c4e73436bbbeb1a695940fdcf&userId=108'
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        first_pay = txt['data']['pay']['first_pay']  # 首付价格
        price = txt['data']['pay']['price']   # 全款价格
        for i in txt['data']['class_list']:
            class_id = i['class_id']  # 班级ID
            curr_student = i['curr_student']  # 当前报名人数
            teacher = i['teacher']  # 教师昵称，麻痹取不到接口要挂
            class_no = i['class_no']  # 班级coding
            max_student = i['max_student']  # 报名上限人数
            actual.append((first_pay, price, class_id, curr_student, teacher, class_no, max_student, ))
        expect = select(sqls.get_career_price.replace('my_id', career_id))
        equal('get_career_price', expect, actual)

    # 提交咨询信息
    def submit_consult_info(self):
        name = '李朗'+str(random.randint(0, 100))  # 随机姓名
        phone = 18000000000+random.randint(0, 1000000000)  # 随机手机号
        url = self.url+'v3/submitConsultInfo/?realName='+name+'&phoneNum='+str(phone)
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        message = txt['message']  # 返回信息
        actual.append((message, name, phone))
        expect = select(sqls.submit_consult_info)
        equal('submit_consult_info', expect, actual)

    # 获取精彩推荐课程
    def get_excellent_recom(self):
        url = self.url+'v3/getExcellentRecom/?UUID=&userId='
        res = requests.get(url)
        txt = json.loads(res.text)
        actual = list()
        for i in txt['data']['list']:
            course_id = i['course_id']  # 推荐课程id
            img_url = i['img_url'].split('uploads/')[-1]  # 课程图片
            name = i['name']  # 课程名称
            actual.append((course_id, img_url, name))
        expect = select(sqls.get_excellent_recom)
        equal('get_excellent_recom', expect, actual)
if __name__ == '__main__':
    InterFace().get_excellent_recom()


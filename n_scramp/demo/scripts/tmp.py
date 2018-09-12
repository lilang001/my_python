# -*- coding: utf-8 -*-

"""
@author : Jackie
@date : 2015/11/11
@note :
"""
import json
import os
import django
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
django.setup()

from mz_lps2.models import AsyncMethod


def get_lesson(lesson_id):
    from mz_course.models import Lesson
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        return lesson.video_url
    except:
        return ''


def get_course(course_id):
    from mz_course.models import Course
    try:
        course = Course.objects.get(id=course_id)
        return course.name
    except:
        return ''


def save(rows):
    writer = csv.writer(open('d:/data_step1.csv', 'wb'))
    writer.writerow(['course_id', 'lesson_id', 'student_id', 'submit_datetime', 'date'])
    for row in rows:
        writer.writerow(row)


def step1():
    rows = list()
    for obj in AsyncMethod.objects.filter(submit_datetime__gt="2015-11-01").order_by('submit_datetime'):
        methods = json.loads(obj.methods)
        lesson_id = str(methods.get('lesson_id'))
        course_id = str(methods.get('course'))
        examine = str(methods.get('examine'))
        student_id = str(methods.get('student'))
        submit_date = obj.submit_datetime.date().isoformat()
        if examine == "-1" and lesson_id != 0:
            row = (course_id, lesson_id, student_id, \
                   str(obj.submit_datetime), submit_date)
            rows.append(row)
    return rows


def step2(rows):
    t1 = dict()  # 按时间
    t2 = dict()  # 按视频
    t3 = dict()  # 按课程
    for course, lesson, student, dt, d in rows:
        t1.setdefault(d, list())
        t1[d].append((course, lesson, student))
        t2.setdefault(lesson, list())
        t2[lesson].append(d)
        t3.setdefault(course, 0)
        t3[course] += 1
        # for d in sorted(t1.keys()):
        #     rs = t1[d]  # 课程,章节,学生
        #     print d, u"视频浏览总数:%s" % len(rs)
        # print u"11.01~11.11 每个视频播放次数"
        # for _x, _y in sorted(((x, len(y)) for x, y in t2.iteritems()), key=lambda m: m[1], reverse=True):
        #     print u'视频id:', _x, u'次数:', _y, get_lesson(_x)
    for x, y in sorted(t3.iteritems(), key=lambda m: m[1], reverse=True):
        print u"课程id:", x, u"次数:", y, get_course(x)


if __name__ == "__main__":
    rows = step1()
    # save(rows)
    step2(rows)

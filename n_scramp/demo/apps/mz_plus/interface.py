# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from mz_plus.keywords import extrac_keyword

__author__ = 'Jackie'


def get_fit_video(content):
    """
    根据关键字,获取最适合的视频资源
    :param content:文本内容
    :return:视频资源地址,超链接地址(麦子学院视频播放地址)
    """
    keyword = extrac_keyword(content)
    from mz_course.models import Course, Lesson
    # 根据关键字找到热门教程
    courses = Course.objects.filter(
        Q(name__icontains=keyword) | Q(search_keywords__name__icontains=keyword), is_click=True, is_active=True)
    courses = courses.order_by('-favorite_count')
    if courses:
        course = courses[0]
        stage_set = course.stages_m.all()  # 取出所有章节
        try:
            careercourse = stage_set[0].career_course.short_name.lower()
        except:
            careercourse = 'others'
        lesson_list = Lesson.objects.filter(course_id=course.id).order_by("index")
        callback_url = "http://www.maiziedu.com/course/%s/%d-%d" % (
            careercourse, course.id, lesson_list[0].id) if lesson_list else ""
        video_url = lesson_list[0].video_url
        return True, dict(course_url=callback_url, video_url=video_url, course_name=course.name)
    else:
        return False, dict(msg=u'未匹配到合适的课程')


if __name__ == "__main__":
    print extrac_keyword("jajavavapython,java,co,pythondcco")

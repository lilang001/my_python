# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class Keywords(models.Model):
    name = models.CharField(u'关键词', max_length=50)

    class Meta:
        db_table = "mz_common_keywords"
        verbose_name = u'关键词'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 职业课程 models
class CareerCourse(models.Model):
    name = models.CharField("职业课程名称", max_length=50)
    short_name = models.CharField("职业课程英文名称简写", max_length=10, unique=True)
    image = models.ImageField("课程图标(160*160)", upload_to="course/%Y/%m")
    app_image = models.ImageField("课程小图标(24*24)", upload_to="course/%Y/%m", null=True, blank=True)
    app_career_image = models.ImageField("app图标", upload_to="course/%Y/%m", null=True, blank=True)
    description = models.TextField("文字介绍")
    student_count = models.IntegerField("学习人数", default=0)
    market_page_url = models.URLField("营销页面地址", blank=True, null=True)
    course_color = models.CharField("课程配色", max_length=50)
    discount = models.DecimalField("折扣", default=1, max_digits=3, decimal_places=2)
    click_count = models.IntegerField("点击次数", default=0)
    index = models.IntegerField("职业课程顺序(从小到大)", default=999)
    search_keywords = models.ManyToManyField(Keywords, null=True, blank=True, verbose_name="搜索关键词")
    seo_title = models.CharField("SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField("SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)
    # add by Steven YU
    course_scope = models.SmallIntegerField("课程类型", null=True, blank=True, choices=((0, "高校专区"), (1, "企业专区"),))
    product_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"产品ID")
    balance_product_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"产品尾款ID")

    status = models.IntegerField(default=0, choices=((0, "一般课程"), (1, "即将开班"), (2, "热门课程")), verbose_name="课程状态")
    guide_line_page = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"课程大纲页")
    qq = models.CharField("QQ群号", max_length=20, null=True, blank=True)
    qq_key = models.CharField("QQ群key", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "职业课程"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.name


# 阶段 models
class Stage(models.Model):
    name = models.CharField("阶段名称", max_length=50)
    description = models.TextField("阶段描述")
    price = models.IntegerField("阶段价格")
    index = models.IntegerField("阶段顺序(从小到大)", default=999)
    is_try = models.BooleanField(default=False, verbose_name=u"是否是试学阶段")
    career_course = models.ForeignKey(CareerCourse, verbose_name="职业课程")


    class Meta:
        verbose_name = "课程阶段"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


# 课程 models
class Course(models.Model):
    name = models.CharField("课程名称", max_length=50)
    image = models.ImageField("课程封面", upload_to="course/%Y/%m")
    description = models.TextField("课程描述")
    is_active = models.BooleanField("有效性", default=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)
    need_days = models.IntegerField("无基础学生完成天数", default=7)
    need_days_base = models.IntegerField("有基础学生完成天数", default=5)
    student_count = models.IntegerField("学习人数", default=0)
    favorite_count = models.IntegerField("收藏次数", default=0)
    click_count = models.IntegerField("点击次数", default=0)
    is_novice = models.BooleanField("是否是新手课程", default=False)
    is_click = models.BooleanField("是否点击能进入课程", default=False)
    index = models.IntegerField("课程顺序(从小到大)", default=999)
    stages_m = models.ManyToManyField(Stage, related_name="stages_m", blank=True, null=True, verbose_name="多阶段",
                                      through="Course_Stages_m")

    # stages = models.ForeignKey(Stage, blank=True, null=True, verbose_name="阶段")

    search_keywords = models.ManyToManyField(Keywords, null=True, blank=True, verbose_name="小课程搜索关键词")
    # Add by Steven YU
    is_homeshow = models.BooleanField(u"是否在首页显示", default=False)
    # is_required = models.BooleanField(u"是否必修", default=True) # add fo lps2
    course_status = models.SmallIntegerField(u"课程状态", choices=((0, "更新中"), (1, "已完结"),), default=0)
    score_ava = models.FloatField("课程平均评分", default=0.0)
    need_pay = models.BooleanField(u"是否需要付费才能观看", default=False)

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    # def getStages(self, stage_id):
    #     stage=self.stages
    #     if stage_id>0:
    #         stage=Stage.objects.get(pk=stage_id)
    #     return stage

    def __unicode__(self):
        return self.name


# 阶段和课程产生的关联对象
class Course_Stages_m(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    stage = models.ForeignKey(Stage, verbose_name=u"阶段")
    is_required = models.BooleanField(u"是否必修", default=True)

    class Meta:
        verbose_name = u"阶段课程"
        verbose_name_plural = verbose_name
        unique_together = (("course", "stage"),)



# 章节 models
class Lesson(models.Model):
    name = models.CharField("章节名称", max_length=50)
    video_url = models.CharField("视频资源URL", max_length=1000)
    video_length = models.IntegerField("视频长度（秒）")
    play_count = models.IntegerField("播放次数", default=0)
    share_count = models.IntegerField("分享次数", default=0)
    index = models.IntegerField("章节顺序(从小到大)", default=999)
    is_popup = models.BooleanField("是否弹出提示框（支付、登录）", default=False)
    course = models.ForeignKey(Course, verbose_name="课程")
    seo_title = models.CharField("SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField("SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)
    # add by yuxin
    have_homework = models.BooleanField("是否有作业", null=False, blank=False, default=True)
    code_exercise_type = models.SmallIntegerField("在线编码类型", choices=((0, "无在线编码"), (1, "python"), (2, "php"),),
                                                  default=0)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name


# 章节资源 models
class LessonResource(models.Model):
    name = models.CharField("章节资源名称", max_length=50)
    download_url = models.FileField("下载地址", upload_to="lesson/%Y/%m")
    download_count = models.IntegerField("下载次数", default=0)
    lesson = models.ForeignKey(Lesson, verbose_name="章节")

    class Meta:
        verbose_name = "章节资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# 课程资源 models
class CourseResource(models.Model):
    name = models.CharField("课程资源名称", max_length=50)
    download_url = models.FileField("下载地址", upload_to="course/%Y/%m")
    download_count = models.IntegerField("下载次数", default=0)
    course = models.ForeignKey(Course, verbose_name="课程")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CareerCatagory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"课程方向")

    class Meta:
        verbose_name = u"课程方向"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)


class CourseCatagory(models.Model):
    career_catagory = models.ForeignKey(CareerCatagory, verbose_name=u"课程方向")
    name = models.CharField(u"课程分类", max_length=50)
    is_hot_tag = models.BooleanField(default=False, verbose_name=u"是否热门标签")

    class Meta:
        verbose_name = u"课程分类"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)

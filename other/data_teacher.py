# coding:utf8
__author__ = 'Administrator'
import MySQLdb
import datetime
import xlwt
import time
import smtplib
import calendar
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
import os.path
import mimetypes


def friday():
    oneday = datetime.timedelta(days=1)
    lastFriday = datetime.datetime.today()-oneday
    while lastFriday.weekday() != calendar.FRIDAY:
        lastFriday -= oneday
    return lastFriday

# 生成报表数据
def excel_create():

    con0 = MySQLdb.Connect(host='192.168.1.142', user='root', passwd='1234', port=3306, charset='utf8')
    cur = con0.cursor()
    begindate = friday().date()
    enddate = datetime.datetime.today()
    # 运营部需要的数据
    sql_ask = """
SELECT F.nick_name ,COUNT(1),F.id AS count FROM  (
	SELECT id, user FROM fps_lilang.mz_forum_discuss WHERE type IN ('0','3') AND date_publish BETWEEN  '{begindate}' AND '{enddate}'
		UNION ALL
	SELECT A.* FROM (SELECT id,user FROM  fps_lilang.mz_forum_entity WHERE date_publish BETWEEN '{begindate}' AND '{enddate}') AS A
		INNER JOIN (SELECT entity_ptr_id  FROM fps_lilang.mz_forum_courseask UNION ALL SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask ) AS B
	ON A.id=B.entity_ptr_id  ) AS E
INNER JOIN
	(SELECT C.id ,C.nick_name FROM (SELECT * FROM lps_lilang.mz_user_userprofile_groups WHERE group_id=2) AS D
	LEFT JOIN lps_lilang.mz_user_userprofile AS C  ON C.id=D.userprofile_id) AS F
	ON E.user=F.id   GROUP BY F.id ORDER BY COUNT(1) DESC
    """

    sql_ask_long = """
SELECT Z.user,US.nick_name,Z.id,Z.type,Z.soure,Z.title,Z.Tags,Y.coding FROM (
SELECT  F.reply_count, F.id, F.date_publish,F.user ,F.type ,F.soure , F.title ,F.Tags  FROM (
SELECT *, (UNIX_TIMESTAMP(B.min) - UNIX_TIMESTAMP(A.date_publish))/3600 dif_hour FROM  (SELECT MIN(date_publish) AS min, relate_id  from fps_lilang.mz_forum_discuss WHERE type IN('3','0') AND date_publish BETWEEN   '{begindate}' AND '{enddate}' GROUP BY  relate_id ) AS B
 LEFT JOIN ( SELECT Z.* FROM (
SELECT fps_lilang.mz_forum_entity.reply_count,fps_lilang.mz_forum_entity.id , fps_lilang.mz_forum_entity.date_publish,fps_lilang.mz_forum_entity.user, '开放问答' AS type , '空' AS soure , fps_lilang.mz_forum_entity.title ,GROUP_CONCAT(fps_lilang.mz_common_tags.`name`) AS Tags FROM  fps_lilang.mz_forum_ask
	LEFT JOIN fps_lilang.mz_forum_entitytag ON fps_lilang.mz_forum_ask.entity_ptr_id=fps_lilang.mz_forum_entitytag.entity_id
	LEFT JOIN fps_lilang.mz_common_tags ON fps_lilang.mz_forum_entitytag.tag_id=fps_lilang.mz_common_tags.id
	LEFT JOIN fps_lilang.mz_forum_entity ON fps_lilang.mz_forum_ask.entity_ptr_id=fps_lilang.mz_forum_entity.id
GROUP BY fps_lilang.mz_forum_ask.entity_ptr_id
UNION ALL
SELECT fps_lilang.mz_forum_entity.reply_count,fps_lilang.mz_forum_entity.id , fps_lilang.mz_forum_entity.date_publish,fps_lilang.mz_forum_entity.user, '课程问答' AS type , lps_lilang.mz_course_lesson.`name` AS soure ,  fps_lilang.mz_forum_entity.title ,lps_lilang.mz_course_lesson.seo_keyword AS Tags FROM fps_lilang.mz_forum_courseask
 LEFT JOIN fps_lilang.mz_forum_entity ON  fps_lilang.mz_forum_courseask.entity_ptr_id=mz_forum_entity.id
 LEFT JOIN lps_lilang.mz_course_lesson ON fps_lilang.mz_forum_entity.relate_id=lps_lilang.mz_course_lesson.id  ) AS Z    WHERE date_publish BETWEEN   '{begindate}' AND '{enddate}' AND  reply_count>0)  AS A
ON A.id=B.relate_id) AS F WHERE F.date_publish is NOT NULL        AND dif_hour>12

)AS Z
LEFT JOIN lps_lilang.mz_user_userprofile  AS US ON   Z.user=US.id
LEFT JOIN
(
SELECT SU.user_id,CS.coding  FROM  (SELECT user_id,student_class_id FROM  lps_lilang.mz_lps_classstudents GROUP BY user_id ) AS SU
 LEFT JOIN lps_lilang.mz_lps_class AS CS  ON  SU.student_class_id=CS.id
) AS Y
ON Z.`user`=Y.user_id   WHERE Z.user NOT IN (5) ORDER BY  Y.coding DESC
    """
    sql_ask_noanswer = """
SELECT Z.user,US.nick_name,Z.id,Z.type,Z.soure,Z.title,Z.Tags,Y.coding,(UNIX_TIMESTAMP(NOW()) - UNIX_TIMESTAMP(Z.date_publish))/3600  AS H FROM (
SELECT Z.*  FROM (
SELECT fps_lilang.mz_forum_entity.reply_count,fps_lilang.mz_forum_entity.id , fps_lilang.mz_forum_entity.date_publish,fps_lilang.mz_forum_entity.user, '开放问答' AS type , '空' AS soure ,  fps_lilang.mz_forum_entity.title ,GROUP_CONCAT(fps_lilang.mz_common_tags.`name`) AS Tags FROM  fps_lilang.mz_forum_ask
	LEFT JOIN fps_lilang.mz_forum_entitytag ON fps_lilang.mz_forum_ask.entity_ptr_id=fps_lilang.mz_forum_entitytag.entity_id
	LEFT JOIN fps_lilang.mz_common_tags ON fps_lilang.mz_forum_entitytag.tag_id=fps_lilang.mz_common_tags.id
	LEFT JOIN fps_lilang.mz_forum_entity ON fps_lilang.mz_forum_ask.entity_ptr_id=fps_lilang.mz_forum_entity.id
GROUP BY fps_lilang.mz_forum_ask.entity_ptr_id
UNION ALL
SELECT fps_lilang.mz_forum_entity.reply_count,fps_lilang.mz_forum_entity.id , fps_lilang.mz_forum_entity.date_publish,fps_lilang.mz_forum_entity.user, '课程问答' AS type , lps_lilang.mz_course_lesson.`name` AS soure ,  fps_lilang.mz_forum_entity.title ,lps_lilang.mz_course_lesson.seo_keyword AS Tags FROM fps_lilang.mz_forum_courseask
 LEFT JOIN fps_lilang.mz_forum_entity ON  fps_lilang.mz_forum_courseask.entity_ptr_id=fps_lilang.mz_forum_entity.id
 LEFT JOIN lps_lilang.mz_course_lesson ON fps_lilang.mz_forum_entity.relate_id=lps_lilang.mz_course_lesson.id  ) AS Z    WHERE date_publish BETWEEN '{begindate}' AND '{enddate}' AND  reply_count=0

)AS Z
LEFT JOIN lps_lilang.mz_user_userprofile  AS US ON   Z.user=US.id
LEFT JOIN
(
SELECT SU.user_id,CS.coding  FROM  (SELECT user_id,student_class_id FROM  lps_lilang.mz_lps_classstudents GROUP BY user_id ) AS SU
 LEFT JOIN lps_lilang.mz_lps_class AS CS  ON  SU.student_class_id=CS.id
) AS Y
ON Z.`user`=Y.user_id   WHERE Z.user NOT IN (5, 21, 83,
47991, 41468, 11835, 40296, 21, 83, 15, 352, 14136, 17604, 18048, 51043,
34134, 48872, 39171, 30394, 2, 14, 28471, 28846, 11233, 31609, 43069,
50370, 53631, 53833, 58351, 58360, 53565, 41838, 43228, 43660, 2653,
6484, 32587, 11878) ORDER BY  H DESC
    """
    # 教师发布评论数据
    cur.execute( sql_ask.format(begindate=begindate,enddate=enddate))
    result = cur.fetchall()
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(u'教师每周发表评论数据',  cell_overwrite_ok = True)
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = u'微软雅黑'    # 指定“宋体”
    style.font = font
    worksheet.write(0, 0, u'姓名', style)
    worksheet.write(0, 1, u'问答数量',style)
    worksheet.write(0, 2, u'用户id',style)
    for i in range(len(result)):
        for j in range(len(result[i])):
            worksheet.write(i+1, j,label=result[i][j], style=style)
            j = j+1
        i = i+1

    #超过12小时没回复但已经回复的问题
    cur.execute( sql_ask_long.format(begindate=begindate,enddate=enddate))
    result2 = cur.fetchall()
    worksheet = workbook.add_sheet(u'超过12小时未回复但已经回复的问题',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'用户id', style)
    worksheet.write(0, 1, u'用户昵称', style)
    worksheet.write(0, 2, u'问答id', style)
    worksheet.write(0, 3, u'问答类型', style)
    worksheet.write(0, 4, u'源自课程',style)
    worksheet.write(0, 5, u'问答标题', style)
    worksheet.write(0, 6, u'标签', style)
    worksheet.write(0, 7, u'学生所属班级', style)
    for i in range(len(result2)):
        for j in range(len(result2[i])):
            worksheet.write(i+1, j, label=result2[i][j], style=style)
            j = j+1
        i = i+1
    #还没回复的问题
    cur.execute( sql_ask_noanswer.format(begindate=begindate,enddate=enddate))
    result3 = cur.fetchall()
    worksheet = workbook.add_sheet(u'还没回复的问题',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'用户id', style)
    worksheet.write(0, 1, u'用户昵称', style)
    worksheet.write(0, 2, u'问答id', style)
    worksheet.write(0, 3, u'问答类型', style)
    worksheet.write(0, 4, u'源自课程', style)
    worksheet.write(0, 5, u'问答标题', style)
    worksheet.write(0, 6, u'标签', style)
    worksheet.write(0, 7, u'学生所属班级', style)
    worksheet.write(0, 8, u'已经发布多少小时', style)
    for i in range(len(result3)):
        for j in range(len(result3[i])):
            worksheet.write(i+1, j, label=result3[i][j], style=style)
            j = j+1
        i = i+1
    file_name = 'Ask'+datetime.datetime.today().strftime("%Y%m%d%H%M%S")+'.xls'
    workbook.save(file_name)
    return file_name




# 发送邮件
def send_mail(to_list, sub, content, flilename):
    # 构造邮件内容
    me = u"每日数据统计"+"<"+'lilang@maiziedu.com'+">"
    msg = MIMEMultipart('related')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)      # 将收件人列表以‘；’分隔
    msgText = MIMEText('%s' %content, 'html', 'utf-8')
    msg.attach(msgText)
    # 操作附件
    att = MIMEText(open('%s'%flilename, 'rb').read(), 'base64', 'utf-8')
    att["Contect-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="%s"'%flilename
    msg.attach(att)
    try:
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", port=465)                         #连接服务器
        server.login('lilang@maiziedu.com', 'Woaiwojia001')               #登录操作
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


# 开始运行，先生成数据，再发送邮件
excel_create()
mailto_list = ['lilang@maiziedu.com']
send_mail(mailto_list, u'教师每日问答数据', u'教师每日问答数据', excel_create())

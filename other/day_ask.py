
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

a = [
    '1',
    '2',
    '3',
    '4',
]
b = '(' + ','.join(a) + ')'
def friday():
    oneday = datetime.timedelta(days=1)
    lastFriday = datetime.datetime.today()-oneday
    while lastFriday.weekday() != calendar.FRIDAY:
        lastFriday -= oneday
    return lastFriday

# 生成报表数据
def excel_create():
    # 定义数据库连接
    con0 = MySQLdb.Connect(host='192.168.1.142', user='root', passwd='1234', port=3306, charset='utf8')
    cur = con0.cursor()
    # 定义sql参数
    begindate = friday().date()
    enddate = datetime.date.today()
    # 定义excel样式参数
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = u'微软雅黑'    # 指定“宋体”
    style.font = font
    #sql语句集合
    sql_ask = """
    SELECT  CONVERT(DATE(date_publish),CHAR),type,count(1) FROM (
SELECT A.entity_ptr_id AS num , type, B.date_publish FROM (
SELECT entity_ptr_id,'问答-开放问答'  AS type FROM fps_lilang.mz_forum_ask
UNION ALL
SELECT entity_ptr_id,'问答-课程问答'  AS type FROM fps_lilang.mz_forum_courseask
UNION ALL
SELECT entity_ptr_id, CASE WHEN  category=1 THEN '文章-就业故事'  WHEN  category=2 THEN '文章-技术文章' WHEN  category=3 THEN '文章-麦子新闻' WHEN  category=4 THEN '文章-新课上线' ELSE '文章-吐槽'
						END AS type FROM fps_lilang.mz_forum_article
UNION ALL
SELECT entity_ptr_id, CASE WHEN  category=0 THEN '活动-麦子活动' ELSE '活动-麦子公开课'
            END AS type  FROM fps_lilang.mz_forum_activity  ) AS A
LEFT JOIN fps_lilang.mz_forum_entity  AS B ON A.entity_ptr_id=B.id WHERE B.date_publish  BETWEEN '{begindate}' AND '{enddate}'
UNION ALL
SELECT A.id AS num,B.type ,A.date_publish FROM fps_lilang.mz_forum_discuss  AS A LEFT JOIN
(
SELECT entity_ptr_id,'问答-开放问答评论'  AS type FROM fps_lilang.mz_forum_ask
UNION ALL
SELECT entity_ptr_id,'问答-课程问答评论'  AS type FROM fps_lilang.mz_forum_courseask
UNION ALL
SELECT entity_ptr_id, CASE WHEN  category=1 THEN '文章-就业故事评论'  WHEN  category=2 THEN '文章-技术文章评论' WHEN  category=3 THEN '文章-麦子新闻评论' WHEN  category=4 THEN '文章-新课上线评论' ELSE '文章-吐槽评论'
						END AS type FROM fps_lilang.mz_forum_article
UNION ALL
SELECT entity_ptr_id, CASE WHEN  category=0 THEN '活动-麦子活动评论' ELSE '活动-麦子公开课评论'
            END AS type  FROM fps_lilang.mz_forum_activity  ) AS B
ON A.relate_id=B.entity_ptr_id WHERE  A.date_publish  BETWEEN '{begindate}' AND '{enddate}'
) AS A  GROUP BY type,DATE(date_publish) ORDER BY -DATE(date_publish),type

    """
    sql_count = """
    SELECT count(1) FROM
	(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask UNION ALL  SELECT  entity_ptr_id FROM  fps_lilang.mz_forum_courseask ) AS B
INNER JOIN
	(SELECT * FROM fps_lilang.mz_forum_entity WHERE date_publish BETWEEN '{begindate}' AND '{enddate}' AND reply_count=0) AS A
ON A.id=B.entity_ptr_id ;
    """
    sql_ask_day = """
    SELECT dis_date,COUNT(1) FROM (
SELECT C.id,CONVERT(DATE(C.date_publish),CHAR) AS dis_date FROM (SELECT * FROM fps_lilang.mz_forum_entity  WHERE date_publish BETWEEN '{begindate}' AND '{enddate}') AS C INNER JOIN
	(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask UNION ALL SELECT entity_ptr_id FROM fps_lilang.mz_forum_courseask UNION ALL SELECT entity_ptr_id FROM fps_lilang.mz_forum_article ) AS D
ON C.id=D.entity_ptr_id
UNION ALL
SELECT B.id,A.dis_date FROM  (SELECT DATE(date_publish) AS dis_date,relate_id FROM fps_lilang.mz_forum_discuss WHERE type IN (0,1,3) AND date_publish BETWEEN '{begindate}' AND '{enddate}' GROUP BY DATE(date_publish),relate_id) AS A LEFT  JOIN
	fps_lilang.mz_forum_entity AS B ON A.relate_id= B.id  WHERE A.dis_date!=DATE(B.date_publish)
) AS E GROUP BY dis_date ORDER BY dis_date DESC;
    """
    sql_carrer_student = """
    SELECT E.count,D.* FROM(
	SELECT count(1)AS count,user FROM (
		SELECT A.id,A.user,date_publish FROM
			(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask  UNION ALL SELECT  entity_ptr_id FROM  fps_lilang.mz_forum_courseask ) AS B
				INNER JOIN
			(SELECT * FROM fps_lilang.mz_forum_entity WHERE date_publish BETWEEN '{begindate}' AND '{enddate}' ) AS A
		ON A.id=B.entity_ptr_id
			UNION ALL
		SELECT id,user,date_publish FROM fps_lilang.mz_forum_discuss WHERE type IN (0,3) AND date_publish BETWEEN '{begindate}' AND '{enddate}'
	) AS C GROUP BY user) AS E

INNER JOIN
	(SELECT B.id,B.username,B.nick_name,B.mobile,B.email,D.coding FROM lps_lilang.mz_user_userprofile_groups  AS A
		INNER JOIN (SELECT user_id,student_class_id FROM lps_lilang.mz_lps_classstudents GROUP BY user_id ) AS C ON C.user_id=A.userprofile_id
		LEFT JOIN lps_lilang.mz_lps_class AS D  ON C.student_class_id=D.id
		LEFT JOIN lps_lilang.mz_user_userprofile AS B  ON A.userprofile_id=B.id

	WHERE group_id=1 AND A.userprofile_id NOT IN (5, 21, 83,
	47991, 41468, 11835, 40296, 21, 83, 15, 352, 14136, 17604, 18048, 51043,
	34134, 48872, 39171, 30394, 2, 14, 28471, 28846, 11233, 31609, 43069,
	50370, 53631, 53833, 58351, 58360, 53565, 41838, 43228, 43660, 2653,
	6484, 32587, 11878)) AS D
	ON E.user=D.id  ORDER BY count DESC ;
    """
    sql_carrer_total = """
   SELECT D.coding,D.teacher_id,E.nick_name,C.entity_count,C.student_count,D.current_student_count,C.student_count/D.current_student_count*C.entity_count AS rate FROM (
SELECT student_class_id,count(1) AS entity_count ,count(DISTINCT(user_id)) AS student_count FROM (SELECT user_id,student_class_id FROM lps_lilang.mz_lps_classstudents) A INNER  JOIN
(SELECT id,user FROM  fps_lilang.mz_forum_entity WHERE date_publish BETWEEN  '{begindate}' AND '{enddate}'
 UNION ALL
 SELECT id,user FROM  fps_lilang.mz_forum_discuss WHERE date_publish BETWEEN  '{begindate}' AND '{enddate}'
) B ON A.user_id=B.user  GROUP BY student_class_id ) AS C
LEFT JOIN lps_lilang.mz_lps_class AS D  ON C.student_class_id=D.id
LEFT JOIN lps_lilang.mz_user_userprofile AS E ON D.teacher_id= E.id
ORDER BY rate DESC;
    """
    sql_student = """
    SELECT E.count,D.* FROM(
	SELECT count(1)AS count,user FROM (
		SELECT A.id,A.user,date_publish FROM
			(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask  UNION ALL SELECT  entity_ptr_id FROM  fps_lilang.mz_forum_courseask ) AS B
				INNER JOIN
			(SELECT * FROM fps_lilang.mz_forum_entity WHERE date_publish BETWEEN '{begindate}' AND '{enddate}' ) AS A
		ON A.id=B.entity_ptr_id
			UNION ALL
		SELECT id,user,date_publish FROM fps_lilang.mz_forum_discuss WHERE type IN (0,3) AND date_publish BETWEEN '{begindate}' AND '{enddate}'
	) AS C GROUP BY user) AS E
INNER JOIN
	(SELECT B.id,B.username,B.nick_name,B.mobile,B.email FROM lps_lilang.mz_user_userprofile_groups  AS A
		LEFT JOIN lps_lilang.mz_user_userprofile AS B
		ON A.userprofile_id=B.id
	WHERE group_id=1 AND A.userprofile_id NOT IN (5, 21, 83,
	47991, 41468, 11835, 40296, 21, 83, 15, 352, 14136, 17604, 18048, 51043,
	34134, 48872, 39171, 30394, 2, 14, 28471, 28846, 11233, 31609, 43069,
	50370, 53631, 53833, 58351, 58360, 53565, 41838, 43228, 43660, 2653,
	6484, 32587, 11878)) AS D
	ON E.user=D.id  ORDER BY count DESC ;
    """
    sql_teacher = """
     SELECT E.count,D.* FROM(
	SELECT count(1)AS count,user FROM (
		SELECT A.id,A.user,date_publish FROM
			(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask  UNION ALL SELECT  entity_ptr_id FROM  fps_lilang.mz_forum_courseask ) AS B
				INNER JOIN
			(SELECT * FROM fps_lilang.mz_forum_entity WHERE date_publish BETWEEN '{begindate}' AND '{enddate}' ) AS A
		ON A.id=B.entity_ptr_id
			UNION ALL
		SELECT id,user,date_publish FROM fps_lilang.mz_forum_discuss WHERE type IN (0,3) AND date_publish BETWEEN '{begindate}' AND '{enddate}'
	) AS C GROUP BY user) AS E
INNER JOIN
	(SELECT B.id,B.username,B.nick_name,B.mobile,B.email FROM lps_lilang.mz_user_userprofile_groups  AS A
		LEFT JOIN lps_lilang.mz_user_userprofile AS B
		ON A.userprofile_id=B.id
	WHERE group_id=2 AND A.userprofile_id NOT IN (5, 21, 83,
	47991, 41468, 11835, 40296, 21, 83, 15, 352, 14136, 17604, 18048, 51043,
	34134, 48872, 39171, 30394, 2, 14, 28471, 28846, 11233, 31609, 43069,
	50370, 53631, 53833, 58351, 58360, 53565, 41838, 43228, 43660, 2653,
	6484, 32587, 11878)) AS D
	ON E.user=D.id  ORDER BY count DESC ;
    """
    sql_askranking = """
    SELECT A.ranking,B.id,B.nick_name,B.username,B.mobile,CONVERT(DATE(count_date),CHAR) FROM fps_lilang.mz_forum_activaterank  AS A  LEFT JOIN lps_lilang.mz_user_userprofile AS B ON  A.user=B.id
 WHERE `user` !=0	ORDER BY count_end_date, ranking DESC LIMIT 15 ;
    """
    sql_noanswer = """
SELECT Z.user,US.nick_name,US.username,US.mobile,US.email,Z.id,CONVERT(Z.date_publish,CHAR),Z.type,Z.soure,Z.title,Z.Tags,Y.coding,(UNIX_TIMESTAMP(NOW()) - UNIX_TIMESTAMP(Z.date_publish))/3600  AS H FROM (
SELECT Z.*  FROM (
	SELECT D.reply_count,D.id , D.date_publish,D.user, '开放问答' AS type,'空' AS soure,D.title ,GROUP_CONCAT(C.`name`) AS Tags
		FROM  fps_lilang.mz_forum_ask 					 AS A
		LEFT JOIN fps_lilang.mz_forum_entitytag  AS B  ON A.entity_ptr_id=B.entity_id
		LEFT JOIN fps_lilang.mz_common_tags 		 AS C  ON B.tag_id=C.id
		LEFT JOIN fps_lilang.mz_forum_entity 		 AS D  ON A.entity_ptr_id=D.id
	GROUP BY A.entity_ptr_id
UNION ALL
SELECT B.reply_count,B.id , B.date_publish,B.user, '课程问答' AS type , D.name AS soure ,B.title ,GROUP_CONCAT(F.name) AS Tags
FROM fps_lilang.mz_forum_courseask 											AS  A
	LEFT JOIN fps_lilang.mz_forum_entity  								AS  B  ON  A.entity_ptr_id=B.id
	LEFT JOIN lps_lilang.mz_course_lesson 								AS  C  ON  B.relate_id=C.id
  LEFT JOIN lps_lilang.mz_course_course   							AS  D  ON  C.course_id=D.id
	LEFT JOIN lps_lilang.mz_course_course_search_keywords AS  E  ON  D.id=E.course_id
	LEFT JOIN lps_lilang.mz_common_keywords  							AS  F  ON  E.keywords_id=F.id
GROUP BY A.entity_ptr_id

) AS Z    WHERE date_publish BETWEEN  '{begindate}' AND '{enddate}' AND  reply_count=0

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
6484, 32587, 11878) ORDER BY  H DESC;

    """
    sql_12answer = """
    SELECT Z.user,US.nick_name,US.username,US.mobile,US.email,Z.id,CONVERT(Z.date_publish,CHAR),Z.type,Z.soure,Z.title,Z.Tags,Y.coding FROM (
SELECT  F.reply_count, F.id, F.date_publish,F.user ,F.type ,F.soure , F.title ,F.Tags  FROM (
SELECT *, (UNIX_TIMESTAMP(B.min) - UNIX_TIMESTAMP(A.date_publish))/3600 dif_hour FROM  (SELECT MIN(date_publish) AS min, relate_id  from fps_lilang.mz_forum_discuss WHERE type IN('3','0') AND date_publish BETWEEN  '{begindate}' AND '{enddate}' GROUP BY  relate_id ) AS B
 LEFT JOIN ( SELECT Z.* FROM (
SELECT D.reply_count,D.id , D.date_publish,D.user, '开放问答' AS type , '空' AS soure , D.title ,GROUP_CONCAT(C.`name`) AS Tags
	FROM  fps_lilang.mz_forum_ask														AS A
	LEFT JOIN fps_lilang.mz_forum_entitytag				AS B		ON A.entity_ptr_id=B.entity_id
	LEFT JOIN fps_lilang.mz_common_tags 					AS C		ON B.tag_id=C.id
	LEFT JOIN fps_lilang.mz_forum_entity 					AS D		ON A.entity_ptr_id=D.id
GROUP BY A.entity_ptr_id
UNION ALL
SELECT B.reply_count,B.id , B.date_publish,B.user, '课程问答' AS type , D.name AS soure ,  B.title ,GROUP_CONCAT(F.name) AS Tags
 FROM fps_lilang.mz_forum_courseask                                     AS A
 LEFT JOIN fps_lilang.mz_forum_entity                        AS B ON A.entity_ptr_id=B.id
 LEFT JOIN lps_lilang.mz_course_lesson                       AS C ON B.relate_id=C.id
 LEFT JOIN lps_lilang.mz_course_course                       AS D ON C.course_id=D.id
 LEFT JOIN lps_lilang.mz_course_course_search_keywords       AS E ON D.id=E.course_id
 LEFT JOIN lps_lilang.mz_common_keywords                     AS F ON E.keywords_id=F.id
GROUP BY A.entity_ptr_id

 ) AS Z    WHERE date_publish BETWEEN '{begindate}' AND '{enddate}' AND  reply_count>0)  AS A
ON A.id=B.relate_id ) AS F WHERE F.date_publish is NOT NULL       AND dif_hour>12

)AS Z
LEFT JOIN lps_lilang.mz_user_userprofile  AS US ON   Z.user=US.id
LEFT JOIN
(
SELECT SU.user_id,CS.coding  FROM  (SELECT user_id,student_class_id FROM  lps_lilang.mz_lps_classstudents GROUP BY user_id ) AS SU
 LEFT JOIN lps_lilang.mz_lps_class AS CS  ON  SU.student_class_id=CS.id
) AS Y
ON Z.`user`=Y.user_id   WHERE Z.user NOT IN (5) ORDER BY  Y.coding DESC;
    """
    sql_ask_hour = """
    SELECT A.hour_pub,sumcount,ask_count,artilce_count FROM (
SELECT hour_pub,COUNT(1) AS sumcount FROM (
SELECT C.id,HOUR(date_publish) AS hour_pub FROM (SELECT * FROM fps_lilang.mz_forum_entity  WHERE date_publish BETWEEN  '{begindate}' AND '{enddate}') AS C INNER JOIN
	(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask UNION ALL SELECT entity_ptr_id FROM fps_lilang.mz_forum_courseask UNION ALL SELECT entity_ptr_id FROM fps_lilang.mz_forum_article ) AS D
ON C.id=D.entity_ptr_id
UNION ALL
SELECT id,HOUR(date_publish) AS hour_pub FROM fps_lilang.mz_forum_discuss WHERE type IN (0,1,3) AND date_publish BETWEEN  '{begindate}' AND '{enddate}'
) AS E GROUP BY hour_pub
)  AS  A  LEFT JOIN
(
SELECT hour_pub,COUNT(1) AS ask_count FROM (
SELECT C.id,HOUR(date_publish) AS hour_pub FROM (SELECT * FROM fps_lilang.mz_forum_entity  WHERE date_publish BETWEEN '{begindate}' AND '{enddate}') AS C INNER JOIN
	(SELECT entity_ptr_id FROM fps_lilang.mz_forum_ask UNION ALL SELECT entity_ptr_id FROM fps_lilang.mz_forum_courseask ) AS D
ON C.id=D.entity_ptr_id
UNION ALL
SELECT id,HOUR(date_publish) AS hour_pub FROM fps_lilang.mz_forum_discuss WHERE type IN (0,3) AND date_publish BETWEEN '{begindate}' AND '{enddate}'
) AS E GROUP BY hour_pub
)
   AS  B   ON  A.hour_pub=B.hour_pub  LEFT JOIN
(
SELECT hour_pub,COUNT(1) AS artilce_count FROM (
SELECT C.id,HOUR(date_publish) AS hour_pub FROM (SELECT * FROM fps_lilang.mz_forum_entity  WHERE date_publish BETWEEN  '{begindate}' AND '{enddate}') AS C INNER JOIN
	( SELECT entity_ptr_id FROM fps_lilang.mz_forum_article ) AS D
ON C.id=D.entity_ptr_id
UNION ALL
SELECT id,HOUR(date_publish) AS hour_pub FROM fps_lilang.mz_forum_discuss WHERE type IN (1) AND date_publish BETWEEN  '{begindate}' AND '{enddate}'
) AS E GROUP BY hour_pub
)
	 AS  C  ON A.hour_pub=C.hour_pub  ORDER BY sumcount DESC
    """
    sql_divide_aritcle = """
    """
    sql_course_count = """
    SELECT  C.name,count(1) FROM (
SELECT relate_id,date_publish FROM fps_lilang.mz_forum_entity where relate_id is NOT NULL  AND date_publish BETWEEN  '{begindate}' AND '{enddate}'
UNION ALL
SELECT A.relate_id  ,B.date_publish  FROM fps_lilang.mz_forum_entity AS A
	LEFT JOIN fps_lilang.mz_forum_discuss as B ON  A.id=B.relate_id
WHERE A.relate_id IS NOT NULL AND B.date_publish BETWEEN  '{begindate}' AND '{enddate}' ) AS A
LEFT JOIN lps_lilang.mz_course_lesson AS B ON A.relate_id=B.id
LEFT JOIN lps_lilang.mz_course_course AS C ON B.course_id=C.id
GROUP BY  C.id ORDER BY count(1) DESC

    """
    sql_actnum = """
    SELECT CONVERT(DATE(date_publish),CHAR) 参与日期,count(1) 参与人数  FROM (
SELECT   user ,date_publish FROM (
SELECT date_publish,user FROM fps_lilang.mz_forum_entity
UNION ALL
SELECT date_publish,user FROM fps_lilang.mz_forum_discuss
) AS A WHERE A.date_publish BETWEEN   '{begindate}' AND '{enddate}'   GROUP BY  user
) AS B
GROUP BY DATE(date_publish) ORDER BY DATE(date_publish) DESC;
    """
    # 问答日报表
    cur.execute(sql_ask.format(begindate=begindate, enddate=enddate))
    result = cur.fetchall()
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet(u'FPS分类日报表',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'统计日期', style)
    worksheet.write(0, 1, u'发布类型', style)
    worksheet.write(0, 2, u'数量', style)
    worksheet.write(0, 5, u'没有回答的问答数', style)
    for i in range(len(result)):
        for j in range(len(result[i])):
            worksheet.write(i+1, j, label=result[i][j], style=style)
            j = j+1
        i = i+1
    # 没有回答问答汇总
    cur.execute(sql_count.format(begindate=begindate, enddate=enddate))
    result1 = cur.fetchall()
    worksheet.write(1, 5, result1[0][0])

    # 当天发布及被回复的非当天发布的文章问答数量
    cur.execute(sql_ask_day.format(begindate=begindate, enddate=enddate))
    result9 = cur.fetchall()
    worksheet = workbook.add_sheet(u'问答发布及回复',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'统计日期', style)
    worksheet.write(0, 1, u'数量', style)
    for i in range(len(result9)):
        for j in range(len(result9[i])):
            worksheet.write(i+1, j, label=result9[i][j], style=style)
            j = j+1
        i = i+1
    # 直通班学员问答评论数
    cur.execute(sql_carrer_student.format(begindate=begindate, enddate=enddate))
    result2 = cur.fetchall()
    worksheet = workbook.add_sheet(u'直通班问答数量',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'发布数量', style)
    worksheet.write(0, 1, u'用户id', style)
    worksheet.write(0, 2, u'用户名', style)
    worksheet.write(0, 3, u'用户昵称', style)
    worksheet.write(0, 4, u'手机', style)
    worksheet.write(0, 5, u'邮箱', style)
    worksheet.write(0, 6, u'所在班级', style)
    for i in range(len(result2)):
        for j in range(len(result2[i])):
            worksheet.write(i+1, j, label=result2[i][j], style=style)
            j = j+1
        i = i+1
    # 直通班整体情况
    cur.execute(sql_carrer_total.format(begindate=begindate, enddate=enddate))
    result6 = cur.fetchall()
    worksheet = workbook.add_sheet(u'直通班整体',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'班级代码', style)
    worksheet.write(0, 1, u'教师id', style)
    worksheet.write(0, 2, u'教师昵称', style)
    worksheet.write(0, 3, u'发布数量', style)
    worksheet.write(0, 4, u'参与学生数', style)
    worksheet.write(0, 5, u'学生总数', style)
    worksheet.write(0, 6, u'班级点数', style)
    for i in range(len(result6)):
        for j in range(len(result6[i])):
            worksheet.write(i+1, j, label=result6[i][j], style=style)
            j = j+1
        i = i+1

    # 普通学生的问答评论数
    cur.execute(sql_student.format(begindate=begindate, enddate=enddate))
    result5 = cur.fetchall()
    worksheet = workbook.add_sheet(u'学生统计数量',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'发布数量', style)
    worksheet.write(0, 1, u'用户id', style)
    worksheet.write(0, 2, u'用户名', style)
    worksheet.write(0, 3, u'用户昵称', style)
    worksheet.write(0, 4, u'手机', style)
    worksheet.write(0, 5, u'邮箱', style)
    for i in range(len(result5)):
        for j in range(len(result5[i])):
            worksheet.write(i+1, j, label=result5[i][j], style=style)
            j = j+1
        i = i+1

    # 老师的问答评论数
    cur.execute(sql_teacher.format(begindate=begindate, enddate=enddate))
    result4 = cur.fetchall()
    worksheet = workbook.add_sheet(u'老师统计数量',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'发布数量', style)
    worksheet.write(0, 1, u'用户id', style)
    worksheet.write(0, 2, u'用户名', style)
    worksheet.write(0, 3, u'用户昵称', style)
    worksheet.write(0, 4, u'手机', style)
    worksheet.write(0, 5, u'邮箱', style)
    for i in range(len(result4)):
        for j in range(len(result4[i])):
            worksheet.write(i+1, j, label=result4[i][j], style=style)
            j = j+1
        i = i+1
    # 上周问答前五名
    cur.execute(sql_askranking)
    result7 = cur.fetchall()
    worksheet = workbook.add_sheet(u'周排行',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'排吗名', style)
    worksheet.write(0, 1, u'用户id', style)
    worksheet.write(0, 2, u'用户昵称', style)
    worksheet.write(0, 3, u'用户名', style)
    worksheet.write(0, 4, u'手机', style)
    worksheet.write(0, 5, u'统计截止日期', style)
    for i in range(len(result7)):
        for j in range(len(result7[i])):
            worksheet.write(i+1, j, label=result7[i][j], style=style)
            j = j+1
        i = i+1

    # 没问答的问答统计
    cur.execute(sql_noanswer.format(begindate=begindate, enddate=enddate))
    result10 = cur.fetchall()
    worksheet = workbook.add_sheet(u'未回复',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'用户id', style)
    worksheet.write(0, 1, u'昵称', style)
    worksheet.write(0, 2, u'用户名', style)
    worksheet.write(0, 3, u'手机', style)
    worksheet.write(0, 4, u'邮箱', style)
    worksheet.write(0, 5, u'问答id', style)
    worksheet.write(0, 6, u'发布时间', style)
    worksheet.write(0, 7, u'类型', style)
    worksheet.write(0, 8, u'源自', style)
    worksheet.write(0, 9, u'标题', style)
    worksheet.write(0, 10, u'标签', style)
    worksheet.write(0, 11, u'班级名', style)
    worksheet.write(0, 12, u'发布了多久', style)
    for i in range(len(result10)):
        for j in range(len(result10[i])):
            worksheet.write(i+1, j, label=result10[i][j], style=style)
            j = j+1
        i = i+1
    # 超过12小时已回答的问答统计
    cur.execute(sql_12answer.format(begindate=begindate, enddate=enddate))
    result14 = cur.fetchall()
    worksheet = workbook.add_sheet(u'超12小时',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'用户id', style)
    worksheet.write(0, 1, u'昵称', style)
    worksheet.write(0, 2, u'用户名', style)
    worksheet.write(0, 3, u'手机', style)
    worksheet.write(0, 4, u'邮箱', style)
    worksheet.write(0, 5, u'问答id', style)
    worksheet.write(0, 6, u'发布时间', style)
    worksheet.write(0, 7, u'类型', style)
    worksheet.write(0, 8, u'源自', style)
    worksheet.write(0, 9, u'标题', style)
    worksheet.write(0, 10, u'标签', style)
    worksheet.write(0, 11, u'班级名', style)
    for i in range(len(result14)):
        for j in range(len(result14[i])):
            worksheet.write(i+1, j, label=result14[i][j], style=style)
            j = j+1
        i = i+1
    # 统计小时问答文章评论发布量
    cur.execute(sql_ask_hour.format(begindate=begindate, enddate=enddate))
    result15 = cur.fetchall()
    worksheet = workbook.add_sheet(u'发帖小时统计',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'小时', style)
    worksheet.write(0, 1, u'总数量', style)
    worksheet.write(0, 2, u'问答及其评论数', style)
    worksheet.write(0, 3, u'文章及其评论数', style)
    for i in range(len(result15)):
        for j in range(len(result15[i])):
            worksheet.write(i+1, j, label=result15[i][j], style=style)
            j = j+1
        i = i+1
    # 课程下评论数统计
    cur.execute(sql_course_count.format(begindate=begindate, enddate=enddate))
    result16 = cur.fetchall()
    worksheet = workbook.add_sheet(u'课程评论数',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'课程名', style)
    worksheet.write(0, 1, u'数量', style)
    for i in range(len(result16)):
        for j in range(len(result16[i])):
            worksheet.write(i+1, j, label=result16[i][j], style=style)
            j = j+1
        i = i+1
    # 每日FPS活跃人数
    cur.execute(sql_actnum.format(begindate=begindate, enddate=enddate))
    result17 = cur.fetchall()
    worksheet = workbook.add_sheet(u'FPS活跃人数',  cell_overwrite_ok = True)
    worksheet.write(0, 0, u'参与日期', style)
    worksheet.write(0, 1, u'人数', style)
    for i in range(len(result17)):
        for j in range(len(result17[i])):
            worksheet.write(i+1, j, label=result17[i][j], style=style)
            j = j+1
        i = i+1

    # 保存excel
    cur.close();
    file_name = 'FPS'+datetime.datetime.today().strftime("%Y%m%d%H%M%S")+'.xls'
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
mailto_list = [
         'lilang@maiziedu.com',
	 # 'andrew@maiziedu.com',
	 # 'eric@maiziedu.com',
	 # 'june@maiziedu.com',
    # 'jessie.wang@maiziedu.com'
]
send_mail(mailto_list, u'运营FPS日报表', u'运营FPS日报表', excel_create())

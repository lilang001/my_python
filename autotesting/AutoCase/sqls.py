# _*_ coding:utf-8 _*_
__author__ = 'Administrator'
from datetime import datetime
from datetime import timedelta

lps = 'lps_20160307'
fps = 'fps_20160302'
file_path = 'http://192.168.1.142/uploads/'
now = datetime.now()
def handle_weekday(cur_time):
    d = cur_time.weekday() - 4
    if d < 0:
        begin = (cur_time - timedelta(days=d+7)).date()
        end = cur_time
    else:
        begin = (cur_time - timedelta(days=d)).date()
        end = cur_time
    return begin, end
database_time = "SELECT NOW() ;"
ask_list = """
SELECT   avatar_url,nick_name, title ,content ,Tags, source,UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(time_date),review_count, reply_count ,praise_count FROM (
SELECT A.*, B.nick_name,B.avatar_url,CASE WHEN D.date_publish IS NULL THEN A.date_publish ELSE  D.date_publish END AS time_date ,D.content   FROM (
SELECT D.is_head,D.review_count, D.reply_count,D.praise_count,D.id ,D.date_publish, D.user,'' AS source,D.title ,GROUP_CONCAT(C.name) AS Tags
		FROM  {fps}.mz_forum_ask 					 AS A
		LEFT JOIN {fps}.mz_forum_entitytag  AS B  ON A.entity_ptr_id=B.entity_id
		LEFT JOIN {fps}.mz_common_tags 		 AS C  ON B.tag_id=C.id
		INNER JOIN {fps}.mz_forum_entity 		 AS D  ON A.entity_ptr_id=D.id
	GROUP BY A.entity_ptr_id
UNION ALL
SELECT B.is_head,B.review_count,B.reply_count,B.praise_count,B.id ,B.date_publish, B.user , D.name AS source ,B.title ,F.name AS Tags
FROM {fps}.mz_forum_courseask 											AS  A
	INNER JOIN {fps}.mz_forum_entity  								AS  B  ON  A.entity_ptr_id=B.id
	LEFT JOIN {lps}.mz_course_lesson 								AS  C  ON  B.relate_id=C.id
  LEFT JOIN {lps}.mz_course_course   							AS  D  ON  C.course_id=D.id
	LEFT JOIN {lps}.mz_course_course_search_keywords AS  E  ON  D.id=E.course_id
	LEFT JOIN {lps}.mz_common_keywords  							AS  F  ON  E.keywords_id=F.id
GROUP BY A.entity_ptr_id) AS A
LEFT JOIN {lps}.mz_user_userprofile AS B ON A.user= B.id
LEFT JOIN (SELECT max(id) AS id,relate_id FROM {fps}.mz_forum_discuss  GROUP BY relate_id) AS C ON A.id=C.relate_id
LEFT JOIN {fps}.mz_forum_discuss AS D  ON C.id =D.id ORDER BY -is_head,-time_date  LIMIT 20 ) AS A ;
""".format(fps=fps, lps=lps)

ask_count = """
SELECT count(1) FROMhandle_weekday(now)[0].date()
( SELECT entity_ptr_id  FROM {fps}.mz_forum_courseask UNION ALL SELECT entity_ptr_id FROM {fps}.mz_forum_ask) AS A
""".format(fps=fps)

ask_hot_tags = """
SELECT  C.name FROM {fps}.mz_forum_ask AS A  INNER JOIN
{fps}.mz_forum_entitytag as B ON A.entity_ptr_id=B.entity_id
LEFT JOIN  {fps}.mz_common_tags AS C ON B.tag_id=C.id  GROUP BY C.name
ORDER BY -count(1)  limit 10;
""".format(fps=fps)

ask_rule = """1. 欢迎分享与IT、工作和生活相关的问题。 2. 禁止广告、羞辱、诽谤、人身攻击、使用不文明用语，违者将被冻结帐号。 3. 每成功发表一个问题麦子圈奖励2个积分。 4. 每增加一条评论麦子圈奖励1个积分。"""

ask_hot_qa = """
SELECT id ,title,reply_count FROM {fps}.mz_forum_entity AS A INNER JOIN
 {fps}.mz_forum_ask AS B ON A.id =B.entity_ptr_id ORDER BY reply_count desc  LIMIT 10
""".format(fps=fps)

ask_rank = """
SELECT C.id, C.avatar_url , C.nick_name, C.description ,count FROM (
SELECT count(1) AS count,user FROM
(SELECT id ,user ,date_publish FROM {fps}.mz_forum_entity AS A
	INNER JOIN {fps}.mz_forum_ask  AS B ON A.id =B.entity_ptr_id
	UNION ALL SELECT id ,user ,date_publish FROM {fps}.mz_forum_discuss WHERE type=0 )  AS  A
WHERE date_publish BETWEEN '{begindate}'  AND '{enddate}' GROUP BY A.user   )AS A
INNER   JOIN  (SELECT * from {lps}.mz_user_userprofile_groups WHERE group_id=1 ) AS B ON A.user = B.userprofile_id
INNER JOIN {lps}.mz_user_userprofile AS  C  ON A.user =C.id
WHERE A.user NOT IN (5, 21, 83, 47991, 41468, 11835, 40296, 21, 83, 15, 352, 14136, 17604,
18048, 51043, 34134, 48872, 39171, 30394, 2, 14, 28471, 28846, 11233,
31609, 43069, 50370, 53631, 53833, 58351, 58360, 53565, 41838, 43228,
43660, 2653, 6484, 32587, 11878) ORDER BY A.count desc LIMIT 5;
""".format(fps=fps, lps=lps, begindate=handle_weekday(now)[0], enddate=handle_weekday(now)[1])

ask_detail_base_info = """
SELECT A.title ,A.content , B.name ,C.nick_name  ,UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(A.date_publish) ,A.praise_count ,A.collect_count , A.review_count  FROM
(SELECT * FROM {fps}.mz_forum_entity WHERE id ='lilang_id') AS A
LEFT JOIN (SELECT A.entity_id ,GROUP_CONCAT(B.name) AS name FROM {fps}.mz_forum_entitytag AS A
LEFT JOIN {fps}.mz_common_tags AS B ON A.tag_id=B.id GROUP BY A.entity_id) AS B ON B.entity_id=A.id
LEFT JOIN {lps}.mz_user_userprofile  AS C ON A.user =C.id;
""".format(fps=fps, lps=lps)



ask_detail_course_ask_base_info = """
SELECT A.title ,A.content , E.name , D.name, C.nick_name, UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(A.date_publish),A.praise_count ,A.collect_count , A.review_count FROM
(SELECT * FROM {fps}.mz_forum_entity WHERE id ='lilang_id') AS A
LEFT JOIN {lps}.mz_user_userprofile  AS C ON A.user =C.id
LEFT JOIN {lps}.mz_course_lesson     AS B ON A.relate_id =B.id
LEFT JOIN {lps}.mz_course_course     AS D ON B.course_id=D.id
LEFT JOIN (SELECT A.course_id, B.name  FROM {lps}.mz_course_course_search_keywords AS A LEFT JOIN  {lps}.mz_common_keywords AS B ON A.keywords_id=B.id GROUP BY A.course_id )
AS E ON D.id=E.course_id;
""".format(fps=fps, lps=lps)

ask_discuss = """
SELECT A.user, B.nick_name,A.publish,A.content,A.praise_count FROM (
SELECT B.user ,UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(B.date_publish) AS publish,B.content,B.praise_count,B.parent_id AS index_id, B.date_publish FROM
( SELECT * FROM {fps}.mz_forum_discuss  WHERE relate_id='lilang_id'  AND parent_id IS NULL ORDER BY date_publish DESC LIMIT 10 ) AS A
INNER  JOIN {fps}.mz_forum_discuss AS B ON A.id= B.parent_id
UNION ALL SELECT * FROM (SELECT C.user ,UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(C.date_publish),C.content,C.praise_count, C.id AS index_id ,C.date_publish
FROM {fps}.mz_forum_discuss AS C  WHERE relate_id='lilang_id'  AND parent_id  IS NULL   ORDER BY date_publish DESC LIMIT 10 ) AS C  ) AS A
LEFT JOIN {lps}.mz_user_userprofile  AS B ON A.user=B.id ORDER BY  -index_id,date_publish   ;
""".format(fps=fps, lps=lps)

ask_detail_relate_ask = """
SELECT id , title, reply_count FROM (
SELECT DISTINCT(A.entity_id) AS ask_id FROM {fps}.mz_forum_entitytag AS A  WHERE tag_id in
( SELECT GROUP_CONCAT(tag_id) FROM {fps}.mz_forum_entitytag WHERE entity_id ='lilang_id') ) AS A
INNER JOIN {fps}.mz_forum_ask AS C ON A.ask_id=C.entity_ptr_id
LEFT JOIN {fps}.mz_forum_entity AS B ON A.ask_id = B.id  ORDER BY  date_publish   LIMIT 5
""".format(fps=fps)


ask_detail_relate_course_ask = """
SELECT id, title , reply_count FROM {fps}.mz_forum_entity
WHERE relate_id IN (SELECT relate_id FROM {fps}.mz_forum_entity WHERE id ='lilang_id' ) and id not IN ('lilang_id') LIMIT 5;
""".format(fps=fps)

# 开始文章了,少年们
article_list = """
SELECT  A.image, D.id,D.title, D.content ,GROUP_CONCAT(C.name) AS Tags , E.avatar_small_thumbnall, D.nickname, D.user,  UNIX_TIMESTAMP(NOW())-UNIX_TIMESTAMP(D.date_publish) ,
 D.review_count, D.reply_count, D.praise_count
		FROM  (SELECT * FROM  {fps}.mz_forum_article WHERE category='lilang_type')					 AS A
		LEFT JOIN {fps}.mz_forum_entitytag  AS B  ON A.entity_ptr_id=B.entity_id
		LEFT JOIN {fps}.mz_common_tags 		 AS C  ON B.tag_id=C.id
		INNER JOIN {fps}.mz_forum_entity 		 AS D  ON A.entity_ptr_id=D.id
		LEFT JOIN {lps}.mz_user_userprofile AS E ON E.id =D.user
	GROUP BY A.entity_ptr_id  ORDER BY  -is_head,-date_publish;
""".format(fps=fps, lps=lps)

article_total_count = """
SELECT count(1) FROM
( SELECT entity_ptr_id  FROM {fps}.mz_forum_article WHERE category = 'lilang_type' ) AS A
INNER JOIN {fps}.mz_forum_entity  AS B  ON A.entity_ptr_id=B.id;
""".format(fps=fps)

article_hot_tags = """
SELECT  C.name FROM {fps}.mz_forum_article AS A  INNER JOIN
{fps}.mz_forum_entitytag as B ON A.entity_ptr_id=B.entity_id
LEFT JOIN  {fps}.mz_common_tags AS C ON B.tag_id=C.id  GROUP BY C.name
ORDER BY -count(1)  limit 10;
""".format(fps=fps)

article_rule = """1. 欢迎分享与IT、工作和生活相关的文章。 2. 禁止广告、羞辱、诽谤、人身攻击、使用不文明用语，违者将被冻结帐号。 3. 文章经编辑审核后可见。 4. 每成功发表一篇文章麦子圈奖励3个积分。 5. 每增加一条评论麦子圈奖励1个积分。"""

article_hot_article = """
SELECT id ,title FROM {fps}.mz_forum_entity AS A INNER JOIN {fps}.mz_forum_article AS B
ON A.id =B.entity_ptr_id ORDER BY review_count desc  LIMIT 10 ;
""".format(fps=fps)

articel_detail_info = """
SELECT A.title ,C.avatar_small_thumbnall,C.id,C.nick_name , DATE_FORMAT(A.date_publish,'%Y-%m-%d %H:%i'),B.name,A.content  , A.praise_count ,A.collect_count , A.review_count FROM
(SELECT * FROM {fps}.mz_forum_entity WHERE id ='lilang_type') AS A
LEFT  JOIN (SELECT A.entity_id ,GROUP_CONCAT(B.name) AS name FROM {fps}.mz_forum_entitytag AS A  LEFT JOIN {fps}.mz_common_tags AS B ON A.tag_id=B.id GROUP BY A.entity_id) AS B ON B.entity_id=A.id
LEFT JOIN {lps}.mz_user_userprofile  AS C ON A.user =C.id;

""".format(fps=fps, lps=lps)

article_detail_relate = """
SELECT id , title  FROM (
SELECT DISTINCT(A.entity_id) AS entity_id FROM {fps}.mz_forum_entitytag AS A  WHERE tag_id in
( SELECT GROUP_CONCAT(tag_id) FROM {fps}.mz_forum_entitytag WHERE entity_id ='lilang_id') ) AS A
INNER JOIN {fps}.mz_forum_article AS C ON A.entity_id=C.entity_ptr_id
LEFT JOIN {fps}.mz_forum_entity AS B ON A.entity_id = B.id  ORDER BY  date_publish   LIMIT 5 ;
""".format(fps=fps)

get_excellent_course = """
SELECT  click_count,lesson_count , A.id , A.name ,A.image ,C.nick_name, CASE WHEN course_status=1 THEN 0 ELSE 1 END AS updating  FROM {lps}.mz_course_course  AS A
LEFT JOIN (SELECT course_id, count(1) AS lesson_count , SUM(play_count) AS hot_count FROM {lps}.mz_course_lesson GROUP BY course_id ) AS B
ON A.id= B.course_id
LEFT JOIN {lps}.mz_user_userprofile AS C ON A.teacher_id= C.id
ORDER BY hot_count  DESC LIMIT 15 ;
""".format(lps=lps)

get_excellent_course_ad = """
SELECT image_url, callback_url, target_id, ad_type, title FROM {lps}.mz_common_appad;
""".format(lps=lps)

get_career_course = """
SELECT course_count , student_count , A.name ,CASE WHEN class_count IS NULL THEN 0 ELSE class_count END AS  class_count, A.id,A.app_career_image FROM
 (SELECT *  FROM {lps}.mz_course_careercourse  WHERE course_scope IS NULL )  AS A
LEFT JOIN ( SELECT A.career_course_id ,count(1) AS course_count  FROM (SELECT * FROM {lps}.mz_course_stage WHERE  lps_version IS NULL ) AS A
						LEFT JOIN {lps}.mz_course_course_stages_m AS B  ON A.id= B.stage_id
						INNER JOIN (SELECT  * FROM {lps}.mz_course_course  WHERE is_active=1) AS C ON B.course_id=C.id
GROUP BY A.career_course_id ) AS B ON A.id=B.career_course_id
LEFT JOIN ( SELECT count(1) AS class_count , career_course_id FROM  {lps}.mz_lps_class GROUP BY career_course_id ) AS C ON A.id =C.career_course_id
 ORDER BY  A.index , A.id;
""".format(lps=lps)

get_career_detail = """
SELECT   A.description,'落地页地址,http://ww...' AS index_html, B.description AS stage_desc, B.id AS stage_id,B.name AS stage_name, D.id AS course_id,  D.image AS course_imgae, D.name AS course_name, CASE WHEN D.is_click=1 THEN 0 ELSE 1 END AS course_status
 FROM (SELECT * FROM  {lps}.mz_course_careercourse WHERE id ='my_id') AS A
LEFT JOIN (SELECT  * from {lps}.mz_course_stage WHERE  lps_version IS NULL ) AS B  ON A.id=B.career_course_id
LEFT JOIN {lps}.mz_course_course_stages_m AS C ON C.stage_id=B.id
LEFT JOIN {lps}.mz_course_course AS D ON D.id=C.course_id ORDER BY B.index, D.index ,D.id;
""".format(lps=lps)

get_career_price = """
SELECT   first_pay ,price ,D.id,D.current_student_count ,E.nick_name, D.coding,D.student_limit  FROM  (SELECT * FROM  {lps}.mz_course_careercourse WHERE id ='my_id' ) AS A
INNER JOIN (SELECT  career_course_id, SUM(price) AS first_pay FROM  {lps}.mz_course_stage WHERE is_try=1 GROUP BY career_course_id) AS B ON A.id=B.career_course_id
INNER JOIN (SELECT  career_course_id, SUM(price) AS price FROM  {lps}.mz_course_stage  GROUP BY career_course_id) AS C ON A.id=C.career_course_id
LEFT  JOIN  (SELECT  * FROM  {lps}.mz_lps_class WHERE is_active=1 AND status=1) AS D ON A.id=D.career_course_id
LEFT JOIN {lps}.mz_user_userprofile AS E ON D.teacher_id=E.id;
""".format(lps=lps)

submit_consult_info = """
SELECT  '数据存储成功' AS  message, name, phone FROM  {fps}.mz_common_appconsultinfo  ORDER BY date_publish DESC LIMIT 1;
""".format(fps=fps)

get_excellent_recom = """
SELECT  id, image , name FROM  {lps}.mz_course_course ORDER BY -click_count  limit 3;
""".format(lps=lps)

task_list = """
SELECT B.name ,D.name FROM {lps}.mz_course_careercourse  AS A
INNER JOIN  (SELECT  * FROM  {lps}.mz_course_stage where lps_version=3) AS B
ON A.id=B.career_course_id
INNER JOIN  {lps}.mz_lps3_stagetaskrelation  AS C ON B.id=C.stage_id
INNER JOIN  {lps}.mz_lps3_task               AS D ON C.task_id=D.id
WHERE A.id=2
ORDER BY B.index, C.index;
""".format(lps=lps)

ava = """
SELECT id,avatar_url,avatar_middle_thumbnall,avatar_small_thumbnall FROM  fps_lilang.mz_user_userprofile   ;
"""

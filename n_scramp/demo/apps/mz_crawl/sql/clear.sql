delete from mz_crawl_questionkeyword;
delete from mz_crawl_answer;
delete from mz_crawl_updatelog;
delete from mz_crawl_question;


alter table mz_crawl_questionkeyword auto_increment=1;
alter table mz_crawl_answer auto_increment=1;
alter table mz_crawl_updatelog auto_increment=1;
alter table mz_crawl_question auto_increment=1;
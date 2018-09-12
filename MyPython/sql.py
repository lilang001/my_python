__author__ = 'Administrator'

import sqlite3

conn = sqlite3.connect('test2.db')

cusor = conn.cursor()

cusor.execute('DROP TABLE user')
cusor.execute('create table user ( id varchar(20) primary key, name varchar(20))')
cusor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
print (cusor.rowcount)
cusor.execute('select * from user where id=?', '1')
values = cusor.fetchall()
print(values)
cusor.close()
conn.close()

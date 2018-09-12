# -*- coding: utf-8 -*-
__author__ = 'admin'
import shelve
import os
from datetime import datetime


class UserManagement(object):
    __doc__ = """
    用户注册。建立一个用户数据库(包括登录名、密码和上次登录时间戳)类(参考练习7-5
和9-12)，来管理一个系统，该系统要求用户在登录后才能访问某些资源。这个数据库类对用户进行
管理，并在实例化操作时加载之前保存的用户信息，提供访问函数来添加或更新数据库的信息。在
Edit By Vheavens
Edit By Vheavens
数据修改后，数据库会在垃圾回收时将新信息保存到磁盘。(参见__del__())
        """

    def __init__(self, dbfile):
        self.db = {}
        if os.path.exists(dbfile):
            self.db = file.open(dbfile, 'wr')
        for i in self.db:
            self.db.readlines()

        self.dbfile = dbfile
        self.flag = False



    def login(self,user,pwd):
        if not self.db.has_key(user):
            self.flag = False
            print 'user or pwd is wrong'
        elif self.db[user][0] == pwd:
            self.db[user][1] = datetime.now()
            self.flag = True
            print 'login success'
        else:
            print 'user or pwd is wrong'

    def deluser(self,user):
        if self.flag:
            self.db.pop(user)
        else:
            print 'login first'

    def updateuser(self, user, pwd):
        if self.flag:
            self.db[user] = [pwd, datetime.now()]
        else:
            print 'login first'

    def listall(self):
        if self.flag:
            for user in self.db:
                print user, self.db[user][0], self.db[user][1]
        else:
            print 'login first'

    def __del__(self):
        data = shelve.open(self.dbfile, 'c')
        data.update(self.db)
        data.close()
user = UserManagement("shelve.data")
user.login('lilang','111111')
# user.updateuser('test1','test1')
# user.updateuser('test2','test2')
# user.listall()

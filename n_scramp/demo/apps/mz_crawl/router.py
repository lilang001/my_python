# -*- coding: utf-8 -*-

__author__ = 'Jackie'


class CrawlDBRouter(object):
    """
    @attention: 一个控制 account 应用中模型的 所有数据库操作的路由
    """
    db_name = 'crawl'
    app_name = 'mz_crawl'
    def db_for_read(self, model, **hints):
        """
        @attention: crawl 应用中模型的操作指向 'crawl'
        """
        if model._meta.app_label == self.app_name:
            return self.db_name
        return None

    def db_for_write(self, model, **hints):
        """
        @attention: crawl 应用中模型的操作指向 'crawl'
        """
        if model._meta.app_label == self.app_name:
            return self.db_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        @attention: 如果包含 crawl 应用中的模型则允许所有关系
        """
        if obj1._meta.app_label == self.app_name or obj2._meta.app_label == self.app_name:
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        @attention: 确保 crawl 应用只存在于 'crawl' 数据库
        """
        if db == self.db_name:
            return model._meta.app_label == self.app_name
        elif model._meta.app_label == self.app_name:
            return False
        return None

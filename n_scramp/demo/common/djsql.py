# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.db import connections


def exec_sql(sql, params=None, database="default"):
    cursor = connections[database].cursor()
    cursor.execute(sql, params)
    return cursor.fetchall()

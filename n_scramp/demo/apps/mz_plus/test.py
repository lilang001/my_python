# -*- coding: utf-8 -*-
from django.db.models.query import QuerySet

__author__ = 'Jackie'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")

from mz_course.models import Course

print Course.objects.all().count()


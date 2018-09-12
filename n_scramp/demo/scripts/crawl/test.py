# -*- coding: utf-8 -*-

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")

django.setup()

from mz_crawl import interface

print interface.get_hot_tags()

print interface.get_top_questions_by_tag('C++')
print interface.get_questions('c#')

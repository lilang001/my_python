# -*- coding: utf-8 -*-

__author__ = 'Jackie'

import os
import json
import requests
from pyquery import PyQuery as PQ

KEYWORDS = dict()


def reload_keywords():
    json_file = os.path.join(os.path.dirname(__file__), 'keywords.json')
    try:
        new = json.load(open(json_file, 'rb'))
        KEYWORDS.clear()
        KEYWORDS.update(new)
    except:
        _init1()
        with open(json_file, 'wb') as f:
            json.dump(KEYWORDS, f)


def _init1():
    resp = requests.get("http://ask.csdn.net/tags?type=category")
    for a in PQ(resp.text)('.tags_list a'):
        KEYWORDS.setdefault(PQ(a).remove("em").text().strip().lower(), len(KEYWORDS) + 1)


def _init2():
    pass


if __name__ == "__main__":
    reload_keywords()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    from mz_crawl.models import KeyWord

    for k in sorted(KEYWORDS.iterkeys()):
        print type(k),k
        KeyWord(name=k).save()

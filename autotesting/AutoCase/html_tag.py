__author__ = 'Maiziedu'

import re
def filter_html_tag(str):
    filter_html_re = re.compile(r'<[^>]+>')
    return filter_html_re.sub('',str)

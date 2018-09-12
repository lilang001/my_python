# -*- coding: utf-8 -*-
__author__ = 'Jackie'

import os
import re

from django.utils.importlib import import_module


def main():
    """去sites目录下找模块
    有run方法认为可用模块
    """
    modules = list()
    _dir = os.path.join(os.path.dirname(__file__), 'sites')
    for filename in os.listdir(_dir):
        try:
            module = re.search(r"^(?P<module>crawl_\w+)\.py$",
                               filename).groups()[0]
            module = import_module("sites.%s" % module)
            if "run" in dir(module) and module.ACTIVE:  #
                modules.append(module)
        except:
            pass
    for module in modules:
        print module, 'run...'
        # module.run()
        import multiprocessing
        p = multiprocessing.Process(target=module.run)
        p.start()


if __name__ == "__main__":
    main()

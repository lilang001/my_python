# coding=utf-8
from pyse import TestRunner
# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))

# path = './baidu_case'
path = './Spark_case'

runner = TestRunner(path, "Auto Test Report", "Auto Test Report")
runner.run()

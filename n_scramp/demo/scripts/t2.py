# -*- coding: utf-8 -*-

"""
@author : Jackie
@date : 2015/11/17
@note :
"""
import requests

resp=requests.get("http://223.151.245.41/ocs.maiziedu.com/candy4java_4_199.mp4",stream=True)
print resp.status_code
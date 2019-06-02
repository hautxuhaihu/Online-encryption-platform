# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 下午4:00
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : http_client.py
# @Software: PyCharm

import requests
import json


s = requests.Session()
headers = {'Host':'www.xxx.com'}
post_data = json.dumps({"id": 1, "to_en_data": "待测数据", "password": "1234567890123456"})
url = "http://localhost:8888"
s.headers.update(headers)
r = s.post(url, data=post_data)
# r.text数据中含有两个引号，使用切片进行分割，得到真正的密文
print(r.text[1:-1])


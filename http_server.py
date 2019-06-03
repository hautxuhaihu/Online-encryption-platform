# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 下午10:59
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : http_server.py
# @Software: PyCharm

from http.server import HTTPServer, BaseHTTPRequestHandler
from aes import MyAES
import json


data = {'result': 'this is a test'}     # json格式的数据
host = ('localhost', 8888)


class HandleResquest(BaseHTTPRequestHandler):
    """
    这是一个可以接收post请求，并且可以接收post中的参数
    """
    def do_GET(self):
        post_data = self.rfile.read(int(self.headers['content-length'])).decode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        print("服务器收到信息GET：" + post_data)

    def do_POST(self):
        print('ok')
        post_data = self.rfile.read(int(self.headers['content-length'])).decode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        print("服务器收到信息："+post_data)

        post_data = json.loads(post_data)
        myAES = MyAES(post_data["password"])
        en_result = myAES.aes_encrypt(post_data["to_en_data"])
        print("服务器回复密文："+en_result)
        self.wfile.write(json.dumps(en_result).encode())


if __name__ == '__main__':
    server = HTTPServer(host, HandleResquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

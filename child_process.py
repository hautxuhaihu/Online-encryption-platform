# -*- coding: utf-8 -*-
# @Time    : 2019/6/4 下午10:57
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : child_process.py
# @Software: PyCharm

from twisted.internet import reactor
from aes import MyAES
import sys, json
from twisted.internet.threads import deferToThreadPool
from twisted.python.threadpool import ThreadPool

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
sys.stdin = open(sys.stdin.fileno(), mode='r', encoding='utf-8', buffering=1)

# 初始化并启动线程池
myThreadPool = ThreadPool(1, 5, 'myThreadPool')
myThreadPool.start()


def main():
    request_str = sys.stdin.readline().strip()

    # json解析数据
    request_json = json.loads(request_str)
    # 判断用户发送的数据中是否包括关键元素
    if "to_en_data" in request_json and "password" in request_json:
        # 调用模块加密
        # myAES = MyAES(request_json["password"])
        # encrypt_result = myAES.aes_encrypt(request_json["to_en_data"])
        # print(encrypt_result)
        deferToThreadPool(reactor, myThreadPool, encrypt, request_json)
    else:
        print("not found to_en_data or password")

    reactor.callLater(0, main)

def encrypt(request_json):

    myAES = MyAES(request_json["password"])
    encrypt_result = myAES.aes_encrypt(request_json["to_en_data"])
    print(encrypt_result)

reactor.run(main())


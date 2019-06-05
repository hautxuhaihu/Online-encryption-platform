# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 下午10:14
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : http_server_multithreading.py
# @Software: PyCharm


from twisted.logger import jsonFileLogObserver, Logger
from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.internet.threads import deferToThreadPool
from twisted.python.threadpool import ThreadPool
from aes import MyAES
import json
from read_ini import ReadINI

# 初始化并启动线程池
myThreadPool = ThreadPool(1, 5, 'myThreadPool')
myThreadPool.start()
# 实例化Logger
log = Logger(observer=jsonFileLogObserver(open("myLog/log.json", "a")),
             namespace="http_server_multithreading")


def encrypt_task(request):
    """
    分析request请求，将用户待加密的数据加密
    :param request:
    :return:
    """
    request_str = request.content.read().decode()
    try:
        # json解析数据
        request_json = json.loads(request_str)
        # 判断用户发送的数据中是否包括关键元素
        if "to_en_data" in request_json and "password" in request_json:
            # 调用模块加密
            myAES= MyAES(request_json["password"])
            encrypt_result = myAES.aes_encrypt(request_json["to_en_data"])
            request.write(encrypt_result.encode())
            log.debug("{debug}.", debug=encrypt_result)
        else:
            request.write("not found to_en_data or password".encode())
            log.debug("{debug}.", debug="not found to_en_data or password")
    except:
        log.error("{error}", error="The json data in the request cannot be parsed normally")
    finally:
        request.finish()


class RequestHandler(resource.Resource):
    """
    此类用于处理用户发过来的请求
    """
    isLeaf = True

    def render_POST(self, request):
        """
        对post请求进行处理
        :param request:客户端发送过来的请求
        :return: 返回客户端AJAX状态值
        """
        deferToThreadPool(reactor, myThreadPool, encrypt_task, request)
        log.info("Got data: {data}.", data="AJAX status value is 1")
        return 1


# 监听8080端口，并开始twisted的事件循环
site = server.Site(RequestHandler())
port = int(ReadINI("config.ini").read("config","port"))
endpoint = endpoints.TCP4ServerEndpoint(reactor, port)
endpoint.listen(site)
log.info("{info}", info="Http server is listening port %s" % port)
reactor.run()


# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 下午10:14
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : http_server_multithreading.py
# @Software: PyCharm

from twisted.logger import jsonFileLogObserver, Logger
from twisted.web import server, resource
from twisted.internet import reactor, endpoints, protocol
from aes import MyAES
import json, os
from read_ini import ReadINI


log = Logger(observer=jsonFileLogObserver(open("myLog/log.json", "a")),
                     namespace="http_server_multithreading")


class MyPP(protocol.ProcessProtocol):
    def __init__(self):
        self.data = ""

    def connectionMade(self):
        print("connectionMade!")
        # print("xuhaihu\n".encode())
        # self.transport.write("xuhaihu\n".encode())
        # self.transport.closeStdin()

    def outReceived(self, data):
        print("outReceived! with %d bytes!" % len(data))
        self.data = data.decode()
        print(self.data)
        requestHandler.request.write(data)
        requestHandler.request.finish()

    def errReceived(self, data):
        print("errReceived! with %d bytes!" % len(data))
        print(self.data)

    def inConnectionLost(self):
        print("inConnectionLost! stdin is closed! (we probably did it)")

    def outConnectionLost(self):
        print("outConnectionLost! The child closed their stdout!")

    def errConnectionLost(self):
        print("errConnectionLost! The child closed their stderr.")

    def processExited(self, reason):
        print("processExited, status %d" % (reason.value.exitCode,))

    def processEnded(self, reason):
        print("processEnded, status %d" % (reason.value.exitCode,))
        print("quitting")
        reactor.stop()


myPP = MyPP()
reactor.spawnProcess(myPP, os.environ['VIRTUAL_ENV']+"/bin/python", [os.environ['VIRTUAL_ENV']+"/bin/python", "child_process.py"],
                     childFDs={0:"w", 1:"r", 2:2, 3:"w", 4:"r"})


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
            myPP.transport.write((request_json["password"]+"\n").encode())
            myAES = MyAES(request_json["password"])
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
        self.request = request
        request_str = request.content.read()+"\n".encode()
        myPP.transport.write(request_str)
        # myPP.transport.closeStdin()
        # deferToThreadPool(reactor, myThreadPool, encrypt_task, request)
        log.info("Got data: {data}.", data="AJAX status value is 1")
        return 1


# 监听8080端口，并开始twisted的事件循环
requestHandler = RequestHandler()
site = server.Site(requestHandler)
port = int(ReadINI("config.ini").read("config", "port"))
endpoint = endpoints.TCP4ServerEndpoint(reactor, port)
endpoint.listen(site)
log.info("{info}", info="Http server is listening port %s" % port)
reactor.run()


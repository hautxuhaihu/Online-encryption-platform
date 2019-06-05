# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 下午8:57
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : twisted_http_server_demo.py
# @Software: PyCharm

from twisted.web import server, resource
from twisted.internet import reactor, endpoints, protocol
from twisted.internet.threads import deferToThreadPool
from twisted.python.threadpool import ThreadPool
import time, os

# 初始化并启动线程池
myThreadPool = ThreadPool(1, 1, 'myThreadPool')
myThreadPool.start()


def time_consuming_task(request):
    time.sleep(5)
    request.write("<html>Hello, world!</html>".encode())
    request.finish()


class RequestHandler(resource.Resource):
    """
    此类用于处理用户发过来的请求
    """
    # 令isleaf=true，调用render函数
    isLeaf = True
    def render_GET(self, request):
        """
        用于处理GET请求
        :param request:Request对象，包含了所有客户端发送过看来的数据
        :return: 返回AJAX的状态码
        """
        deferToThreadPool(reactor, myThreadPool, time_consuming_task, request)
        return 1

    def render_POST(self, request):
        time.sleep(5)
        print(request.content.read().decode())


class MyPP(protocol.ProcessProtocol):
    def __init__(self, verses):
        self.verses = verses
        self.data = ""

    def connectionMade(self):
        print("connectionMade!")
        for i in range(self.verses):
            self.transport.write("abc\n".encode())

        # self.transport.closeStdin()

        # self.transport.closeStdin() # tell them we're done

    def outReceived(self, data):
        print("outReceived! with %d bytes!" % len(data))
        self.data = self.data + data.decode()
        print(self.data)

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


pp = MyPP(10)
# reactor.spawnProcess(pp, "ls", ["ls"], childFDs = { 0: "w", 1: "r", 2: "r" , 4: "w"})

reactor.spawnProcess(pp, os.environ['VIRTUAL_ENV']+"/bin/python", [os.environ['VIRTUAL_ENV']+"/bin/python", "child_process.py"],
                     childFDs={0:"w", 1:"r", 2:2, 3:"w", 4:"r"})


# 监听8080端口，并开始twisted的事件循环
site = server.Site(RequestHandler())
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(site)
reactor.run()
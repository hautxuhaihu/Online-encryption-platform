# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 下午8:57
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : twisted_http_server.py
# @Software: PyCharm

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from twisted.internet.threads import deferToThreadPool
from twisted.python.threadpool import ThreadPool
import time

# 初始化并启动线程池
myThreadPool = ThreadPool(1, 8, 'myThreadPool')
myThreadPool.start()


def time_consuming_task(request):
    time.sleep(5)
    request.write("Hello, world!".encode())
    request.finish()


class RequestHandler(resource.Resource):
    """
    此类用于处理用户发过来的请求
    """

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


# 监听8080端口，并开始twisted的事件循环
site = server.Site(RequestHandler())
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
endpoint.listen(site)
reactor.run()
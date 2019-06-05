# -*- coding: utf-8 -*-
# @Time    : 2019/6/4 下午10:57
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : child_process.py
# @Software: PyCharm

from twisted.internet import reactor
import sys, os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)

def main():
    input = sys.stdin.readline().strip('\n')
    print(input)
    reactor.callLater(0, main)


reactor.run(main())
# -*- coding: utf-8 -*-
# @Time    : 2019/6/5 下午7:06
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : sub.py
# @Software: PyCharm

import sys, os
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)


def main():
    running = True
    with open("test.txt", "a") as f:

        while running:
            # input = sys.stdin.readline().rstrip('\n')
            input = sys.stdin.readline().strip('\n')
            f.write(input+"\n")
            if input == 'q':
                running = False
            # print ("You said:%s" % input)


if __name__ == "__main__":
    main()
    # sys.exit(2)
# -*- coding: utf-8 -*-
# @Time    : 2019/6/3 下午10:14
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : read_ini.py
# @Software: PyCharm

import configparser


class ReadINI(object):
    def __init__(self, ini_file_name):
        self.ini_file_name = ini_file_name

    def read(self, ini_section, ini_key):
        conf = configparser.ConfigParser()
        conf.read(self.ini_file_name, encoding='utf-8')
        value = conf.get(ini_section, ini_key)
        return value


if __name__ == '__main__':
    readINI = ReadINI('config.ini')
    print(readINI.read('config', 'port'))
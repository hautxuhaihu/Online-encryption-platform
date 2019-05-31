# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 下午10:35
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : aes.py
# @Software: PyCharm

import base64
from Crypto.Cipher import AES


class MyAES(object):
    def __init__(self, key, to_en_text=None, to_de_text=None):
        self.key = key
        self.to_en_text = to_en_text
        self.to_de_text = to_de_text

    # str不是16的倍数那就补足为16的倍数
    def convert_to_16(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    #加密方法
    def encrypt_oracle(self, key, text):
        # 秘钥
        key = '123456'
        # 待加密文本
        text = 'ewrwerrrrrrr'
        # 初始化加密器
        aes = AES.new(self.convert_to_16(key), AES.MODE_ECB)
        #先进行aes加密
        encrypt_aes = aes.encrypt(self.convert_to_16(text))
        # 用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        print(encrypted_text)


    #解密方法
    def decrypt_oralce(self):
        # 秘钥
        key = '123456'
        # 密文
        text = 'qR/TQk4INsWeXdMSbCDDdA=='
        # 初始化加密器
        aes = AES.new(self.convert_to_16(key), AES.MODE_ECB)
        #优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
        #执行解密密并转码返回str
        decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','')
        print(decrypted_text)

if __name__ == '__main__':
    myAES = MyAES()
    myAES.decrypt_oralce()
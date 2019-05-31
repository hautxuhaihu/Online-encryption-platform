# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 下午10:35
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : aes.py
# @Software: PyCharm

import base64
from Crypto.Cipher import AES


class MyAES(object):
    """
    这是自定义的AES类，包含加密、解密功能
   Attributes:
       key:128位的秘钥
       to_en_text:待加密的字符串
       to_de_text:待解密的字符串

    """
    def __init__(self, key, to_en_text=None, to_de_text=None):
        """初始化AES对象,给待加密，待解密的属性赋值"""
        self.aes = AES.new(self.convert_to_16(key), AES.MODE_ECB)
        self.to_en_text = to_en_text
        self.to_de_text = to_de_text

    @classmethod
    def convert_to_16(cls, value):
        """str不是16的倍数那就补足为16的倍数"""
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    def aes_encrypt(self):
        """加密字符串方法"""
        # 先进行aes加密
        encrypt_aes = self.aes.encrypt(self.convert_to_16(self.to_en_text))
        # 用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
        return encrypted_text

    def aes_decrypt(self):
        """解密字符串方法"""
        # 优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(self.to_de_text.encode(encoding='utf-8'))
        # 执行解密密并转码返回str
        decrypted_text = str(self.aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0', '')
        print(decrypted_text)


if __name__ == '__main__':
    key = '123456'
    to_en_data = '123456'
    myAES = MyAES(key, to_en_text=to_en_data)
    encrypt_result = myAES.aes_encrypt()
    print(encrypt_result)

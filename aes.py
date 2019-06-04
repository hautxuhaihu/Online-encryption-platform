# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 下午10:35
# @Author  : xuhaihu
# @Email   : 1829755168@qq.com
# @File    : aes.py
# @Software: PyCharm

import base64
from Crypto.Cipher import AES
import time


class MyAES(object):
    """
    这是自定义的AES类，包含加密、解密功能
    Attributes:
        aes_key:128位的秘钥,16个长度大小的字符串
    """
    def __init__(self, aes_key):
        """
        初始化AES对象,给待加密，待解密的属性赋值
        :param aes_key: aes秘钥
        """
        self.aes = AES.new(aes_key.encode(), AES.MODE_ECB)

    @classmethod
    def pkcs7_padding(cls, text):
        """
        明文使用PKCS7填充
        最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
        :param text: 待加密内容(明文), string类型
        :return:填充过的数据，string类型
        """
        time.sleep(1)
        # 明文变成bytes的长度，utf-8编码时，英文占1个byte，而中文占3个byte
        bytes_length = len(bytes(text, encoding='utf-8'))
        # 计算需要填充的长度
        padding_size = AES.block_size - bytes_length % AES.block_size
        # tips：chr(padding_size)看与其它语言的约定，有的会使用'\0'
        padding_text = chr(padding_size) * padding_size
        return text + padding_text

    @classmethod
    def pkcs7_rm_padding(cls, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串，string类型
        :return:去填充后的数据，string类型
        """
        length = len(text)
        padding = ord(text[length - 1])
        return text[0:length - padding]

    def aes_encrypt(self, to_en_text):
        """
        加密字符串方法
        :param to_en_text: 待加密明文
        :return 返回String类型的密文
        """
        # 先进行数据填充
        text_with_padding = self.pkcs7_padding(to_en_text).encode()
        # 进行aes加密,aes.encrypt的输入格式为字节，输出为字节
        encrypt_data = self.aes.encrypt(text_with_padding)
        # 用base64编码
        base64_en_data = base64.encodebytes(encrypt_data)
        # 将base64编码的数据转化成字符串，并去掉换行符
        encrypted_text = base64_en_data.decode().replace("\n", "")
        return encrypted_text

    def aes_decrypt(self, to_de_text):
        """
        解密字符串方法
        :param to_de_text: 待解密密文
        :return 返回明文，string类型
        """
        # 优先逆向解密base64成bytes
        base64_de_data = base64.decodebytes(to_de_text.encode())
        # 执行aes解密并转码返回str,aes.decrypt的输入格式为字节，输出为字节
        decrypted_text = (self.aes.decrypt(base64_de_data)).decode()
        # 去除pkcs7填充数据
        text_rm_padding = self.pkcs7_rm_padding(decrypted_text)
        return text_rm_padding


if __name__ == '__main__':
    print("假设16字节的秘钥为："+"1234567890123456")
    print("待加密数据为："+"qwertyuiop")
    key = "1234567890123456"
    to_en_data = "qwertyuiop"
    myAES = MyAES(key)
    encrypt_result = myAES.aes_encrypt(to_en_data)
    print("加密后的密文为："+encrypt_result)
    print("---------------------------------------")
    decrypt_result = myAES.aes_decrypt(encrypt_result)
    print("将密文再次解密，得到明文："+decrypt_result)

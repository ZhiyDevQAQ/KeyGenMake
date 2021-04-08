#!/usr/bin/env python
# coding:utf-8
# @Author:ZhiyDevQAQ
# @Name:KeygenMake.py
# @Date:2021/4/8 16:29

from paramiko import RSAKey, SSHException
from io import StringIO
import platform


class getKeygen(object):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return '本类用于生成ssh的RSA公钥和私钥'

    def gen_keys(self, key=''):
        '''
        用于生成公钥和私钥

        :param String key: 私钥
        :return Dict keys:包含private_key和public_key两个键的字典
        '''
        # private_key_buffer暂存私钥,public_key_buffer暂存公钥,keys存储生成好的公钥和私钥并作为返回对象
        private_key_buffer = StringIO()
        public_key_buffer = StringIO()
        keys = {}
        # 首先判断有没有私钥传入，如果没有则生成一个私钥，如果有私钥则利用传入的私钥生成公钥
        if not key:
            try:
                key = RSAKey.generate(1024)
                key.write_private_key(private_key_buffer)
                private_key = private_key_buffer.getvalue()
                # print('private_key:%s' % private_key)
            except IOError as e:
                print('灵能数据写入失败,具体错误信息如下:%s' % e)
            except SSHException as e:
                print('无效的灵能参数key,具体错误信息:%s' % e)
        else:
            private_key = key
            private_key_buffer.write(private_key)
            print('private_key:%s' % private_key_buffer.getvalue())
            try:
                key = RSAKey.from_private_key(private_key_buffer)
            except SSHException as e:
                print('无效的灵能参数key,具体错误信息:%s' % e)

        for line in [key.get_name(),
                    " ",
                    key.get_base64(),
                    " %s@%s" % ("RedBlade", platform.uname()[1])]:
            public_key_buffer.write(line)
        public_key = public_key_buffer.getvalue()
        keys['private_key'] = private_key
        keys['public_key'] = public_key
        return keys

    def write_keygen(self, keys):
        '''
        将生成的公钥和私钥分别生成文件并写入

        :param keys: 上方返回的keys
        :return null:
        '''
        private_key = keys['private_key']
        public_key = keys['public_key']
        osname = platform.uname()[1]
        pubname = 'RedBlade_RSA_%s.pub' % osname
        priname = 'RedBlade_RSA_%s' % osname
        with open(pubname, 'w', encoding='utf-8') as f, open(priname, 'w', encoding='utf-8') as e:
            f.write(public_key)
            e.write(private_key)


if __name__ == '__main__':
    keygen = getKeygen()
    key = keygen.gen_keys()
    keygen.write_keygen(key)

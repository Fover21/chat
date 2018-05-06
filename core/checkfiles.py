# -*- coding: utf-8 -*-
# 自动创建settings模块中的所有txt文件
# 不存在则创建,否则不创建

import os
from conf import settings
from core.login import get_pwd
from lib.mypickle import MyPickle

files = settings.file_name  # 获取文件字典
for i in files:  # 遍历字典
    if os.path.exists(settings.file_name[i]) is False:  # 判断文件是否存在，False表示不存在
        with open(settings.file_name[i], mode='ab') as mk:  # 打开每一个文件
            if i == 'user':  # 判断是否为用户认证文件
                # 写入默认的用户认证文件
                user_list = [('xiao','123','red',[]),('韩雪','123','green',[]),('林志玲','123','yellow',[]),('赵丽颖','123','blue',[])]
                for j in user_list:
                    info = {}
                    encrypt_pwd = get_pwd(j[0], j[1])
                    info = {'username': j[0], 'password': encrypt_pwd, 'color': j[2],'friends':j[3],'ip': ('127.0.0.1', 9090)}
                    MyPickle(files[i]).dump(info)  # 写入文件



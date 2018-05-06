import os
import sys
import time

sys.path.append(os.path.dirname(os.getcwd()))  # 添加项目根目录到系统环境变量
from lib.mysocket import Mysocket
from lib.Prompt import Prompt
from conf import settings


class Server(object):
    def __init__(self):
        self.ip = settings.server['ip']
        self.port = settings.server['port']
        self.rxb = settings.server['rxb']

    def main(self):
        sk = Mysocket()
        sk.bind((self.ip, self.port))
        while True:
            print(Prompt.display('正在等待对方回复...', 'green'))
            msg, client_addr = sk.my_recv(self.rxb)  # udp协议不用建立链接
            name, color, friends, friends_color, mesg = msg.split(':')

            print(''.center(36, '='))
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            print(Prompt.display('{} : {}'.format(name, mesg), color.strip()))
            inp = input('>>>')
            sk.my_send('{}:{}:{}'.format(friends, friends_color, inp), client_addr)  # 发送信息

        sk.close()


if __name__ == '__main__':
    Server().main()

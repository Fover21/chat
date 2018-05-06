import time
from lib.mysocket import Mysocket
from lib.mypickle import MyPickle
from lib.Prompt import Prompt
from conf import settings


class Client(object):

    def __init__(self, info):
        self.info = info
        self.ip = '127.0.0.1'
        self.port = 9090
        self.rxb = 1024
        self.user_files = MyPickle(settings.file_name['user'])
        self.sk = Mysocket()
        self.operate_lst = [
            ('查看所有用户', self.show_user),
            ('查看我的好友', self.show_my_user),
            ('添加我的好友', self.add_my_user),
            ('删除我的好友', self.delete_my_user),
            ('退出', self.q),
        ]
        self.main()

    def main(self):
        print(Prompt.display('您好: {} 欢迎使用聊天系统!\n'.format(self.info['username']), 'purple_red'))
        self.menu()

    def menu(self):
        while True:
            self.interlacing_color(self.operate_lst)  # 隔行换色
            num = input('输入您要做的操作序号：').strip()
            if num.isdigit():  # 判断数字
                num = int(num)  # 转换数字类型
                if num in range(1, len(self.operate_lst) + 1):  # 判断输入的序号范围
                    # print(operate_lst[num - 1][0])
                    self.operate_lst[num - 1][1]()
                else:
                    print('序号不存在,请重新输入!')
            else:
                print('操作序号必须为数字!')

    def run_chat(self, friends, friends_color):  # 发起聊天
        while True:
            inp = input('请输入发送内容,或者输入b返回: ').strip()
            if not inp:
                print(Prompt.display('发送内容不能为空!', 'red'))
                continue
            elif inp.upper() == 'B':
                pro_mes = Prompt.display('是否关闭当前会话 Y/N ? ', 'red')
                confirm = input(pro_mes).strip()
                if confirm.upper() == 'Y':
                    self.menu()
                    self.sk.close()
                    break
                elif confirm.upper() == 'N':
                    continue
                else:
                    print(Prompt.display('输入内容有误,请输入Y/N', 'red'))
                    continue

            self.sk.my_send(
                ('{}:{}:{}:{}:{}'.format(self.info['username'], self.info['color'], friends, friends_color, inp)),
                (self.ip, self.port))  # 发送数据给服务器
            print(Prompt.display('正在等待对方回复...', 'green'))
            msg, addr = self.sk.my_recv(self.rxb)  # 接收信息
            name, color, mesg = msg.split(':')  # 姓名,颜色,消息

            print(''.center(36, '='))
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            print(Prompt.display('❀{} : {}'.format(name, mesg), color))

        self.sk.close()  # 关闭连接

    def user_info(self):  # 获取当前用户详细信息
        for i in self.user_files.load():  # 读取用户文件
            if i['username'] == self.info['username']:
                return i

    def user_all(self):  # 所有用户列表,排除自己
        user_list = []
        for i in self.user_files.load():
            if i['username'] == self.info['username']:  # 如果当前登录用户等于自己，不追加到列表中
                pass
            else:
                user_list.append(i)
        return user_list

    def show_user(self):
        print('当前用户列表如下:'.center(30, '='))
        self.interlacing_color(self.user_all())
        print(''.center(36, '='))

    def show_my_user(self):  # 查看我的好友
        if self.user_info()['friends'] == []:
            print(Prompt.display('当前好友暂无!请添加好友', 'red'))
        else:
            friends_list = self.user_info()['friends']
            print('好友列表如下:'.center(31, '='))
            self.interlacing_color(friends_list)
            print(''.center(36, '='))
            while True:
                pro_mes = Prompt.display('是否发起聊天 Y/N(返回) ? ', 'green')
                confirm = input(pro_mes).strip()
                if confirm.upper() == 'Y':
                    self.interlacing_color(friends_list)
                    choice = input('请输入好友编号,或输入b返回: ').strip()
                    if choice.upper() == 'B':
                        # self.menu()
                        break
                    if choice.isdigit():
                        choice = int(choice)
                        if choice in range(1, len(friends_list) + 1):
                            friends = friends_list[choice - 1]  # 好友
                            color = self.friends_color(friends)  # 好友颜色
                            self.run_chat(friends, color)  # 发起会话
                        else:
                            print(Prompt.display('好友编号不存在,请重新输入!', 'red'))
                            continue
                    else:
                        print(Prompt.display('请输入数字!', 'red'))
                        continue

                elif confirm.upper() == 'N':
                    break
                else:
                    print(Prompt.display('输入错误,请重新输入!', 'red'))
                    continue

    def friends_color(self,friends):  # 获取好友颜色
        if not friends:
            return '好友名字不能为空!'

        for i in self.user_files.load():
            if i['username'] == friends:
                return i['color']

        return 'white'  # 找不到就显示白色

    def write_file(self, user_list):  # 写入文件
        if not user_list:
            return '用户列表不能为空!'

        with open(settings.file_name['user'], encoding='utf-8', mode='w') as f:  # 清空用户文件
            pass

        # 重新写入文件
        for i in user_list:
            try:
                self.user_files.dump(i)
            except Exception as e:
                print(e)
                return False

    def add(self, friends):  # 添加动作
        if not friends:
            return '好友名字不能为空!'

        if friends in self.user_info()['friends']:
            print(Prompt.display('好友已添加,请勿重复!', 'red'))
            return False

        user_list = []  # 所有用户列表
        for i in self.user_files.load():
            if i['username'] == self.info['username']:  # 如果是当前用户
                i['friends'].append(friends)  # 追加到好友列表中
            user_list.append(i)

        ret = self.write_file(user_list)  # 写入文件
        if ret is False:
            return False
        else:
            return True

    def add_my_user(self):  # 添加好友
        friends = self.choose_friends()  # 选择所有用户
        ret = self.add(friends[0])  # 添加指定的用户
        if ret is False:
            print(Prompt.display('添加好友失败!', 'red'))
        else:
            print(Prompt.display('添加好友成功!', 'green'))

    def delete_my_user(self):  # 删除好友
        friends_list = self.user_info()['friends']  # 获取当前用户好友列表
        print('好友列表如下:'.center(31, '='))
        self.interlacing_color(friends_list)  # 显示列表
        print(''.center(36, '='))

        while True:
            choice = input('请输入好友编号,或输入b返回: ').strip()
            if choice.upper() == 'B':
                # self.menu()
                break
            if choice.isdigit():
                choice = int(choice)
                if choice in range(1, len(friends_list) + 1):
                    friends = friends_list[choice - 1]  # 选择的好友
                    pro_mes = Prompt.display('您真的要删除吗? Y/N ', 'red')
                    confirm = input(pro_mes).strip()
                    if confirm.upper() == 'Y':
                        ret = self.delete(friends)  # 执行删除动作
                        if ret is False:
                            print(Prompt.display('删除好友失败!', 'red'))
                        else:
                            print(Prompt.display('删除好友成功!', 'green'))
                        break

            else:
                print(Prompt.display('请输入数字!', 'red'))

    def delete(self, friends):  # 删除动作
        if not friends:
            return '好友名字不能为空!'

        user_list = []  # 所有用户列表
        for i in self.user_files.load():
            if i['username'] == self.info['username']:  # 如果是当前用户

                i['friends'].remove(friends)  # 删除好友
            user_list.append(i)

        ret = self.write_file(user_list)  # 写入文件
        if ret is False:
            return False
        else:
            return True

    def q(self):  # 退出
        exit()

    def choose_friends(self):  # 选择好友，进行相应的操作
        self.show_user()  # 显示所有用户
        while True:
            choice = input('请输入用户编号,或输入b返回: ').strip()
            if choice.upper() == 'B':
                self.menu()
                break
            if choice.isdigit():
                choice = int(choice)
                if choice in range(1, len(self.user_all()) + 1):
                    friends = self.user_all()[choice - 1]
                    return friends['username'], friends['color']
            else:
                print(Prompt.display('请输入数字!', 'red'))

    def interlacing_color(self, custom_list):  # 列表隔行换色
        diff = 0  # 差值
        if len(custom_list) > len(Prompt.colour_dic):  # 当菜单列表长度大于颜色列表长度时
            diff = len(custom_list) - len(Prompt.colour_list)  # 菜单列表长度-颜色列表长度

        colour_list = list(Prompt.colour_dic)
        new_list = colour_list  # 新的颜色列表

        if diff >= 0:  # 当菜单列表长度大于等于颜色列表长度时
            for i in range(diff + 1):
                new_list.append(colour_list[i])  # 添加颜色,使颜色列表等于菜单列表长度

        count = -1  # 颜色列表索引值，默认为-1
        for key, item in enumerate(custom_list, 1):  # 获取每个角色类的operate_lst静态属性,显示的序列号从1开始
            count += 1  # 索引加1
            if type(item) == str:
                ret = Prompt.random_color('{}.\t{}'.format(key, item))  # 随机显示颜色
                print(ret)
            else:
                length = len(item)
                if length == 2:
                    ret = Prompt.display('{}.\t{}'.format(key, item[0]), new_list[count])  # 按照列表顺序显示颜色
                    print(ret)
                elif length == 5:
                    ret = Prompt.display('{}.\t{}'.format(key, item['username']), item['color'])  # 按照列表顺序显示颜色
                    print(ret)


if __name__ == '__main__':
    Client().main()
    # Client().show_my_user()
    # print(len(Client.user_all()))

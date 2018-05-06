from socket import *  # 导入socket模块
class Mysocket(socket):  # 继承socket
    def __init__(self,coding='utf-8'):  # 默认编码为utf-8
        self.coding = coding
        super().__init__(type=SOCK_DGRAM)  # 设定为udp协议
    def my_recv(self,num):  # num表示最大字节，比如1024
        msg,addr = self.recvfrom(num)
        return msg.decode(self.coding),addr  # 返回解码后的接收信息
    def my_send(self,msg,addr):  # msg和addr分别表示发送信息和连接ip:端口
        return self.sendto(msg.encode(self.coding),addr)  # 发送编码后的信息
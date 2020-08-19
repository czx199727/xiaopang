"""
基于 poll方法的IO多路服用网络并发
"""

from socket import *
from select import *

# 创建好监听套接字
sock = socket()
sock.bind(('0.0.0.0',8888))
sock.listen(5)

sock.setblocking(False)

#创建poll 对象
p = poll()

# 准备IO进行监控  map字典用于查找IO对象,必须与register
map = {sock.fileno():sock}
p.register(sock,EPOLLIN)
#循环监控IO发生
while True:
    #开始监控IO events -->[(filenp,event),(),()]
    events = p.poll()
    #伴随监控的IO的增多,就绪的IO情况也会复杂
    #分类讨论  分两类   sock --- connfd
    for fd,event in events:
        #有客户端连接
        if fd == sock.fileno():
            connfd,addr = map[fd].accept()
            print("Connect from",addr)
            connfd.setblocking(False)
            p.register(connfd) # 增加监控
            map[connfd.fileno()] = connfd  #维护字典
        elif event == POLLIN:
            #某个客户端发消息
            data = map[fd].recv(1024).decode()
            if not data:
                #客户端退出
                p.unregister(fd)
                map[fd].close()
                del map[fd]
                continue
            print('收到:',data)
            map[fd].send(b'OK')
        #     wlist.append(r)
        #
        # for w in ws:
        #     w.send(b'OK')
        #     wlist.remove(w) #如果不移除会一直就绪发送




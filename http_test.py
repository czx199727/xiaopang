"""
http 请求演示实例
"""
from socket import *

#tcp 套接字
s = socket()
s.bind(('0.0.0.0',8888))
s.listen(5)

c,addr = s.accept()
data = c.recv(1024*10)
print(data.decode())

html="HTTP/1.1 200 OK\r\n"
html+="Content-type:text/html\r\n"
html+="\r\n"
with open('python.html')as f:
    html+=f.read()

c.send(html.encode())

c.close()
s.close()


import socket
import threading
import time


def tcplink(sock, addr):
    print("接受一个新的链接%s:%s..." % addr)

    sock.send(b'from   server!')
    while True:
        data = sock.recv(1024)
        # time.sleep(1)
        print("一次服务器收到是%s" % str(data, encoding="utf-8"))
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('服务器给你返回的, %s!' % data.decode('utf-8')).encode('utf-8'))

    sock.close()
    print('Connection from %s:%s closed.' % addr)


def startServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 8887))
    s.listen(3)
    print("服务器开始等待连接")
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()


startServer()

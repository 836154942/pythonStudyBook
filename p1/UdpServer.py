import socket
import threading


def oneClint(addr):
    print("")


def start_Server():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 9998))
    while True:
        data, addr = s.recvfrom(1024)
        # threading.Thread(target=oneClint,args=(data,addr))
        print("一次接受的是 %s" % str(data, encoding="utf-8"))
        s.sendto(bytes("服务器返回的是 %s" % str(data, encoding="utf-8"), encoding="utf-8"), addr)


start_Server()

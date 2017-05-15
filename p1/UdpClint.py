import socket


def start_clint():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for data in ['第一条消息', '第2222222条消息', '333333个哥哥']:
        s.sendto(bytes(data, encoding="utf-8"), ('127.0.0.1', 9998))
        print(str(s.recv(1024), encoding="utf-8"))

    s.close()


start_clint()

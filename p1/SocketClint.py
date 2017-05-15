import socket


def getSina():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.sina.com.cn", 80))
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
    buffer = []
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break

    data = b''.join(buffer)  # 将字符串、元组、列表中的元素以指定的字符(分隔符)连接生成一个新的字符串
    header, html = data.split(b'\r\n\r\n', 1)
    s.close()
    print(header.decode('utf-8'))
    with open('sina.html', 'wb') as f:
        f.write(html)


def clientConnect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8887))

    buffer = []
    while True:
        d = s.recv(1024)
        if d:
            buffer.append(d)
        else:
            break

        print(str(d, encoding="utf-8"))
        sedText = input("输入发送的内容。 exit 结束")
        s.send(bytes(sedText, encoding="utf-8"))

    data = b''.join(buffer)
    print(str(data, encoding="utf-8"))


clientConnect()
# getSina()

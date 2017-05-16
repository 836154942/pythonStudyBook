def cus():
    r = ''
    while True:
        n = yield r
        # if not n:
        #     print("收到none")
        #     return
        print("消费者接收到%s" % n)
        r = "200  ok"

def worker(c):
    c.send(None)
    n = 0
    while n < 5:
        n += 1
        print("生产者生产了一个%s" % n)
        r = c.send(n)
        print("生产者接受到的是%s" % r)

def test_work_custom():
    c = cus()
    worker(c)

test_work_custom()
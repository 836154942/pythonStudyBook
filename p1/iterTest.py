class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        temp = self.a
        self.a = self.b
        self.b = temp + self.b

        # self.a, self.b = self.b, self.a + self.b  # 计算下一个值 简化写法
        if self.a > 100000:
            raise StopIteration
        return self.a

    def __getitem__(self, n):
        a, b = 1, 1
        if isinstance(n, int):
            for i in range(n):
                a, b = b, a + b
            return a
        elif isinstance(n, slice):
            L = []
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            if stop is None:
                 stop =100
            a, b = 1,1
            for i in range(stop):
                if  i >=start:
                    L.append(a)
                a, b = b, a + b
        return L

# for n in Fib():
#     print(n)

print(Fib()[:])

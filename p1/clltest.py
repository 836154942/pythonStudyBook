class FunC(object):
    def __init__(self, name, age):
        self.__name__ = name
        self.__age__ = age

    def __call__(self, *args, **kwargs):
        self.__name__ = args[0]
        self.__age__ = args[1]
        print("name  %s   age %s" % (self.__name__, self.__age__))



a =FunC("spc",24)
a("spcs ","23")
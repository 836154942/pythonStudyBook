# 面向对象学习
class Student(object):
    def __init__(self, name, sex):
        self.__name = name
        self.__sex = sex
        self.name2 = name
        self._name3 = name

    def get_name(self):
        return self.__name

    def print_info(self):
        print("姓名是 %s  ,性别是 %s" % (self.__name, self.__sex))


def test_object():
    a = Student("小明", "男")
    a.name2 = "刚发生了空间够大了开始就过来咯"
    a._name3 = "v;lasjdgjasgjlasjd"
    a.__name = "545754545424245"  # 定义为私有的是就算修改也不是对象的那个了
    print(a.name2)
    print("应该私有的  " + a._name3)

    a.print_info()


# 继承

class Animal(object):
    def __init__(sele, name):
        sele.name = name

    def eat(self):
        print(self.name + "吃饭了")


class Dog(Animal):
    def __init__(self):
        super(Dog, self).__init__("狗")

    def eat(self):
        print("小狗狗吃饭了")

    def __len__(self):
        return 100


class Cat(Animal):
    def __init__(self):
        super(Cat, self).__init__("猫")


class NotAnimal(object):
    def eat(self):
        print("我不是动物，但我也可以吃饭")


class Bad(object):
    def __init__(self):
        print("Bad")


def test_sub():
    d = Dog()
    c = Cat()
    d.eat()
    c.eat()


def showEat(animal):
    animal.eat()


def test_eat():
    d = Dog()
    showEat(d)
    c = Cat()
    showEat(c)
    x = NotAnimal()
    showEat(x)


def test_dir():
    d = Dog()
    # for i in dir(d):
    #     print(i)
    print(len(d))


def test_attr():
    d = Dog()
    print(" 是否有 eat " + str(hasattr(d, "eat")))
    if hasattr(d, "eat"):
        getattr(d, "eat")()

    setattr(d, "dog_sleep", lambda m: print("睡了%s 个小时" % m))
    if hasattr(d, "dog_sleep"):
         getattr(d,"dog_sleep")(5)

test_attr()

from types import MethodType


class Student(object):
    __slots__ = ("age")
    pass


def f1():
    s = Student()
    s.age = 10
    s2 = Student()
    Student.age = 20
    print(s.age)
    print(s2.age)


def set_age(self, age):
    self.age = age


def set_name(self, name):
    self.name = name


# 绑定实例的只能在一个实例上用
# 绑定对象的可以在在任何一个实例上通用
# 绑定对象 和是实例的，实例的会覆盖对象的
def f2():
    s = Student()
    # s.set_age = MethodType(set_age, s)
    # s.set_age(100)
    # print(s.age)
    s2 = Student()
    Student.set_age = MethodType(set_age, Student)
    s2.set_age(200)
    s.set_age = MethodType(set_age, s)
    s.set_age(100)
    Student.set_age(300)
    print(s2.age)
    print(s.age)
    print(Student.age)


# 对于属性 没有用slots 来限定，实例覆盖对象的。
# 用了slots以后， 对于属性 如果先设置实例的，然后再设置对象的值，实例自己的值，会被对象的覆盖.变成只读
# __slots__test
def f3():
    s = Student()
    s.name = "第一个学生"
    s.age = 1552
    # s.source =55  crash
    print(s.name)
    Student.name = "学生的name"
    Student.age = "学生的年龄"
    Student.source = "100"
    print(s.name + "  " + str(s.age) + " " + str(s.source))
    s2 = Student()
    print(s2.name + "  " + str(s2.age) + " " + str(s2.source))
    print(s.name + "  " + str(s.age) + " " + str(s.source))
    print(Student.name + "  " + str(Student.age) + " " + str(Student.source))


# 直接等于绑定
# 没有用__slots__  就是基本的实例赋值才有。。set的才会有，否则没有。。最基础的
# 没有用__slots__ 直接给一个对象是指一个方法为属性，那么对象没有这属性。只有实例才有。。。
# 用了 slots   实例是有的， 对象会有一个内部类的意思，产生这个变量的 引用 member_descriptor。
def f4():
    s = Student()
    Student.set_age = set_age
    s.set_age(99)
    s2 = Student()
    s2.set_age(77)
    print(s2.age)
    print(s.age)
    print(type(Student.age))  # crash if no  slots


# MethodType绑定
# 不管有没有slots  所有的实例通用一个。。静态变量
# 有了slots 。 绑定规定之外的也可以，不会报错。相当于静态变量
def f5():
    from types import MethodType
    s = Student()
    Student.set_age = MethodType(set_age, Student)
    s.set_age(22)
    print(s.age)
    s2 = Student()
    s2.set_age(33)
    print(s.age)
    print(Student.age)


class Teacher(object):
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    # read only age
    @property
    def age(self):
        return 80  # @property 注解的是get方法，属性名是 方法名字


def f6():
    t = Teacher()
    t.name=99
    # t.age = 50 crash
    print(t.name)
    print(t.age)




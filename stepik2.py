from random import randint
from string import ascii_lowercase, digits, ascii_uppercase
from math import sqrt

class EmailValidator:
    EMAIL_CHARS = ascii_lowercase + ascii_uppercase + digits + "_.@"
    EMAIL_RANDOM_CHARS = ascii_lowercase + ascii_uppercase + digits + "_"

    def __new__(cls, *args, **kwargs):
        return None

    @classmethod
    def check_email(cls, email):
        if not cls.__is_email_str(email):
            return False

        if not set(email) < set(cls.EMAIL_CHARS):
            return False

        s = email.split('@')
        if len(s) != 2:
            return False

        if len(s[0]) > 100 or len(s[1]) > 50:
            return False

        if "." not in s[1]:
            return False

        if email.count('..') > 0:
            return False

        return True

    @staticmethod
    def __is_email_str(email):
        return type(email) == str

    @classmethod
    def get_random_email(cls):
        n = randint(4, 20)
        length = len(cls.EMAIL_RANDOM_CHARS) - 1
        return "".join(cls.EMAIL_RANDOM_CHARS[randint(0, length)] for i in range(n)) + '@gmail.com'


class Car:
    def __init__(self):
        self.__model = None

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        if type(value) == str and 2 <= len(value) <= 100:
            self.__model = value


class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age


class WindowDlg:
    def __init__(self, title, width, height):
        self.__title: str = title
        self.__width: int = width
        self.__height: int = height

    def show(self):
        print(f'{self.__title}: {self.__width}, {self.__height}')

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if 0 <= value <= 1000:
            self.__width = value
            self.show()

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if 0 <= value <= 1000:
            self.__height = value
            self.show()


class StackObj:
    def __init__(self, data):
        self.__data: str = data
        self.__next = None

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, obj):
        if isinstance(obj, StackObj) or obj is None:
            self.__next = obj

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, obj):
        if isinstance(obj, StackObj) or obj is None:
            self.__data = obj


class Stack:
    def __init__(self):
        self.top = None
        self.last = None

    def push(self, obj):
        if self.last:
            self.last.next = obj

        self.last = obj
        if self.top is None:
            self.top = obj

    def pop(self):
        h = self.top
        if h is None:
            return
        while h and h.next != self.last:
            h = h.next
        if h:
            h.next = None
        last = self.last
        self.last = h
        if self.last is None:
            self.top = None

        return last

    def get_data(self):
        s = []
        h = self.top
        while h:
            s.append(h.data)
            h = h.next
        return s


class RadiusVector2D:
    MIN_COORD = -100
    MAX_COORD = 1024

    def __init__(self, x=0, y=0):
        self.__x = self.__y = 0
        self.x = x
        self.y = y

    @classmethod
    def __is_verify(cls, value):
        return type(value) in (int, float) and cls.MIN_COORD <= value <= cls.MAX_COORD

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, data):
        if self.__is_verify(data):
            self.__x = data

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, data):
        if self.__is_verify(data):
            self.__y = data

    @staticmethod
    def norm2(vector):
        res = vector.__x * vector.__x + vector.__y * vector.__y
        return res


class DecisionTree:
    @classmethod
    def predict(cls, root, x):
        obj = root
        while obj:
            obj_next = cls.get_next(obj, x)
            if obj_next is None:
                break
            obj = obj_next

        return obj.value


    @classmethod
    def get_next(cls, obj, x):
        if x[obj.index] == 1:
            return obj.left
        return obj.right


    @classmethod
    def add_obj(cls, obj, node=None, left=True):
        if node:
            if left is True:
                node.left = obj
            if left is False:
                node.right = obj
        return obj


class TreeObj:
    def __init__(self, indx, value=None):
        self.index = indx
        self.value: str = value
        self.__left = None
        self.__right = None

    @property
    def left(self):
        return self.__left

    @left.setter
    def left(self, left):
        self.__left = left

    @property
    def right(self):
        return self.__right

    @right.setter
    def right(self, right):
        self.__right = right


class LineTo:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class PathLines:
    def __init__(self, *args):
        self.coords = list((LineTo(0, 0), ) + args)

    def get_path(self):
        if self.coords is None:
            return
        else:
            return self.coords

    def get_length(self):
        res = 0
        for i in range(1, len(self.coords)):
            l = sqrt((self.coords[i].x - self.coords[i - 1].x)**2 + (self.coords[i].y - self.coords[i - 1].y)**2)
            res += l
        return res

    def add_line(self, line):
        self.coords.append(line)


class PhoneBook:
    phone_list = []

    def add_phone(self, phone):
        self.phone_list.append(phone)

    def remove_phone(self, indx):
        self.phone_list.pop(indx)

    def get_phone_list(self):
        return self.phone_list


class PhoneNumber:
    def __init__(self, number, fio):
        if len(str(number)) == 11 and type(number) == int:
            self.number = number
        if type(fio) == str:
            self.fio = fio


class FloatValue:
    @classmethod
    def check_value(cls, data):
        if type(data) != float:
            raise TypeError('Присваивать можно только вещественный тип данных')

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.check_value(value)
        instance.__dict__[self.name] = value


class Cell:
    value = FloatValue()

    def __init__(self, value=0.0):
        self.value = value


class TableSheet:
    def __init__(self, N, M):
        self.cells = [[Cell(0.0) for _ in range(M)] for _ in range(N)]


class ValidateString:
    def __init__(self, min_length=3, max_length=100):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, string):
        if type(string) == str and self.min_length <= len(string) <= self.max_length:
            return True
        else:
            return False


class StringValue:
    def __init__(self, validator):
        self.validator = validator

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if self.validator.validate(value):
            setattr(instance, self.name, value)

class RegisterForm:
    login = StringValue(validator=ValidateString())
    password = StringValue(validator=ValidateString())
    email = StringValue(validator=ValidateString())

    def __init__(self, login, password, email):
        self.login = login
        self.password = password
        self.email = email

    def get_fields(self):
        tete = [self.login, self.password, self.email]
        return tete

    def show(self):
        print(f'<form>\n', f'Логин: {self.login}\n', f'Пароль: {self.password}\n', f'Email: {self.email}\n', f'</form>')



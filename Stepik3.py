import time

class SuperShop:
    def __init__(self, name):
        self.name: str = name
        self.goods = []

    def add_product(self, product):
        self.goods.append(product)

    def remove_product(self, product):
        self.goods.remove(product)


class StringValue:
    def __init__(self, min_length=2, max_length=50):
        self.min_length = min_length
        self.max_length = max_length

    def check(self, string):
        if type(string) == str and self.min_length <= string <= self.max_length:
            return True
        else:
            return False


class PriceValue:
    def __init__(self, max_value=10000):
        self.max_value = max_value

    def check(self, price):
        if type(price) == int or type(price) == float and 0 <= price <= self.max_value:
            return True
        else:
            return False


class Product:
    name = StringValue()
    price = PriceValue()

    def __init__(self, name, price):
        self.name = name
        self.price = price


class Bag:
    def __init__(self, max_weight):
        self.max_weight: int = max_weight
        self.__things = []
        self.count = 0
        self.__total = 0

    @property
    def things(self):
        return self.__things

    def add_thing(self, thing):
        s = self.get_total_weight()
        if s + thing.weight <= self.max_weight:
            self.__things.append(thing)

    def remove_thing(self, indx):
        self.__things.pop(indx)

    def get_total_weight(self):
        return sum(t.weight for t in self.__things)


class Thing:
    def __init__(self, name, weight):
        if type(name) == str:
            self.name = name
        if type(weight) == int or type(weight) == float:
            self.weight = weight


class TVProgram:
    def __init__(self, chanel):
        self.items = []
        self.chanel: str = chanel

    def add_telecast(self, tl):
        self.items.append(tl)

    def remove_telecast(self, indx):
        for i in self.items:
            if i.uid == indx:
                self.items.remove(i)


class Telecast:
    def __init__(self, id, name, duration):
        if type(id) == int:
            self.__id = id
        if type(name) == str:
            self.__name = name
        if type(duration) == int:
            self.__duration = duration

    @property
    def uid(self):
        return self.__id

    @uid.setter
    def uid(self, value):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value):
        self.__duration = value


class Book:
    attrs = d = {
        'title': str,
        'author': str,
        'pages': int,
        'year': int
    }

    def __init__(self, title='', author='', pages=0, year=0):
        self.title: str = title
        self.author: str = author
        self.pages: int = pages
        self.year: int = year

    def __setattr__(self, key, value):
        if key in self.attrs and self.attrs[key] == type(value):
            super().__setattr__(key, value)
        else:
            raise TypeError("Неверный тип присваемых данных.")


book = Book('Python ООП', 'Сергей Балакирев', 123, 2022)


class Shop:
    def __init__(self, name):
        self.name = name
        self.goods = []

    def add_product(self, product):
        self.goods.append(product)

    def remove_product(self, product):
        self.goods.remove(product)


class Product:
    _id_instance = 1
    d = {
        'name': (str,),
        'weight': (int, float),
        'price': (int, float)
    }

    def __init__(self, name, weight, price):
        self.id = Product._id_instance
        Product._id_instance += 1

        self.name = name
        self.weight = weight
        self.price = price

    def __setattr__(self, key, value):
        if key in self.d and type(value) in self.d[key]:
            if (key == 'price' or key == 'weight') and value <= 0:
                raise TypeError("Неверный тип присваемых данных.")
        elif key in self.d:
            raise TypeError("Неверный тип присваемых данных.")

        object.__setattr__(self, key, value)

    def __delattr__(self, item):
        if item == 'id':
            raise AttributeError("Атрибут id удалять запрещено.")
        object.__delattr__(self, item)


class LessonItem:
    d = {
        'title': str,
        'practices': int,
        'duration': int
    }

    def __init__(self, title, practices, duration):
        self.title = title
        self.practices = practices
        self.duration = duration

    def __setattr__(self, key, value):
        if key in self.d and type(value) == self.d[key]:
            if (key == 'practices' or key == 'duration') and value <= 0:
                raise TypeError("Неверный тип присваиваемых данных.")
        elif key in self.d:
            raise TypeError("Неверный тип присваиваемых данных.")

        object.__setattr__(self, key, value)

    def __getattr__(self, item):
        if item not in self.d.keys():
            return False

    def __delattr__(self, item):
        if item in self.d.keys():
            raise AttributeError(f"Атрибут {item} удалять запрещено.")

        object.__delattr__(self, item)


class Module:
    def __init__(self, name):
        self.name = name
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def remove_lesson(self, indx):
        self.lessons.pop(indx)


class Course:
    def __init__(self, name):
        self.name = name
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)

    def remove_module(self, indx):
        self.modules.pop(indx)


class Museum:
    def __init__(self, name):
        self.name = name
        self.exhibits = []

    def add_exhibit(self, obj):
        self.exhibits.append(obj)

    def remove_exhibit(self, obj):
        self.exhibits.remove(obj)

    def get_info_exhibit(self, indx):
        info = self.exhibits[indx]
        return f'Описание экспоната {info.name}: {info.descr}'


class Picture:
    def __init__(self, name, author, descr):
        self.name = name
        self.author = author
        self.descr = descr


class Mummies:
    def __init__(self, name, location, descr):
        self.name = name
        self.location = location
        self.descr = descr


class Papyri:
    def __init__(self, name, date, descr):
        self.name = name
        self.date = date
        self.descr = descr


class SmartPhone:
    def __init__(self, model):
        self.model = model
        self.apps = []

    def add_app(self, app):
        if app.name not in [i.name for i in self.apps]:
            self.apps.append(app)
        else:
            pass

    def remove_app(self, app):
        self.apps.remove(app)


class AppVK:
    def __init__(self):
        self.name = 'Вконтакте'


class AppYouTube:
    def __init__(self, memory_max):
        self.name = "YouTube"
        self.memory_max = memory_max


class AppPhone:
    def __init__(self, phone_list):
        self.name = "Phone"
        self.phone_list = phone_list


class Circle:
    d = {
        '_Сircle__x': (float, int),
        '_Circle__y': (float, int),
        '_Circle__radius': (float, int)
    }

    def __init__(self, x, y, radius):
        self._Circle__x = x
        self._Circle__y = y
        self._Circle__radius = radius

    @property
    def x(self):
        return self._Circle__x

    @x.setter
    def x(self, value):
        self._Circle__x = value

    @property
    def y(self):
        return self._Circle__y

    @y.setter
    def y(self, value):
        self._Circle__y = value

    @property
    def radius(self):
        return self._Circle__radius

    @radius.setter
    def radius(self, value):
        self._Circle__radius = value

    def __getattr__(self, item):
        if isinstance(item, Circle):
            return object.__getattribute__(self, item)
        else:
            return False

    def __setattr__(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Неверный тип присваиваемых данных.")
        else:
            if key == '_Circle__x':
                object.__setattr__(self,  key, value)
            elif key == '_Circle__y':
                object.__setattr__(self,  key, value)
            elif key == '_Circle__radius' and value > 0:
                object.__setattr__(self, key, value)
            else:
                pass


class Dimensions:
    MIN_DIMENSION = 10
    MAX_DIMENSION = 1000

    def __init__(self, a, b, c):
        self._Dimension__a = a
        self._Dimension__b = b
        self._Dimension__c = c

    @property
    def a(self):
        return self._Dimension__a

    @a.setter
    def a(self, value):
        self._Dimension__a = value

    @property
    def b(self):
        return self._Dimension__b

    @b.setter
    def b(self, value):
        self._Dimension__b = value

    @property
    def c(self):
        return self._Dimension__c

    @c.setter
    def c(self, value):
        self._Dimension__c = value

    def __setattr__(self, key, value):
        if key == '_Dimension__a' or key == '_Dimension__b' or key == '_Dimension__c':
            if self.MIN_DIMENSION <= value <= self.MAX_DIMENSION:
                object.__setattr__(self, key, value)
            else:
                pass
        elif key == 'MIN_DIMENSION' or key == 'MAX_DIMENSION':
            raise AttributeError("Менять атрибуты MIN_DIMENSION и MAX_DIMENSION запрещено.")


class GeyserClassic:
    MAX_DATE_FILTER = 100

    def __init__(self):
        self.filter_class = ('Mechanical', 'Aragon', 'Calcium')
        self.filters = {
            (1, self.filter_class[0]): None,
            (2, self.filter_class[1]): None,
            (3, self.filter_class[2]): None
            }

    def add_filter(self, slot_num, filter):
        key = (slot_num, filter.__class__.__name__)
        if key in self.filters and not self.filters[key]:
            self.filters[key] = filter

    def remove_filter(self, slot_num):
        if type(slot_num) == int and 1 <= slot_num <= 3:
            key = (slot_num, self.filter_class[slot_num - 1])
            if key in self.filters:
                self.filters[key] = None

    def get_filters(self):
        return tuple(self.filters.values())

    def water_on(self):
        end = time.time()
        for f in self.filters.values():
            if f is None:
                return False
            start = f.date
            if end - start > self.MAX_DATE_FILTER:
                return False
        return True


class Mechanical:
    def __init__(self, date):
        self.date = date

    def __setattr__(self, key, value):
        if key == "date" and key in self.__dict__:
            return
        super().__setattr__(key, value)


class Aragon:
    def __init__(self, date):
        self.date = date

    def __setattr__(self, key, value):
        if key == "date" and key in self.__dict__:
            return
        super().__setattr__(key, value)


class Calcium:
    def __init__(self, date):
        self.date = date

    def __setattr__(self, key, value):
        if key == "date" and key in self.__dict__:
            return
        super().__setattr__(key, value)












































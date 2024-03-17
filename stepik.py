class CustomLabel:
    def __init__(self, text, **kwargs):
        self.text = text
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def config(self, **kwargs):
        self.__dict__.update(kwargs)
        for key, value in kwargs.items():
            self.__dict__[key] = value


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_person_info(self):
        print(f'Person: {self.name}, {self.age}')


class Company:
    def __init__(self, company_name, location):
        self.company_name = company_name
        self.location = location

    def display_company_info(self):
        print(f'Company: {self.company_name}, {self.location}')


class Employee:
    def __init__(self, name, age, company_name, location):
        self.personal_data = Person(name, age)
        self.work = Company(company_name, location)


class Task:
    def __init__(self, name, description, status=False):
        self.name = name
        self.description = description
        self.status = status

    def display(self):
        if self.status is True:
            print(f'{self.name} (Сделана)')
        else:
            print(f'{self.name} (Не сделана)')


class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)


class TaskManager:
    def __init__(self, tasklist):
        self.task_list = tasklist

    def mark_done(self, obj):
        obj.status = True

    def mark_undone(self, obj):
        obj.status = False

    def show_tasks(self):
        for task in self.task_list.tasks:
            Task.display(task)


class WeatherStation:
    __attributs = {
        "temperature": 0,
        "humidity": 0,
        "pressure": 0
    }

    def __init__(self):
        self.__dict__ = WeatherStation.__attributs

    def update_data(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def get_current_data(self):
        return (self.temperature, self.humidity, self.pressure)


class AverageCalculator:
    def __init__(self, numbers):
        self.numbers = numbers

    def __calculate_average(self):
        total = sum(self.numbers)
        return total / len(self.numbers)


average_calculator = AverageCalculator([1, 2, 3])
print(average_calculator._AverageCalculator__calculate_average())


class PizzaMaker:
    def __make_pepperoni(self):
        pass

    def _make_barbecue(self):
        pass


class Student:
    def __init__(self, name, age, branch):
        self.__name = name
        self.__age = age
        self.__branch = branch

    def __display_details(self):
        print(f'Имя: {self.__name}\n'
        f'Возраст: {self.__age}\n'
        f'Направление: {self.__branch}')

    def access_private_method(self):
        self._Student__display_details()


class BankDeposit:
    def __init__(self, name, balance, rate):
        self.name = name
        self.balance = balance
        self.rate = rate

    def __calculate_profit(self):
        res = self.balance // 100 * self.rate
        return res

    def get_balance_with_profit(self):
        return self.__calculate_profit() + self.balance


class Library:
    def __init__(self, books: list):
        self.__books = books

    def __check_availability(self, book):
        self.book = book
        if self.book not in self.__books:
            return False
        else:
            return True

    def search_book(self, book):
        self.book = book
        return self.__check_availability(self.book)

    def return_book(self, book):
        self.__books.append(book)

    def _checkout_book(self, book):
        self.book = book
        if self.book in self.__books:
            self.__books.remove(self.book)
            return True
        else:
            return False



class Employee:
    def __init__(self, name, position, hours_worked, hourly_rate):
        self.name = name
        self.__position = position
        self.__hours_worked = hours_worked
        self.__hourly_rate = hourly_rate

    def __calculate_salary(self):
        salary = self.__hourly_rate * self.__hours_worked
        return salary

    def _set_position(self, position):
        self.__position = position

    def get_position(self):
        return self.__position

    def get_salary(self):
        return self.__calculate_salary()

    def get_employee_details(self):
        res = f"Name: {self.name}, Position: {self.__position}, Salary: {self._Employee__calculate_salary()}"
        return res


class BankAccount:
    def __init__(self, account_number, balance):
        self._account_number = account_number
        self._balance = balance

    def get_account_number(self):
        return self._account_number

    def get_balance(self):
        return self._balance

    def set_balance(self, value):
        self._balance = value
        return self._balance


class Employee:
    def __init__(self, name, salary):
        self.__name = name
        self.__salary = salary

    def __get_name(self):
        return self.__name

    def __get_salary(self):
        return self.__salary

    def __set_salary(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self.__salary = value
        else:
            print(f"ErrorValue:{value}")

    title = property(fget=__get_name)
    reward = property(fget=__get_salary, fset=__set_salary)


class UserMail:
    def __init__(self, login, email):
        self.login = login
        self.__email = email

    def get_email(self):
        return self.__email

    def set_email(self, string):
        if isinstance(string, str) \
                and string.count('@') == 1 \
                    and '.' in string[string.find('@'):]:
                self.__email = string
        else:
            print(f"ErrorMail:{string}")

    email = property(fget=get_email, fset=set_email)


class Notebook:
    def __init__(self, *args):
        self._notes = args

    @property
    def notes_list(self):
        for i, k in enumerate(*self._notes):
            print(f'{i + 1}.{k}')


class Money:
    def __init__(self, dollars, cents):
        self.total_cents = dollars * 100 + cents

    @property
    def dollars(self):
        return self.total_cents // 100

    @property
    def cents(self):
        return self.total_cents % 100

    @dollars.setter
    def dollars(self, value):
        if isinstance(value, int) and value >= 0:
            self.total_cents = value * 100 + self.cents
        else:
            print('Error dollars')

    @cents.setter
    def cents(self, value):
        if isinstance(value, int) and 100 > value >= 0:
            self.total_cents = self.dollars * 100 + value
        else:
            print('Error cents')

    def __str__(self):
        return f'Ваше состояние составляет {self.dollars} долларов {self.cents} центов'


class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    @property
    def area(self):
        return self.length * self.width

r1 = Rectangle(5, 10)
assert isinstance(r1, Rectangle)
assert r1.area == 50
assert isinstance(type(r1).area, property), 'Вы не создали property area'

r2 = Rectangle(15, 3)
assert isinstance(r2, Rectangle)
assert r2.area == 45
assert isinstance(type(r2).area, property), 'Вы не создали property area'

r3 = Rectangle(43, 232)
assert r3.area == 9976
print('Good')
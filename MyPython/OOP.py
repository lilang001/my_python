__author__ = 'Administrator'
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.name, self.score))

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'

    def get_name(self):
        return self.__name

    def get_score(self):
        return self.__score

    def set_score(self, score):
        if 0<= score <= 100:
            self.__score = score
        else:
            raise ValueError('bad score')

# bart = Student('Bart Simpson', 59)
# bart.print_score()
# bart = Student('lilang1', 150)
# print(bart)
# print(bart.get_score())
# bart.set_score(0)
# print(bart.get_grade())

class Animal(object):
    def run(self):
        print('Animal is running...')


class Dog(Animal):
    pass

class Monkey(Animal):
    pass

dog = Dog()
dog.run()
print(type('lilang'))
print(dir('ABC'))
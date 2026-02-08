#1
class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    def bark(self):
        print("Dog barks")

my_dog = Dog()
my_dog.speak()
my_dog.bark()

#2
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    def display(self):
        print("The best car in the world is " + self.brand + "\nZhomart agai(C)")

c1 = Car("Toyota")
c1.display()

#3
class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

class Student(Person):
    def __init__(self, fname, lname, year):
        super().__init__(fname, lname)
        self.graduationyear = year

s1 = Student("Aliya", "Serik", 2024)
print(s1.graduationyear)

#4
class Phone:
    def call(self):
        print("Calling...")

class SmartPhone(Phone):
    def call(self):
        super().call()
        print("Using video mode")

p1 = SmartPhone()
p1.call()

#5
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def area(self):
        print(self.length * self.width)

sq = Square(10)
sq.area()
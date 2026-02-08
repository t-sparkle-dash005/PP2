#1
class Device:
    def __init__(self, brand):
        self.brand = brand

class Computer(Device):
    def __init__(self, brand, ram):
        super().__init__(brand)
        self.ram = ram

pc = Computer("Dell", "16GB")
print(pc.brand)
print(pc.ram)

#2
class Employee:
    def welcome(self):
        print("Welcome to the company!")

class Manager(Employee):
    def welcome(self):
        super().welcome()
        print("You are logged in as a Manager.")

mgr = Manager()
mgr.welcome()

#3
class Shape:
    def __init__(self, color):
        self.color = color

class Triangle(Shape):
    def __init__(self, color, base, height):
        super().__init__(color)
        self.base = base
        self.height = height

t1 = Triangle("Red", 10, 5)
print(t1.color)

#4
class Bird:
    def move(self):
        print("The bird is moving")

class Penguin(Bird):
    def move(self):
        super().move()
        print("Specifically, it is waddling")

p = Penguin()
p.move()

#5
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

class SavingsAccount(BankAccount):
    def __init__(self, balance, interest_rate):
        super().__init__(balance)
        self.interest_rate = interest_rate

    def show_info(self):
        print(f"Balance: {self.balance}, Rate: {self.interest_rate}")

sav = SavingsAccount(1000, 0.05)
sav.show_info()
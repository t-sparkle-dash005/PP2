#1
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return f"Player: {self.name}, Score: {self.score}"

p1 = Player("Peter", 100)
print(p1)

#2
class Robot:
    def __init__(self, model, version):
        self.model = model
        self.version = version

    def upgrade(self, new_version):
        self.version = new_version
        print("Robot " + self.model + " updated to " + str(self.version))

r1 = Robot("KZ-777", 2.0)
r1.upgrade(3.1)

#3
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __del__(self):
        print("Record for " + self.name + " has been deleted")

s1 = Student("Aisha", "10th")
del s1
#4
class Phone:
    def __init__(self, brand, price):
        self.brand = brand
        self.price = price

    def set_discount(self, amount):
        self.price -= amount

    def display(self):
        print(self.brand + " new price: $" + str(self.price))

ph1 = Phone("iPhone", 999)
ph1.set_discount(100)
ph1.display()
#5
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def scale(self, factor):
        self.radius = self.radius * factor

    def area(self):
        print(3.14 * self.radius ** 2)

c1 = Circle(5)
c1.scale(2)
c1.area()
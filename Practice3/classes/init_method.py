#1
class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

c1 = Car("Ford", "Something")
print(c1.brand)
print(c1.model)

#2
class Product:
  def __init__(self, name, price):
    self.name = name
    self.price = price

p1 = Product("Laptop", 999)
print(p1.name)
print(p1.price)

#3
class Dog:
  def __init__(self, name, breed):
    self.name = name
    self.breed = breed

d1 = Dog("Buddy", "Golden Retriever")
print(d1.name)
print(d1.breed)

#4
class Book:
  def __init__(self, title, author):
    self.title = title
    self.author = author

b1 = Book("A room of One's Own", "V. Woolf")
print(b1.title)
print(b1.author)

#5
class Movie:
  def __init__(self, title, year):
    self.title = title
    self.year = year

m1 = Movie("Interstellar", 2014)
print(m1.title)
print(m1.year)
#1
x = int(input())
y = x**2

if y > 0 and x > 0:
    print("parabola is opened up")
elif y < 0:
    print("parabola is opened down")

#2
age = int(input("How old are you?"))
if age >= 18:
    print("You can ride the roller coaster")
elif age < 18:
    print("You're too young")

#3
products = ["plates", "cups", "mugs", "bowls"]
if "cups" in products:
    print("you can add to cart")
elif "cups" not in products:
    print("cups are sold out")

#4
present = int(input())
absent = int(input())
if absent == 100 - present:
    print(f"{absent}% of students are absent")
elif present == 100:
    print("all students are present")
elif absent == 100:
    print("no students in class")

#5
x = int(input())
if x > 0:
    print("x i positive")
elif x < 0:
    print("x is negative")
elif not x > 0 or x < 0:
    print("x equals 0")
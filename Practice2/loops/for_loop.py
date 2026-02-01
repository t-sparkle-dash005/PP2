#1
a = "Hello, human"
for b in a:
    print(b, end=" ")
print(" ")

# 2
for n in range(0, 20, 5):
    print(n, end=" ")
print(" ")

#3
cars = ["Volvo", "BMW", "Toyota"]
for l in cars:
    print(l, sep = " ")

#4
for i in "Hello, World!":
    print(i, end = " \n")

#5
a = "uppercase words"
for x in a:
    print(x.upper(), end = " ")
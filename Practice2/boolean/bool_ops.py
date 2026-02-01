#1
x = 5
print(not x > 12 | x < 3)

#2
print(5 | 3)

#3
a = int(input()) #sqr root
b = int(input()) #result

if b >= 0 & a**2 == b:
    print(f"{a} is square root of {b}")
else :
    print(f"{a} is not square root of {b}")

#4
num = 10
if num % num == 0 & num // 1 == num:
    print(f"{num} is prime")
else:
    print(f"{num} is composite")

#5
pwd_reg = "qwerty"
pwd_log = str(input())
if len(pwd_reg) == len(pwd_log) & pwd_reg == pwd_log:
    print("successful login!")
else:
    print("forgot password?")
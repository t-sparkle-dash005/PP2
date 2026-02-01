#1
print("even numbers before 6")
s = 1
while s < 10:
    if s % 2 == 0:
        print(s)
    s += 1

#2
q = 50
while q > 0:
    q -= 10
    if q > 0:
        print(q)

#3
a = 100
while a > 0:
    a -= 10
    if a > 0:
        print(a)

#4
i = 10
while i >= 5:
    print(i)
    i -= 1

#5
num = 1
sum_of_num = 0
while num <= 5:
    print(num)
    sum_of_num += num
    num += 1
print("Sum:", sum_of_num)
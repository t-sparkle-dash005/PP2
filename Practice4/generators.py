#1
def squares_n(N):
    for i in range(N):
        yield i ** 2
#2
def even_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)
n = int(input("Enter a number! "))

#3
def div_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

#4
def sqrs(a, b):
    for i in range(a, b + 1):
        yield i ** 2

for val in sqrs(3, 6):
    print(val)

#5
def cdn(n):
    while n >= 0:
        yield n
        n -= 1

#6
def get_even_num():
    num = int(input())
    result = []
    
    for i in range(0, num +1):
        if i % 2 == 0:
            result.append(i)
    return result

get_even_num()
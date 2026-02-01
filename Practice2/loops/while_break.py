#1
a = 5
while a < 20:
    print(a)
    if a == 10:
        break
    a += 1

#2
print("print numbers until they won't be divisible by 5")
a1 = 11
while a1 < 20:
    print(a1)
    if a1 % 5 == 0:
        break
    a1 += 1

#3
srt = int(input())
tar = int(input())
fin = int(input())
cur = srt
while cur <= fin:
    print(cur)
    if cur == tar:
        break
    cur += 1

#4
num = 123
while num < 500:
    if num % 100 == 0:
        print(num)
        break
    num += 1

#5
d = 111
s = 0
while d > 0:
    print(d)
    s += d
    if d % 30 == 0:
        break
    d -= 50
print(s)
#1
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

#2
for num in range(1, 11):
    if num % 2 == 0:
        continue
    print(num)

#3
for l in "letter q will disappear":
    if l == "q":
        continue
    print(l, end = "")

#4
pos = [1, 2, -3, 4, -5]
for res in pos:
    if res < 0:
        continue
    print(res)

#5
for f in range(1, 30):
    if f % 5 == 0:
        continue
    print(f)
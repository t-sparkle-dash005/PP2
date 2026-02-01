#1
print("numbers divisible by 3 are ignored")
a2 = 21
while a2 < 30:
    a2 += 1
    if a2 % 3 == 0:
        continue
    print(a2)

#2
num = 1
while num < 5:
    num += 1
    if num == 2:
        continue
    print(num)

#3
num = 0
while num < 10:
    num += 1
    if num % 2 == 0:
        continue
    print(num)

#4
p = "Good morning friend"
w = p.split()
i = 0
while i < len(w):
    if w[i] == "friend":
        i += 1
        continue
    print(w[i])
    i += 1

#5
products = ["apples", "lemons", "bread", "cookies"]
idx = 0
while idx < len(products):
    if products[idx].startswith("a") or products[idx].startswith("b"):
        idx += 1
        continue
    print(products[idx])
    idx += 1
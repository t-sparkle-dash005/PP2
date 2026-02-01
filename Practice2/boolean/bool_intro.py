#1
a = True
b = False
print(a, b)

#2
print(bool(1))
print(bool(0))
print(bool())
print(bool("the most usual string"))

#3
print("Is it going to rain?")
def isCloudy() :
    return False
if isCloudy():
    print("Let's go outside!")
else:
    print("We can watch a movie instead.")

#4
divBy3 = 186
sum = divBy3 // 100 + divBy3 % 100 // 10 + divBy3 % 1
if sum % 3 == 0:
    print(f"{divBy3} can be divided by 3")

#5
login = str(input())
password = "123qwerty"
if login == password :
    print("Welcome, user!")
else:
    print("try again")


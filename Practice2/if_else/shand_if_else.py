#1
a = 12
b = 34
if a > b: print("a is more than b")

#2
print("a is maximum") if a > b else print("a and b are equal") if a == b else print("b is maximum")

#3
username = "user1"
print("Welcome, " + username) if len(username) >= 2 else print("username is too short")

#4
isSnowy = True
isSunday = True
if isSnowy and isSunday: print("take a rest")

#5
cweight = 5
print("the cat has normal weight")if cweight in range(4,6) else print("cat should go to vet")

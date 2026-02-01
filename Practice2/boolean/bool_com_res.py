#1
print(10 > 5)
print(10 < 5)
print(10 == 5)

#2
var1 = 100
var2 = 30
if var1 > var2:
    print("var1 is greater than var2")
else:
    print("var1 is not greater than var2")

#3
user_input = input("Is it true that 5 > 3?")
print("Correct answer is:", 5 > 3)

#4
def rain() :
    print(bool(0));

def sunny():
    print(bool(1));
weather = str(input("What's the weather like?"))
if weather == "it's raining":
    rain()
else:
    sunny()

#5
num = int(input("Is the number even or odd?"))
def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False
def isOdd(num):
    if num % 2 != 0:
        return True
    else:
        return False
if isEven(num):
    print("The number is even")
elif isOdd(num):
    print("The number is odd")




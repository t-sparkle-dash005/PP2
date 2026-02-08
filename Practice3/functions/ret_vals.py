#1
def funMean(x, y):
    return (x + y)//2

res = funMean(1, 10)
print(res)

#2
def count_vowels(text):
    vowels = "aeiou"
    count = 0
    
    for char in text:
        if char in vowels:
            count += 1
    return count

user_input = input("your string input!")
result = count_vowels(user_input)
print(result)

#3
def cir_area(rad):
    pi = 3.14159
    area = pi * (rad ** 2)
    return area

c_area = cir_area(5)
print(f"The area is: {c_area}")

#4
def is_even(number):
    return number % 2 == 0

num = 7
if is_even(num):
    print(f"{num} is even!")
else:
    print(f"{num} is odd!")

#5
def first_n(nums):
    for n in nums:
        if n < 0:
            return n
            
    return None

data = [10, 5, -3, 8, -2]
first_neg = first_n(data)
print(f"First negative value: {first_neg}")
#1
a = 12
b = 34
if a > b:
    print("a is greater than b")

#2
a_str = "qwerty"
b_str = "abcdef"
if len(a_str) == len(b_str) :
    print("string lengths of a and b are equal")

#3
if a_str != b_str:
    print("strings a and b are different")

#4
fishes = ["carp", "dolphin", "tuna", "bass"]
if fishes[1] in fishes:
    print("dolphin is a mammal")

#5
if a % 2 == 0  &  b % 2 == 0:
    print(f"sum of {a} and {b} will be even: {a + b}")
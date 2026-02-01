#1
n1 = int(input())
n2 = int(input())
if n1 > n2:
    print(f"{n1} is greater")
elif n1 < n2:
    print(f"{n2} is greater")
else:
    print(f"{n1} and {n2} are equal")

#2 quad. eq:
print("Given: x^2 - 8x + 15")
x1 = 3
x2 = 5
D = 8**2 - 4 * 15
if D > 0:
    print("x1 and x2 are different")
elif D == 0:
    print("x1 and x2 are the same")
else:
    print("this equation doesn't have answer") #only complex numbers

#3
available_places = 5
registered_st = ["Aigul", "Timur", "Robin", "Steve", "Lena", "Aisha"]
if len(registered_st) == available_places:
    print("students registered successfully!")
elif len(registered_st) > available_places:
    print("some students couldn't register")
else:
    print("not enough students registered")

#4
angle = int(input("Enter any angle in degrees: "))
if angle < 90:
    print("The angle is acute")
elif angle == 90:
    print("The angle is right")
elif angle > 90:
    print("The angle is obtuse")
elif angle == 180:
    print("The angle is straight")
else:
    print("angle is full") #when equals 360 deg

#5
exp_lvl = 10
test_passed = True
if exp_lvl >= 3:
    if test_passed:
        print("you're hired, congrats!")
    elif test_passed == False:
        print("you've failed the test, we'll call back")
else:
    print("your experience level is too low")
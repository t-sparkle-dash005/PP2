#1
sales = 5
match sales:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case 4:
        print("Thursday")
    case 5:
        print("Friday, sales day")
    case 6:
        print("Saturday")
    case 7:
        print("Sunday")
        
#2
cows = 3
match cows:
    case 1 | 2 | 3 | 4:
        print("barns full of cows")
    case 5 | 6:
        print("empty barns")

#3
odd_num = 3
match odd_num:
    case 1 | 3 | 5 | 7 | 9:
        print("this number is odd")
    case 2 | 4 | 6 | 8:
        print("this number is even")

#4
room = 4
chest = ["coins", "gems", "jewelry", "map"]
match room:
    case 1 | 2 | 3 | 5:
        print("empty rooms")
    case 4 if "coins" in chest:
        print("treasure is found!")

#5
figure = 2
angles = 3
match figure:
    case 1 | 3 | 4 | 5 if angles != 3:
        print("it's not a triangle")
    case 2 if angles == 3:
        print("it's triangle")
f1 = open("demo.txt")
print(f1.read())

f2 = open("C:\\Users\\Lordeoftherings\\Desktop\\demo2.txt")
print(f2.read())

with open("demo.txt") as fun:
    print(fun.read())
    
    print(fun.read(10))
    
    for x in fun:
        print(x)

print(f1.readline())
f1.close()
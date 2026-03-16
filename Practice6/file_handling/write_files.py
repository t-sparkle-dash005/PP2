with open("demo.txt", "a") as f:
    f.write("And then the lion and the mouse became friends.")
    
with open("demo.txt") as f:
    print(f.read())

with open("demofile.txt", "w") as f:
    f.write("overwrite the content of the file")

with open("demofile.txt") as f:
    print(f.read())

with open("newdemo.txt", "x") as f2:
    f2.write("A new file created!")
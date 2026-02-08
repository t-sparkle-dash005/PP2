#1 fun with args
def in_pond(fish): #fish = parameter
    print(fish + " in the pond")

in_pond("bass") #bass = argument
in_pond("catfish")
in_pond("whale")

#2 multiple args
def xor(x1,x2):
    print(f"XOR returns True only if {x1} or {x2} is True")

xor("a", "b")

#3 default val
def change_theme(theme_def = "light"):
    print("current theme is", theme_def)

change_theme()
change_theme("dark")
change_theme("time-oriented")

#4 key-value args
def laptop(pfc,price):
    print(f"this laptop has {pfc} and costs {price}")

laptop(pfc = "Intel i7 chip", price ="360$")

#positional args, order matters
laptop("AMD Ryzen 7", "500$")

#6 different data types passing
def store(cart):
    for thing in cart:
        print(thing)
#things in cart-^


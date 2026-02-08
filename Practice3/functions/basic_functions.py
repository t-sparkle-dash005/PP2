#1 function creation
def pr_fun():
    print("Hello, World!")

#calling pr_fun
pr_fun()

#2 reusabilty of functions
def fl_to_int(x):
    return(int(x))

print(fl_to_int(12.00))
print(fl_to_int(3.14))
print(fl_to_int(12.99))

#3 return values
def welcome():
    return "Welcome, user!"
greeting = welcome()
print(greeting)
print(greeting, "Have a nice day")

#4 returning value directly
print(welcome)

#5 using pass as a placeholder to implement later
def some_fun():
    pass
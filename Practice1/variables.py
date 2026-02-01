#print integer and string
x = 5
y = 'cups'
print(x, y)


#changing variable type int to str
x = 123
x = "abc"
print(x)


#data will be printed in given data type
x = str(3)
y = int(3)
z = float(3)


#get the data type
x = 5
y = 'John'
print(type(x))
print(type(y))


#case sensitive
a = 4
A = "not a"


#available variable names
myvar = "John"
my_var = "Alice"
_my_var = "Bob"
myVar = "Berik"
MYVAR = "Serik"
myvar2 = "Aliya"

print(myvar, my_var, _my_var, myVar, MYVAR, myvar2, sep=', ')


#assign multiple values to variables in one line
x, y, z = "Monday", "Tuesday", "Wednesday"
print(x + ", " + y + ", " + z)


#one value to multiple variables
x = y = z = "minion"
print(x)
print(y)
print(z)

#unpack a collection
animals = ["cat", "parrot", "dog"]
x, y, z = animals
print(x,y,z, sep=', ')


#printing output
x = "Python is awesome!"
print(x)


#print multiple variables
x = "Sentence"
y = "with"
z = "whitepaces"
print(x, y, z)


#printing variables with + sign
x = "Sentence"
y = "without"
z = "whitepaces"
print(x + y + z)


#print int and string together
x = 5
y = "John"
print(x, y)

#summing integers
x = 5
y = 10
print(x + y)

#creating a function and calling it
x = "awesome"

def myfunc():
    print("Python is " + x)


#call the function and change global variable
x = "awesome"

def myfunc():
    x = "fantastic"
    print("Python is " + x)

myfunc()

print("Python is " + x)
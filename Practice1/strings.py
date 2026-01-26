#single quotes = double quotes
print("Hello")
print('Hello')

#assigning string to variable
a = "Hello"
print(a)

#multiline string
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

#get the letter at position 1
a = "Hello, World!"
print(a[1])

#loop through the letters
for x in "banana":
    print(x)

#find the string length
a = "Hello, World!"
print(len(a))

#check if substring exists
txt = "The best things in life are free!"
print("free" in txt)

#result is 'c'
x = 'Welcome'
print(x[3])

#find the length
x = "Hello World"
print(len(x))

#find 1st char
txt = "Hello World"
print(txt[0])

#letters [2;5),
b = "Hello, World!"
print(b[2:5])

#letters [0;5)
b = "Hello, World!"
print(b[:5])

#letters from 2 to end
b = "Hello, World!"
print(b[2:])

#(-) idx o is on -5, d is on -2
b = "Hello, World!"
print(b[-5:-2])

#result is 'co'
x = 'Welcome'
print(x[3:5])

#char-s 2 to 4 idx
txt = "Hello World"
x = txt[2:5]

#result is 'come'
x = 'Welcome'
print(x[3:])

#all letters will be UPPERCASE
a = "Hello, World!"
print(a.upper())

#letters now lowercase
a = "Hello, World!"
print(a.lower())

#delete whitespace at start and end
a = " Hello, World! "
print(a.strip())

#replacing strings
a = "Hello, World!"
print(a.replace("H", "J"))

#splitting strings into list
a = "Hello, World!"
print(a.split(","))

#returns "Hello World"
txt = " Hello World "
x = txt.strip()

#"HELLO WORLD"
txt = "Hello World"
txt = txt.upper()

#"hello world"
txt = "Hello World"
txt = txt.lower()

#"Jello World"
txt = "Hello World"
txt = txt.replace("H", "J")

#concatenation
a = "Hello"
b = "World"
c = a + " " + b
print(c)

#result is 'WelcomeCoders'
x = 'Welcome'
y = 'Coders'
print(x + y)

#prints 'Join the party'
a = 'Join'
b = 'the'
c = 'party'
print(a + ' ' + b + ' ' + c)

#f-string creation
s = 100
rec = f"Add {s} grams of sugar to the bowl"

#2decimal places
pi = 3.14159
circle = f"Circle area is  multiplication of {pi:.2f} by r^2."
print(circle)

#math operations inside f-string
txt = f"This barn can hold {5+6} cows"
print(txt)

#esc chars
txt = " \"Tusaukeser\" is one of the most important kazakh tradition"
print(txt)

pytext = "indentation\n is very important in Python"
print(pytext)

#string methods: split string into list, add 2 space-tabs
msg = "peppers\ntomatoes\nlettuce"
print("We have", msg.splitlines(), "in our store", sep=' ')

txt = "G\tr\te\te\tt\ti\tn\tg\ts,\th\tu\tm\ta\tn"
x =  txt.expandtabs(2)
print(x)
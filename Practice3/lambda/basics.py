#1
sqr = lambda x: x ** 2
print(sqr(5))

#2
students = [("Ali", 25), ("Steve", 20), ("Sarah", 23)]
students.sort(key=lambda student: student[1])

print(students)

#3
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))

print(evens)

#4
prices = [10, 20, 30]
taxed_prices = list(map(lambda p: p * 1.1, prices))

print(taxed_prices)

#5
check_size = lambda x: "Big" if x > 100 else "Small"

print(check_size(150))
print(check_size(50))
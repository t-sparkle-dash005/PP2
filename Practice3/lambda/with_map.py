#1
cities = ["Almaty", "Astana", "Shymkent"]
upperc = list(map(lambda s: s.upper(), cities))

print(upperc)

#2
citiesAbroad = ["Tokyo", "London", "New York", "Paris", "Barcelona"]
long_cities = list(filter(lambda c: len(c) > 5, citiesAbroad))
print(long_cities)

#3
find_max = lambda a, b: a if a > b else b
print(find_max(15, 27))

#4
nums = [5, 12, 100]
form = list(map(lambda x: f"${x}.00", nums))
print(form)

#5
names = ["Mary", "Alice", "Paul", "Young"]
lengths = list(map(lambda name: len(name), names))
print(lengths)
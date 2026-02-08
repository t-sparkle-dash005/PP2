#1
words = ["banana", "pie", "apple", "watermelon"]
by_length = sorted(words, key=lambda x: len(x))
print(by_length)

#2
nums = [-10, 5, -2, 1, -20]
by_absolute = sorted(nums, key=lambda x: abs(x))
print(by_absolute)

#3
cars = [{"make": "Ford", "year": 2020}, {"make": "Tesla", "year": 2018}, {"make": "BMW", "year": 2024}]
by_year = sorted(cars, key=lambda x: x["year"])
print(by_year)

#4
colors = ["red", "green", "blue", "yellow"]
by_last_letter = sorted(colors, key=lambda x: x[-1])
print(by_last_letter)

#5
pairs = [(1, 5), (10, 2), (3, 3)]
by_sum = sorted(pairs, key=lambda x: x[0] + x[1])
print(by_sum)
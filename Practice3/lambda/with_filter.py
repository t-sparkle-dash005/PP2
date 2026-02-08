#1
scores = [22, 55, 90, 45, 12, 88]
high_scores = list(filter(lambda x: x > 50, scores))
print(high_scores)

#2
fruits = ["Strawberry", "Apple", "Arbuz", "Banana"]
a_fruits = list(filter(lambda x: x.startswith("A"), fruits))
print(a_fruits)

#3
items = ["Table", "", "Chair", "", "Lamp"]
active_items = list(filter(lambda x: x != "", items))
print(active_items)

#4
temps = [10, -5, 2, -1, 0, -8]
freezing = list(filter(lambda x: x < 0, temps))
print(freezing)

#5
words = ["tree", "cloud", "sun", "bird", "rain"]
f_letter_words = list(filter(lambda x: len(x) == 4, words))
print(f_letter_words)
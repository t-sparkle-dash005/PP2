import glob
from functools import reduce
practiceList = glob.glob("*.py")

upper_names = list(map(str.upper, ['demo.txt']))

only_img = list(filter(lambda x: x.endswith('.jpg'), ['cool_cat.jpg', 'garfield.jpg']))

path = ["D", "PP2", "Practice6", "demo.txt"]
fullpath = reduce(lambda x, y: x + "/" + y, path)
print(fullpath)
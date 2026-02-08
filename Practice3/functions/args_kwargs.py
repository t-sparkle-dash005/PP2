#1
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(10, 20))
print(sum_all(1, 2, 3, 4, 5))

#2
def print_profile(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

print_profile(name="Moldir", age=20, city="Taraz")

#3
def greet_team(manager, *staff):
    print(f"Manager: {manager}")
    print(f"Staff: {', '.join(staff)}")

greet_team("Sarah", "John", "Kelly", "Mike")

#4
def universal_wrapper(*args, **kwargs):
    print(f"Positional arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

universal_wrapper(1, 2, action="run", speed="fast")

#5
def build_car(make, model, year):
    print(f"Building a {year} {make} {model}")

car_info = ["Toyota", "Camry", 2024]
build_car(*car_info)

car_dict = {"make": "Tesla", "model": "Model 3", "year": 2023}
build_car(**car_dict)
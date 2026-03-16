files = ["demo.txt", "cool_cat.jpg", "garfield.jpg"]
sizes = ["1KB", "9,99KB", "12,6KB"]
for index, filename in enumerate(files, start=1):
    print(f"{index}: {filename}")

for name, size in zip(files, sizes):
    print(f"{name}: {size} bytes")
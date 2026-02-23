import json

with open('sample-data.json', 'r') as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<6}")
print("-" * 50, "-" * 20, "-" * 6, "-" * 6)

for attr in (obj["l1PhysIf"]["attributes"] for obj in data["imdata"]):
    print(f"{attr['dn']:<50} {attr['descr']:<20} {attr['speed']:<7} {attr['mtu']:<6}")
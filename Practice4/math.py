#1
import math
deg = 15
rad = math.radians(deg)
print(f"Enter degree! {deg}")
print(f"In radians: {rad:.6f}")

#2
h = 5
a = 5
b = 6
area = ((a + b) / 2) * h
print(area)

#3
import math
n = 4
s = 25
area_p = (n * s**2) / (4 * math.tan(math.pi / n))
print(f"Polygon area: {area_p:.0f}")

#4
a1 = 5
a2 = 6
area_par = float(a1 * a2)
print(f"Parallelogram area: {area_par}")

#5
import math
katet_a = 3
katet_b = 4
c = math.hypot(katet_a, katet_b)
print(f"The hypotenuse is: {c}")
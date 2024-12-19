import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Generate elliptic curve points
def generate_elliptic_curve(a, b, mod):
    if (4 * a**3 + 27 * b**2) % mod == 0:
        raise ValueError("Invalid parameters for elliptic curve")
    points = {}
    for x in range(mod):
        for y in range(mod):
            if (y**2 - x**3 - a * x - b) % mod == 0:
                points[(x, y)] = None
    points[(0, 0)] = None  # Add the point at infinity
    return points

# Generate a random generator point
def generate_generator(points, mod):
    G = random.choice(list(points.keys()))
    if G == (0, 0):
        return generate_generator(points, mod)
    return G

# Add two points on the elliptic curve
def add_points(P, Q, a, mod):
    if P == (0, 0):  # P is the point at infinity
        return Q
    if Q == (0, 0):  # Q is the point at infinity
        return P

    x1, y1 = P
    x2, y2 = Q

    if P != Q:
        # Regular point addition
        num = (y2 - y1) % mod
        den = pow(x2 - x1, -1, mod)
        m = (num * den) % mod
    else:
        # Point doubling
        num = (3 * x1**2 + a) % mod
        den = pow(2 * y1, -1, mod)
        m = (num * den) % mod

    x3 = (m**2 - x1 - x2) % mod
    y3 = (m * (x1 - x3) - y1) % mod

    return (x3, y3)

# Scalar multiplication: k * G
def scalar_multiplication(k, G, a, mod):
    result = (0, 0)  # Point at infinity
    temp = G

    while k:
        if k % 2 == 1:
            result = add_points(result, temp, a, mod)
        temp = add_points(temp, temp, a, mod)
        k //= 2

    return result

# Parameters for the elliptic curve
a = 2
b = 3
mod = 17  # Prime modulus

# Generate elliptic curve points
points = generate_elliptic_curve(a, b, mod)

# Generate a random generator point
G = generate_generator(points, mod)

# Scalar multiplication example
k = 3
kG_point = scalar_multiplication(k, G, a, mod)
print(f"{k} * G = {kG_point}")

# Parameters for plotting the curve
a = -1
b = 1

# Generate x values for plotting
x = np.linspace(-3, 3, 400)

# Calculate y values (positive and negative branches)
y_positive = np.sqrt(x**3 + a * x + b)
y_negative = -np.sqrt(x**3 + a * x + b)

# Plot the elliptic curve
plt.plot(x, y_positive, 'b', label="y^2 = x^3 + ax + b")
plt.plot(x, y_negative, 'b')

# Scatter plot of generated points
elliptic_points = list(points.keys())
elliptic_x, elliptic_y = zip(*elliptic_points)
plt.scatter(elliptic_x, elliptic_y, color='green', label="Points on curve")

# Highlight the generator and scalar multiple
plt.scatter(*G, color='red', label="Generator G")
plt.scatter(*kG_point, color='purple', label=f"{k} * G")

# Add labels and legend
plt.title("Elliptic Curve over Finite Field")
plt.xlabel("x")
plt.ylabel("y")
plt.axhline(0, color="black", linewidth=0.5)
plt.axvline(0, color="black", linewidth=0.5)
plt.grid()
plt.legend()
plt.show()

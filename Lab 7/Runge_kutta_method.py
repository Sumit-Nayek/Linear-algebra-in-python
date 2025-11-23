import matplotlib.pyplot as plt

def runge_kutta_2nd(f, x0, y0, h, steps):
    x, y = x0, y0
    results = [(x, y)]

    for i in range(steps):
        k1 = h * f(x, y)
        k2 = h * f(x + h, y + k1)
        y = y + 0.5 * (k1 + k2)
        x = x + h
        results.append((x, y))
        
    return results

print("Runge-Kutta 2nd Order Method")
print("Enter the function f(x, y) for dy/dx = f(x, y)")
f_expr = input("Example: x + y - 2\nf(x, y): ")
f = lambda x, y: eval(f_expr)

x0 = float(input("Enter initial x (x0): "))
y0 = float(input("Enter initial y (y0): "))
h = float(input("Enter step size (h): "))
steps = int(input("Enter number of steps: "))

results = runge_kutta_2nd(f, x0, y0, h, steps)

print("\n--- Results ---")
for (x, y) in results:
    print(f"x={x:.4f}, y={y:.4f}")

x_val, y_val = results[-1]
print(f"\nFinal value: y({x_val:.4f}) ≈ {y_val:.6f}")

x_vals = [p[0] for p in results]
y_vals = [p[1] for p in results]

plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, 'bo-', label="RK2 Solution")
plt.xlabel("x")
plt.ylabel("y")
plt.title(f"RK2 for dy/dx = {f_expr}")
plt.grid(True)
plt.legend()
plt.show()
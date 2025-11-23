def gauss_quadrature(f, a, b, n):
    points_weights = {
        2: [(-0.57735, 1.0), (0.57735, 1.0)],
        3: [(-0.77460, 0.55556), (0, 0.88889), (0.77460, 0.55556)],
        4: [(-0.86114, 0.34785), (-0.33998, 0.65215), 
             (0.33998, 0.65215), (0.86114, 0.34785)]
    }
    
    if n not in points_weights:
        print(f"n={n} not supported. Using n=2")
        n = 2
    
    gauss_points, weights = zip(*points_weights[n])
    
    result = 0
    for i in range(n):
        x = 0.5 * (b - a) * gauss_points[i] + 0.5 * (a + b)
        result += weights[i] * f(x)
    
    return 0.5 * (b - a) * result


func_str = input("Enter the function f(x) (e.g., x**2 - 4): ")
f = lambda x: eval(func_str)

a = float(input("Enter 'a' : "))
b = float(input("Enter 'b' : "))
n = int(input("Enter value of n:"))

result = gauss_quadrature(f, a, b, n)
print(f"∫x² dx from {a} to {b} = {result}")

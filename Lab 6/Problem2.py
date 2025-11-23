def false_position(f, a, b, max_iter=100, tol=1e-6):
    for i in range(max_iter):
        fa = f(a)
        fb = f(b)
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        
        if abs(fc) < tol:
            return c
        
        if fa * fc < 0:
            b = c
        else:
            a = c
    
    return c

func_str = input("Enter the function f(x) (e.g., x**2 - 4): ")
f = lambda x: eval(func_str)

a = float(input("Enter 'a' (lower bound of interval where root lies): "))
b = float(input("Enter 'b' (upper bound of interval where root lies): "))

root = false_position(f, a, b)
print(f"Root: {root}")
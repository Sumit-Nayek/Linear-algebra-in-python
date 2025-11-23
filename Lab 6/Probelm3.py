def newton_raphson(f, df, x0, max_iter=100, tol=1e-6):
    for i in range(max_iter):
        fx = f(x0)
        dfx = df(x0)
        
        if abs(dfx) < tol:
            print("Derivative too small. Method may not converge.")
            return None
            
        x1 = x0 - fx / dfx
        
        if abs(x1 - x0) < tol:
            return x1
            
        x0 = x1
    
    return x0

func_str = input("Enter the function f(x) (e.g., x**2 - 4): ")
f = lambda x: eval(func_str)

df_str = input("Enter the derivative f'(x) (e.g., 2*x): ")
df = lambda x: eval(df_str)

x0 = float(input("Enter initial guess x0: "))

root = newton_raphson(f, df, x0)
print(f"Root: {root}")
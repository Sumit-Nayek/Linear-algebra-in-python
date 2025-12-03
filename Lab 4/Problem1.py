import numpy as np

def solve_linear_equations():
    n = int(input("Enter number of equations/variables (n): "))  # Input number of equations/variables
    print("Enter the coefficients of matrix A row-wise:")
    A = []  # Input coefficient matrix A
    for i in range(n):
        row = list(map(float, input(f"Row {i+1}: ").split()))
        if len(row) != n:
            raise ValueError("Each row must have exactly n coefficients.")
        A.append(row)
    
    print("Enter the constants vector b:")
    b = []
    for i in range(n):
        val = float(input(f"b[{i+1}]: "))
        b.append(val)
    
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    try:
        x = np.linalg.solve(A, b)
        print("\nSolution vector x:")
        for i, val in enumerate(x, 1):
            print(f"x{i} = {val:.4f}")
    except np.linalg.LinAlgError as e:
        print("\nError:", e)

solve_linear_equations()  # Calling the function
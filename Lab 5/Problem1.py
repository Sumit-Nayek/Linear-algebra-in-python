# Minimal Gauss-Jacobi for 3 equations
def simple_jacobi(A, b):
    x = [0, 0, 0]  # Start with (0,0,0)
    
    for it in range(15):
        x_new = [0, 0, 0]
        
        # Update each variable
        for i in range(3):
            total = 0
            for j in range(3):
                if j != i:
                    total += A[i][j] * x[j]
            x_new[i] = (b[i] - total) / A[i][i]
        
        print(f"Iter {it+1}: {[round(v,3) for v in x_new]}")
        x = x_new
    
    return x

# Test the function
A = [[4, 1, 1],
     [1, 5, 2],
     [1, 2, 4]]
b = [7, 8, 9]

result = simple_jacobi(A, b)
print(f"\nSolution: x = {result}")
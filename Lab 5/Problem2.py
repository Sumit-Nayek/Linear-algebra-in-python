def gauss_seidel(A, b, max_iter):
    n = len(A)
    x = [0] * n
    
    for it in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            total = 0
            for j in range(n):
                if j != i:
                    total += A[i][j] * x_new[j]
            x_new[i] = (b[i] - total) / A[i][i]
        print(f"Iter {it+1}: {[round(v,6) for v in x_new]}")
        x = x_new
    
    return x

# User input
n = int(input("Enter number of equations: "))
A = []
print("Enter matrix A row-wise:")
for i in range(n):
    row = list(map(float, input().split()))
    A.append(row)

b = list(map(float, input("Enter vector b: ").split()))
max_iter = int(input("Enter max iterations: "))

result = gauss_seidel(A, b, max_iter)
print(f"Final solution: {[round(v,6) for v in result]}")
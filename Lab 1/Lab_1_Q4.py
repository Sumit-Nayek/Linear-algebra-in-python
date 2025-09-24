#Q4.
# Function to check if a matrix is symmetric
def is_symmetric(matrix, n):
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

# Function to get cofactor of matrix
def get_cofactor(mat, p, q, n):
    temp = []
    for i in range(n):
        if i != p:
            row = []
            for j in range(n):
                if j != q:
                    row.append(mat[i][j])
            temp.append(row)
    return temp

# Function to calculate determinant
def determinant(mat, n):
    if n == 1:
        return mat[0][0]
    det = 0
    sign = 1
    for f in range(n):
        temp = get_cofactor(mat, 0, f, n)
        det += sign * mat[0][f] * determinant(temp, n-1)
        sign = -sign
    return det

# Function to calculate adjoint
def adjoint(mat, n):
    if n == 1:
        return [[1]]
    adj = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            temp = get_cofactor(mat, i, j, n)
            sign = 1 if (i+j) % 2 == 0 else -1
            adj[j][i] = sign * determinant(temp, n-1)  # transpose while assigning
    return adj

# Function to calculate inverse
def inverse(mat, n):
    det = determinant(mat, n)
    if det == 0:
        return None
    adj = adjoint(mat, n)
    inv = [[adj[i][j] / det for j in range(n)] for i in range(n)]
    return inv

# MAIN PROGRAM
n = int(input("Enter order of square matrix (n): "))
print("Enter matrix elements row by row:")
A = []
for i in range(n):
    row = list(map(int, input().split()))
    A.append(row)

# a. Symmetry check
if is_symmetric(A, n):
    print("\nMatrix A is Symmetric.")
else:
    print("\nMatrix A is NOT Symmetric.")

# b. Adjoint and Inverse
adj = adjoint(A, n)
print("\nAdjoint of Matrix A:")
for row in adj:
    print(row)

inv = inverse(A, n)
if inv:
    print("\nInverse of Matrix A:")
    for row in inv:
        print(row)
else:
    print("\nMatrix is Singular, Inverse does not exist.")

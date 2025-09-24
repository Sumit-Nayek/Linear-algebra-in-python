# Q2. Write a Python Program to find the inverse of a n*n matrix - Using adjoint method.
# Function to get minor of element (i,j)
def get_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]
    # Function to calculate determinant
    def determinant(matrix):
    n = len(matrix)
    if n == 1:
    return matrix[0][0]
    if n == 2:
    return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for col in range(n):
    det += ((-1) ** col) * matrix[0][col] * determinant(get_minor(matrix, 0, col))
    return det
# Function to compute cofactor matrix
def cofactor_matrix(matrix):
    n = len(matrix)
    cofactors = []
    for i in range(n):
    cofactor_row = []
    for j in range(n):
    minor = get_minor(matrix, i, j)

    cofactor_row.append(((-1) ** (i+j)) * determinant(minor))
    cofactors.append(cofactor_row)
    return cofactors
# Function to transpose matrix
def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix))]
# Function to compute inverse
def inverse_matrix(matrix):
    det = determinant(matrix)
    if det == 0:
    raise ValueError("Matrix is singular! No inverse exists.")
    cofactors = cofactor_matrix(matrix)
    adjoint = transpose(cofactors)
    n = len(matrix)
    # Divide adjoint by determinant
    inverse = []
    for i in range(n):
    row = []
    for j in range(n):
    row.append(adjoint[i][j] / det)
    inverse.append(row)
    return inverse
# Example
A = [[2, 1, 3],
[1, 2, 2],
[3, 2, 4]]
print("Matrix A:")
for row in A:
    print(row)
print("\nDeterminant of A:", determinant(A))
print("\nInverse of A:")
inv = inverse_matrix(A)
for row in inv:
    print(row)
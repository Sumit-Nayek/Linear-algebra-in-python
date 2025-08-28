#Q3. Write a python program to read a square matrix(n*n) where all the elements are string. hence find the transpose of this matrix.

# Step 1: Take size of square matrix
n = int(input("Enter the size of the square matrix (n): "))

# Step 2: Read the matrix with string elements
matrix = []
print("Enter the elements row by row:")
for i in range(n):
    row = []
    for j in range(n):
        val = input(f"Enter element at position ({i},{j}): ")
        row.append(val)
    matrix.append(row)

# Step 3: Find the transpose
transpose = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(matrix[j][i])  # Swap row and column
    transpose.append(row)

# Step 4: Print result
print("\nOriginal Matrix:") ## To get a matrix looking output for loop used 
for row in matrix:
    print(row)

print("\nTranspose of the Matrix:")
for row in transpose:
    print(row)

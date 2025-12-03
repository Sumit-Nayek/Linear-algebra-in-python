import numpy as np

def matrix_rank():
    # Input number of rows and columns
    m, n = map(int, input("Enter number of rows and columns (m n): ").split())
    
    # Input matrix row-wise
    print("Enter the matrix row-wise:")
    A = []
    for i in range(m):
        row = list(map(float, input(f"Row {i+1}: ").split()))
        if len(row) != n:
            raise ValueError("Each row must have exactly n elements.")
        A.append(row)
    
    # Convert to numpy array
    A = np.array(A, dtype=float)
    
    # Find rank using numpy's linear algebra module
    rank = np.linalg.matrix_rank(A)
    
    # Display result
    print("\nRank of the matrix:", rank)

# Run program
matrix_rank()
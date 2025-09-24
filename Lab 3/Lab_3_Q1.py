# Write a Python Program in order to find the largest eigenvalue of a 3*3 matrix. Hence find corresponding eigenvector to largest eigenvalue. Assume the variation constant is 1.
import math
def determinant_3x3(M):
    a11,a12,a13 = M[0]
    a21,a22,a23 = M[1]
    a31,a32,a33 = M[2]
    return (a11*(a22*a33 - a23*a32)
    -a12*(a21*a33 - a23*a31)
    +a13*(a21*a32 - a22*a31))
def characteristic_polynomial(A):
"""
Build |A - λI| and expand the determinant to get cubic in λ.
Returns coefficients [a,b,c,d] for a*λ^3 + b*λ^2 + c*λ + d = 0
"""
    λ = 1.0 # dummy for substitution
    # Build matrix (A - λI) symbolically with λ as variable
    def entry(i,j):
    if i==j:
    return f"({A[i][j]} - lam)"
    else:
    return f"({A[i][j]})"
# symbolic matrix in string form
    M = [[entry(i,j) for j in range(3)] for i in range(3)]
    print("Matrix (A - λI):")
    for row in M:
        print(row)
    #Now expand determinant traditionally:
    a = f"({A[0][0]} - lam)"; b = f"({A[0][1]})"; c = f"({A[0][2]})"
    d = f"({A[1][0]})"; e = f"({A[1][1]} - lam)"; f = f"({A[1][2]})"
    g = f"({A[2][0]})"; h = f"({A[2][1]})"; i = f"({A[2][2]} - lam)"

    det_exp = f"{a}*({e}*{i} - {f}*{h}) - {b}*({d}*{i} - {f}*{g}) + {c}*({d}*{h} - {e}*{g})"
    print("\nCharacteristic polynomial |A - λI| =")
    print(det_exp, " = 0")
    return det_exp
# Example usage:
A = [
[2, 1, 0],
[1, 3, 1],
[0, 1, 2]
]
char_poly = characteristic_polynomial(A)

## Solving the same quesn using different approach
import numpy as np
# Example 3x3 matrix
A = np.array([
[2, 1, 0],
[1, 3, 1],
[0, 1, 2]
], dtype=float)
# Eigenvalues and eigenvectors using NumPy
eigenvalues, eigenvectors = np.linalg.eig(A)
print("All Eigenvalues:")
print(eigenvalues)
# Find the largest eigenvalue
largest_index = np.argmax(eigenvalues.real) # take the index of max real part
largest_eigenvalue = eigenvalues[largest_index].real
print("\nLargest Eigenvalue:", largest_eigenvalue)
# Corresponding eigenvector
largest_eigenvector = eigenvectors[:, largest_index].real
# Normalize for clarity
largest_eigenvector = largest_eigenvector / np.linalg.norm(largest_eigenvector)

print("\nCorresponding Eigenvector (normalized):")
print(largest_eigenvector)
### Power method application
### Use the power method and write a complete python program to find the dominant eigen value of a n by n square matrix. Input will be flexible to the user input and error tolarance and final output will be dominant egen value and egien vector
import numpy as np
import streamlit as st

def power_method(A, tol=1e-6, max_iter=1):
    n = A.shape[0]
    x = np.ones(n)
    eigenvalue_old = 0

    for i in range(max_iter):
        x_new = np.dot(A, x)
        eigenvalue_new = np.max(x_new)
        x_new = x_new / eigenvalue_new
        
        if abs(eigenvalue_new - eigenvalue_old) < tol:
            break

        x = x_new
        eigenvalue_old = eigenvalue_new

    return eigenvalue_new, x_new, i+1


# ------------- STREAMLIT UI --------------

st.title("Power Method - Dominant Eigen Value Finder")

n = st.number_input("Enter matrix order (n x n)", min_value=2, max_value=20, value=3, step=1)

st.write("Enter the matrix values row-wise")

matrix = []
for i in range(n):
    cols = st.columns(n)
    row = []
    for j in range(n):
        val = cols[j].number_input(f"R{i+1}C{j+1}", value=0, key=f"{i}{j}")
        row.append(val)
    matrix.append(row)

A = np.array(matrix)

tol = st.number_input("Tolerance", value=1e-6, format="%.7f")
max_iter = st.number_input("Max Iterations", min_value=1, value=10, step=1)

if st.button("Compute Dominant Eigen"):
    eigenvalue, eigenvector, iterations = power_method(A, tol, max_iter)
    st.success("✅ Computation Successful!")
    st.write("### 🔹 Results")
    st.write(f"**Dominant Eigen Value:** `{eigenvalue:.6f}`")
    st.write(f"**Eigen Vector:** `{eigenvector}`")
    st.write(f"**Iterations Taken:** `{iterations}`")

    

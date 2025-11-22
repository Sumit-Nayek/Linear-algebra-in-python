import streamlit as st

def simple_jacobi(A, b, max_iter):
    n = len(A)
    x = [0] * n
    
    results = []
    for it in range(max_iter):
        x_new = [0] * n
        for i in range(n):
            total = 0
            for j in range(n):
                if j != i:
                    total += A[i][j] * x[j]
            x_new[i] = (b[i] - total) / A[i][i]
        results.append(x_new.copy())
        x = x_new
    
    return results

def gauss_seidel(A, b, max_iter):
    n = len(A)
    x = [0] * n
    
    results = []
    for it in range(max_iter):
        x_new = x.copy()
        for i in range(n):
            total = 0
            for j in range(n):
                if j != i:
                    total += A[i][j] * x_new[j]
            x_new[i] = (b[i] - total) / A[i][i]
        results.append(x_new.copy())
        x = x_new
    
    return results

st.title("Linear Equation Solver")

method = st.selectbox("Select Method", 
                     ["Gauss-Jacobi Method", "Gauss-Seidel Method"])

n = st.number_input("Number of equations", min_value=2, max_value=10, value=3)

st.subheader("Enter Matrix A (row-wise)")
A = []
for i in range(n):
    cols = st.columns(n)
    row = []
    for j in range(n):
        with cols[j]:
            row.append(st.number_input(f"A[{i+1},{j+1}]", value=0.0, key=f"A_{i}_{j}"))
    A.append(row)

st.subheader("Enter Vector b")
b = []
cols = st.columns(n)
for i in range(n):
    with cols[i]:
        b.append(st.number_input(f"b[{i+1}]", value=0.0, key=f"b_{i}"))

max_iter = st.number_input("Maximum iterations", min_value=1, max_value=100, value=10)

if st.button("Compute Solution"):
    if method == "Gauss-Jacobi Method":
        results = simple_jacobi(A, b, max_iter)
    else:
        results = gauss_seidel(A, b, max_iter)
    
    st.subheader("Results")
    for i, result in enumerate(results):
        st.write(f"Iteration {i+1}: {[round(val, 6) for val in result]}")
    
    st.subheader("Final Solution")
    final_solution = [round(val, 6) for val in results[-1]]
    st.write(f"x = {final_solution}")
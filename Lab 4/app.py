import streamlit as st
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Math Problem Solver",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
    }
    .problem-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .result-box {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-top: 1rem;
    }
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧮 Math Problem Solver</h1>', unsafe_allow_html=True)

# Sidebar for problem selection
with st.sidebar:
    st.markdown("### 📚 Problem Selection")
    problem_choice = st.selectbox(
        "Choose a problem to solve:",
        ["Linear Equations Solver", "Significant Digits & Rounding", "Matrix Rank Calculator"]
    )
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    This app solves three mathematical problems:
    1. **Linear Equations** - Solve system of equations
    2. **Significant Digits** - Count significant digits & round numbers
    3. **Matrix Rank** - Calculate matrix rank
    """)

# Main content area
st.markdown(f'<h2 class="problem-header">{problem_choice}</h2>', unsafe_allow_html=True)

# Problem 1: Linear Equations Solver
if problem_choice == "Linear Equations Solver":
    st.write("Solve a system of linear equations: **Ax = b**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        n = st.number_input(
            "Number of equations/variables (n):",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
            help="Maximum 10 equations for better performance"
        )
    
    with col2:
        st.write("Example input format for coefficients:")
        st.code("1 2 3\n4 5 6\n7 8 9", language="text")
    
    st.subheader("Enter Coefficients Matrix A")
    A_matrix = []
    
    # Create a grid for matrix A input
    cols = st.columns(n)
    for i in range(int(n)):
        with cols[i % len(cols)]:
            row_input = st.text_input(
                f"Row {i+1} of A:",
                value=" ".join(["1" if i==j else "0" for j in range(int(n))]),
                key=f"A_row_{i}",
                help=f"Enter {n} space-separated coefficients for row {i+1}"
            )
            try:
                row = list(map(float, row_input.split()))
                if len(row) != n:
                    st.warning(f"Row {i+1} should have {n} elements")
                else:
                    A_matrix.append(row)
            except:
                st.warning("Please enter valid numbers")
    
    st.subheader("Enter Constants Vector b")
    b_vector = []
    
    cols = st.columns(n)
    for i in range(int(n)):
        with cols[i % len(cols)]:
            b_val = st.number_input(
                f"b[{i+1}]:",
                value=float(i+1),
                key=f"b_{i}",
                format="%.4f"
            )
            b_vector.append(b_val)
    
    if st.button("Solve Linear Equations", type="primary"):
        if len(A_matrix) == n and len(b_vector) == n:
            try:
                A = np.array(A_matrix, dtype=float)
                b = np.array(b_vector, dtype=float)
                
                # Display the system
                st.subheader("System of Equations")
                eq_text = ""
                for i in range(n):
                    terms = [f"{A[i,j]:.2f}x{j+1}" for j in range(n)]
                    eq_text += f"Equation {i+1}: " + " + ".join(terms) + f" = {b[i]:.2f}\n"
                st.text(eq_text)
                
                # Solve the system
                x = np.linalg.solve(A, b)
                
                # Display results
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.success("✅ Solution Found!")
                st.subheader("Solution Vector x:")
                for i, val in enumerate(x, 1):
                    st.write(f"**x{i}** = {val:.6f}")
                
                # Verification
                st.subheader("Verification")
                verification = np.dot(A, x)
                for i in range(n):
                    st.write(f"Equation {i+1}: LHS = {verification[i]:.6f}, RHS = {b[i]:.6f}")
                st.markdown('</div>', unsafe_allow_html=True)
                
            except np.linalg.LinAlgError as e:
                st.error(f"❌ Cannot solve: {e}")
                st.info("The matrix might be singular or the system might have no unique solution.")
        else:
            st.error("Please fill all the required fields correctly.")

# Problem 2: Significant Digits & Rounding
elif problem_choice == "Significant Digits & Rounding":
    st.write("Calculate significant digits and round a number to k decimal places")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_str = st.text_input(
            "Enter a real number:",
            value="0.0045600",
            help="Examples: 0.0045600, 123.4500, -0.00123"
        )
    
    with col2:
        k = st.number_input(
            "Enter value of k (decimal places):",
            min_value=0,
            max_value=10,
            value=3,
            step=1,
            help="Number of decimal places to round to"
        )
    
    # Define the functions
    def count_significant_digits(num_str):
        original_num_str = num_str
        if num_str.startswith(("-", "+")):
            num_str = num_str[1:]
        num_str = num_str.lstrip("0")
        
        if "." in num_str:
            parts = num_str.split(".")
            if len(parts) == 2:
                integer_part, decimal_part = parts
                decimal_part = decimal_part.rstrip("0")
                sig_str = integer_part + decimal_part
            else:
                sig_str = num_str
        else:
            sig_str = num_str.rstrip("0")
        return len(sig_str)
    
    def custom_round(num, k):
        factor = 10 ** k
        shifted = num * factor
        
        if shifted >= 0:
            rounded = int(shifted + 0.5)
        else:
            rounded = int(shifted - 0.5)
        return rounded / factor
    
    if st.button("Calculate Significant Digits & Round", type="primary"):
        if num_str:
            try:
                num = float(num_str)
                sig_digits = count_significant_digits(num_str)
                rounded_num = custom_round(num, int(k))
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        label="Significant Digits",
                        value=sig_digits,
                        help=f"Counted from: {num_str}"
                    )
                
                with col2:
                    st.metric(
                        label=f"Rounded to {k} places",
                        value=f"{rounded_num:.{int(k)}f}",
                        help=f"Original: {num}"
                    )
                
                # Detailed breakdown
                with st.expander("Show Detailed Analysis"):
                    st.write(f"**Original number:** {num_str}")
                    st.write(f"**Numeric value:** {num}")
                    st.write(f"**Number of significant digits:** {sig_digits}")
                    st.write(f"**Rounded to {k} decimal places:** {rounded_num}")
                    st.write(f"**Rounded value (full precision):** {rounded_num}")
                    
                    # Show rounding process
                    st.write("\n**Rounding Process:**")
                    factor = 10 ** int(k)
                    shifted = num * factor
                    st.write(f"1. Multiply by 10^{k}: {num} × {factor} = {shifted}")
                    if shifted >= 0:
                        st.write(f"2. Add 0.5: {shifted} + 0.5 = {shifted + 0.5}")
                        st.write(f"3. Take integer part: {int(shifted + 0.5)}")
                    else:
                        st.write(f"2. Subtract 0.5: {shifted} - 0.5 = {shifted - 0.5}")
                        st.write(f"3. Take integer part: {int(shifted - 0.5)}")
                    st.write(f"4. Divide by 10^{k}: {rounded_num}")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except ValueError:
                st.error("❌ Please enter a valid number")
        else:
            st.warning("Please enter a number")

# Problem 3: Matrix Rank Calculator
elif problem_choice == "Matrix Rank Calculator":
    st.write("Calculate the rank of a matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        m = st.number_input(
            "Number of rows (m):",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )
    
    with col2:
        n = st.number_input(
            "Number of columns (n):",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )
    
    st.subheader("Enter Matrix Elements")
    
    matrix_input_method = st.radio(
        "Choose input method:",
        ["Manual Entry (Grid)", "Row-wise Text Input"]
    )
    
    matrix = []
    
    if matrix_input_method == "Manual Entry (Grid)":
        st.write(f"Enter values for {int(m)}×{int(n)} matrix:")
        
        # Create a grid of number inputs
        for i in range(int(m)):
            cols = st.columns(int(n))
            row = []
            for j in range(int(n)):
                with cols[j]:
                    val = st.number_input(
                        f"A[{i+1},{j+1}]",
                        value=float(i * int(n) + j + 1),
                        key=f"mat_{i}_{j}",
                        format="%.4f"
                    )
                    row.append(val)
            matrix.append(row)
    
    else:  # Row-wise Text Input
        st.write(f"Enter {int(m)} rows, each with {int(n)} space-separated numbers:")
        
        for i in range(int(m)):
            row_input = st.text_input(
                f"Row {i+1}:",
                value=" ".join([str(i * int(n) + j + 1) for j in range(int(n))]),
                key=f"row_{i}"
            )
            try:
                row = list(map(float, row_input.split()))
                if len(row) == n:
                    matrix.append(row)
                else:
                    st.warning(f"Row {i+1} should have {n} elements")
            except:
                st.warning("Please enter valid numbers")
    
    if st.button("Calculate Matrix Rank", type="primary"):
        if len(matrix) == m:
            try:
                A = np.array(matrix, dtype=float)
                
                # Display the matrix
                st.subheader("Input Matrix")
                st.write(A)
                
                # Calculate rank
                rank = np.linalg.matrix_rank(A)
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Matrix Rank", rank)
                
                with col2:
                    st.metric("Shape", f"{int(m)}×{int(n)}")
                
                with col3:
                    if m == n:
                        det = np.linalg.det(A)
                        st.metric("Determinant", f"{det:.6f}")
                    else:
                        st.metric("Determinant", "N/A")
                
                # Additional information
                with st.expander("Show Detailed Analysis"):
                    st.write(f"**Rank:** {rank}")
                    st.write(f"**Shape:** ({int(m)}, {int(n)})")
                    st.write(f"**Full rank?:** {'Yes' if rank == min(m, n) else 'No'}")
                    
                    if m == n:
                        st.write(f"**Determinant:** {np.linalg.det(A):.6f}")
                        st.write(f"**Is singular?:** {'Yes' if np.abs(np.linalg.det(A)) < 1e-10 else 'No'}")
                    
                    # Calculate and show row echelon form
                    st.write("\n**Row Echelon Form:**")
                    try:
                        from scipy import linalg
                        U = linalg.lu(A)[2]  # Get upper triangular matrix from LU decomposition
                        st.write(U)
                    except:
                        st.write("Cannot compute row echelon form")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error calculating rank: {e}")
        else:
            st.error("Please complete the matrix input")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6B7280;'>
    Created with ❤️ using Streamlit | Math Problem Solver
    </div>
    """,
    unsafe_allow_html=True
)
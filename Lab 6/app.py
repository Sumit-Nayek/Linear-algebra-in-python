import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from math import *

st.set_page_config(page_title="Numerical Methods Calculator", layout="wide")

st.title("🔢 Numerical Methods Calculator")
st.markdown("---")

# Initialize session state for function persistence
if 'function_string' not in st.session_state:
    st.session_state.function_string = "x**2 - 4"
if 'results' not in st.session_state:
    st.session_state.results = {}

# Sidebar for method selection
method = st.sidebar.selectbox(
    "Select Numerical Method",
    ["Gauss Quadrature (3 points)", "False Position Method", "Newton-Raphson Method"]
)

# Main input section
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Function Input")
    function_input = st.text_input(
        "Enter f(x) (use Python math syntax):",
        value=st.session_state.function_string,
        help="Examples: x**2 + 2*x + 1, sin(x) + cos(x), exp(x) - 2"
    )
    
    # Update session state
    st.session_state.function_string = function_input

with col2:
    st.subheader("Method Information")
    if method == "Gauss Quadrature (3 points)":
        st.info("""
        **Gauss Quadrature (3 points):**
        - Numerical integration method
        - Highly accurate for polynomial functions
        - Uses 3 specific points with optimized weights
        """)
    elif method == "False Position Method":
        st.info("""
        **False Position Method:**
        - Root-finding method
        - Combines bisection and secant methods
        - Requires two initial guesses with opposite signs
        """)
    else:
        st.info("""
        **Newton-Raphson Method:**
        - Fast root-finding method
        - Requires function derivative
        - Needs one initial guess
        - May not converge for some functions
        """)

# Function parser with error handling
def parse_function(func_str, x_val):
    """Safely evaluate the mathematical function"""
    try:
        # Create a safe environment for eval
        safe_dict = {
            'x': x_val,
            'sin': sin, 'cos': cos, 'tan': tan,
            'asin': asin, 'acos': acos, 'atan': atan,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
            'exp': exp, 'log': log, 'log10': log10,
            'sqrt': sqrt, 'pi': pi, 'e': exp(1),
            'abs': abs, 'pow': pow
        }
        return eval(func_str, {"__builtins__": {}}, safe_dict)
    except:
        return None

# Numerical Methods Implementations
def gauss_quadrature_3point(func_str, a, b):
    """Gauss Quadrature with 3 points"""
    # Gauss points and weights for 3 points
    points = [-np.sqrt(3/5), 0, np.sqrt(3/5)]
    weights = [5/9, 8/9, 5/9]
    
    # Transform from [-1,1] to [a,b]
    def transform(t):
        return (b - a) / 2 * t + (a + b) / 2
    
    integral = 0
    for i in range(3):
        x_transformed = transform(points[i])
        fx = parse_function(func_str, x_transformed)
        if fx is None:
            return None, "Error evaluating function"
        integral += weights[i] * fx
    
    integral *= (b - a) / 2
    return integral, None

def false_position_method(func_str, x0, x1, tol=1e-6, max_iter=100):
    """False Position Method implementation"""
    iterations = []
    
    f0 = parse_function(func_str, x0)
    f1 = parse_function(func_str, x1)
    
    if f0 is None or f1 is None:
        return None, "Error evaluating function at initial points"
    
    if f0 * f1 > 0:
        return None, "Initial guesses must have opposite signs"
    
    for i in range(max_iter):
        x2 = (x0 * f1 - x1 * f0) / (f1 - f0)
        f2 = parse_function(func_str, x2)
        
        if f2 is None:
            return None, "Error evaluating function during iteration"
        
        iterations.append({
            'iteration': i + 1,
            'x0': x0, 'x1': x1, 'x2': x2,
            'f0': f0, 'f1': f1, 'f2': f2
        })
        
        if abs(f2) < tol:
            return {'root': x2, 'iterations': iterations, 'converged': True}, None
        
        if f0 * f2 < 0:
            x1, f1 = x2, f2
        else:
            x0, f0 = x2, f2
    
    return {'root': x2, 'iterations': iterations, 'converged': False}, "Maximum iterations reached"

def newton_raphson_method(func_str, x0, tol=1e-6, max_iter=100):
    """Newton-Raphson Method implementation"""
    iterations = []
    
    # Numerical derivative
    def derivative(f_str, x, h=1e-6):
        f_plus = parse_function(f_str, x + h)
        f_minus = parse_function(f_str, x - h)
        if f_plus is None or f_minus is None:
            return None
        return (f_plus - f_minus) / (2 * h)
    
    for i in range(max_iter):
        fx = parse_function(func_str, x0)
        if fx is None:
            return None, "Error evaluating function"
        
        f_prime = derivative(func_str, x0)
        if f_prime is None or f_prime == 0:
            return None, "Derivative is zero or cannot be computed"
        
        x1 = x0 - fx / f_prime
        fx1 = parse_function(func_str, x1)
        
        if fx1 is None:
            return None, "Error evaluating function at new point"
        
        iterations.append({
            'iteration': i + 1,
            'x0': x0, 'x1': x1,
            'f(x0)': fx, 'f(x1)': fx1,
            'f_prime': f_prime
        })
        
        if abs(fx1) < tol:
            return {'root': x1, 'iterations': iterations, 'converged': True}, None
        
        x0 = x1
    
    return {'root': x1, 'iterations': iterations, 'converged': False}, "Maximum iterations reached"

# Method-specific input parameters
st.subheader("Method Parameters")

if method == "Gauss Quadrature (3 points)":
    col_a, col_b = st.columns(2)
    with col_a:
        a = st.number_input("Lower limit (a):", value=0.0, format="%.6f")
    with col_b:
        b = st.number_input("Upper limit (b):", value=2.0, format="%.6f")
    
    parameters = f"a = {a}, b = {b}"

elif method == "False Position Method":
    col_x0, col_x1 = st.columns(2)
    with col_x0:
        x0 = st.number_input("First guess (x0):", value=1.0, format="%.6f")
    with col_x1:
        x1 = st.number_input("Second guess (x1):", value=3.0, format="%.6f")
    
    parameters = f"x0 = {x0}, x1 = {x1}"

else:  # Newton-Raphson Method
    x0 = st.number_input("Initial guess (x0):", value=2.0, format="%.6f")
    parameters = f"x0 = {x0}"

# Calculate button
if st.button("🚀 Calculate", type="primary"):
    if not function_input:
        st.error("Please enter a function")
    else:
        with st.spinner("Computing..."):
            # Test function parsing
            test_result = parse_function(function_input, 1.0)
            if test_result is None:
                st.error("Error parsing function. Please check your syntax.")
            else:
                # Execute selected method
                if method == "Gauss Quadrature (3 points)":
                    result, error = gauss_quadrature_3point(function_input, a, b)
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.session_state.results[method] = {
                            'result': result,
                            'parameters': parameters,
                            'function': function_input
                        }
                        
                elif method == "False Position Method":
                    result, error = false_position_method(function_input, x0, x1)
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.session_state.results[method] = {
                            'result': result,
                            'parameters': parameters,
                            'function': function_input
                        }
                        
                else:  # Newton-Raphson
                    result, error = newton_raphson_method(function_input, x0)
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.session_state.results[method] = {
                            'result': result,
                            'parameters': parameters,
                            'function': function_input
                        }

# Display results
if method in st.session_state.results:
    st.subheader("📊 Results")
    result_data = st.session_state.results[method]
    
    if method == "Gauss Quadrature (3 points)":
        st.success(f"**Integral Value:** {result_data['result']:.8f}")
        st.latex(fr"\int_{{{a}}}^{{{b}}} {function_input} \, dx \approx {result_data['result']:.6f}")
        
    else:  # Root-finding methods
        root_result = result_data['result']
        if root_result['converged']:
            st.success(f"**Root Found:** {root_result['root']:.8f}")
            st.latex(fr"f({root_result['root']:.6f}) = 0")
        else:
            st.warning(f"**Approximate Root:** {root_result['root']:.8f} (Did not fully converge)")
        
        # Display iteration table
        if root_result['iterations']:
            st.subheader("Iteration Details")
            iterations_df = []
            for iter_data in root_result['iterations'][:10]:  # Show first 10 iterations
                if method == "False Position Method":
                    iterations_df.append({
                        'Iteration': iter_data['iteration'],
                        'x0': f"{iter_data['x0']:.6f}",
                        'x1': f"{iter_data['x1']:.6f}",
                        'x2': f"{iter_data['x2']:.6f}",
                        'f(x2)': f"{iter_data['f2']:.2e}"
                    })
                else:  # Newton-Raphson
                    iterations_df.append({
                        'Iteration': iter_data['iteration'],
                        'x_n': f"{iter_data['x0']:.6f}",
                        'x_{n+1}': f"{iter_data['x1']:.6f}",
                        'f(x_n)': f"{iter_data['f(x0)']:.2e}",
                        "f'(x_n)": f"{iter_data['f_prime']:.2e}"
                    })
            
            st.dataframe(iterations_df, use_container_width=True)
            
            if len(root_result['iterations']) > 10:
                st.info(f"Showing first 10 of {len(root_result['iterations'])} iterations")

# Plot the function
st.subheader("📈 Function Visualization")

plot_col1, plot_col2 = st.columns([2, 1])

with plot_col1:
    # Determine plot range based on method
    if method == "Gauss Quadrature (3 points)":
        x_min, x_max = a - 1, b + 1
    elif method in st.session_state.results:
        root_result = st.session_state.results[method]['result']
        if 'root' in root_result:
            root_val = root_result['root']
            x_min, x_max = root_val - 3, root_val + 3
        else:
            x_min, x_max = -5, 5
    else:
        x_min, x_max = -5, 5
    
    # Generate plot data
    x_vals = np.linspace(x_min, x_max, 400)
    y_vals = []
    valid_points = []
    
    for x in x_vals:
        y = parse_function(function_input, x)
        if y is not None and abs(y) < 1e6:  # Filter out extreme values
            y_vals.append(y)
            valid_points.append(x)
    
    if len(valid_points) > 1:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(valid_points, y_vals, 'b-', linewidth=2, label=f'f(x) = {function_input}')
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f'Function: {function_input}')
        ax.legend()
        
        # Highlight important points
        if method in st.session_state.results:
            result_data = st.session_state.results[method]
            if method == "Gauss Quadrature (3 points)":
                ax.axvline(x=a, color='r', linestyle='--', alpha=0.7, label=f'Lower limit (a={a})')
                ax.axvline(x=b, color='g', linestyle='--', alpha=0.7, label=f'Upper limit (b={b})')
                ax.fill_between(valid_points, y_vals, where=[(x >= a and x <= b) for x in valid_points], 
                              alpha=0.3, color='orange', label='Integration area')
                ax.legend()
            else:
                root_result = result_data['result']
                if 'root' in root_result:
                    root_x = root_result['root']
                    root_y = parse_function(function_input, root_x)
                    if root_y is not None:
                        ax.plot(root_x, root_y, 'ro', markersize=8, label=f'Root ({root_x:.4f})')
                        ax.legend()
        
        st.pyplot(fig)
    else:
        st.warning("Could not generate plot for the given function")

with plot_col2:
    st.subheader("ℹ️ Instructions")
    st.markdown("""
    1. **Enter your function** using Python math syntax
    2. **Select method** from dropdown
    3. **Set parameters** for the chosen method
    4. **Click Calculate** to see results
    5. **View visualization** of the function
    
    **Supported functions:**
    - Basic: +, -, *, /, **
    - Trig: sin, cos, tan, asin, acos, atan
    - Hyperbolic: sinh, cosh, tanh
    - Exponential: exp, log, log10
    - Constants: pi, e
    """)

# Footer
st.markdown("---")
st.markdown(
    "**Numerical Methods Calculator** | "
    "Gauss Quadrature • False Position • Newton-Raphson"
)
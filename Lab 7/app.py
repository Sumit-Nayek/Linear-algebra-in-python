import streamlit as st
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Numerical & Image Processing Tools", layout="wide")

st.title("🔧 Multi-Tool Application")
st.markdown("---")

# Initialize session state
if 'current_method' not in st.session_state:
    st.session_state.current_method = "Runge-Kutta 2nd Order Method"
if 'rk_results' not in st.session_state:
    st.session_state.rk_results = None
if 'image_processed' not in st.session_state:
    st.session_state.image_processed = False

# Sidebar for method selection
method = st.sidebar.selectbox(
    "Select Tool",
    ["Runge-Kutta 2nd Order Method", "Image to Text Converter"]
)

st.session_state.current_method = method

if method == "Runge-Kutta 2nd Order Method":
    st.header("📈 Runge-Kutta 2nd Order Method")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Parameters")
        
        # Function input
        st.markdown("**Enter the function f(x, y) for dy/dx = f(x, y)**")
        default_function = "x + y - 2"
        function_input = st.text_input(
            "f(x, y):",
            value=default_function,
            help="Examples: x + y, x**2 + y, sin(x) + cos(y)"
        )
        
        # Numerical parameters
        x0 = st.number_input("Initial x (x0):", value=0.0, format="%.6f")
        y0 = st.number_input("Initial y (y0):", value=1.0, format="%.6f")
        h = st.number_input("Step size (h):", value=0.1, format="%.6f", min_value=0.001)
        steps = st.number_input("Number of steps:", value=10, min_value=1, max_value=1000)
    
    with col2:
        st.subheader("Method Information")
        st.info("""
        **Runge-Kutta 2nd Order Method:**
        - Also known as the Improved Euler method
        - Numerical method for solving ODEs
        - More accurate than Euler's method
        - Formula: yₙ₊₁ = yₙ + 0.5*(k₁ + k₂)
        where:
          k₁ = h*f(xₙ, yₙ)
          k₂ = h*f(xₙ + h, yₙ + k₁)
        """)
        
        st.markdown("**Example Functions:**")
        examples = {
            "Simple Linear": "x + y",
            "Exponential": "y - x**2 + 1",
            "Trigonometric": "sin(x) + cos(y)",
            "Polynomial": "x**2 + y**2 - 1"
        }
        
        example_choice = st.selectbox("Try examples:", list(examples.keys()))
        if st.button("Load Example Function"):
            st.session_state.function_input = examples[example_choice]
            st.rerun()

    # Runge-Kutta implementation
    def runge_kutta_2nd(f, x0, y0, h, steps):
        x, y = x0, y0
        results = [(x, y)]

        for i in range(steps):
            k1 = h * f(x, y)
            k2 = h * f(x + h, y + k1)
            y = y + 0.5 * (k1 + k2)
            x = x + h
            results.append((x, y))
            
        return results

    # Calculate button for RK method
    if st.button("🚀 Solve ODE", type="primary", key="rk_button"):
        if not function_input:
            st.error("Please enter a function")
        else:
            try:
                # Create the function safely
                safe_dict = {
                    'x': 0, 'y': 0,
                    'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                    'exp': np.exp, 'log': np.log, 'sqrt': np.sqrt,
                    'pi': np.pi, 'e': np.e
                }
                
                # Test the function
                test_f = lambda x, y: eval(function_input, {"__builtins__": {}}, {**safe_dict, 'x': x, 'y': y})
                test_result = test_f(0, 0)
                
                # Run the method
                with st.spinner("Computing solution..."):
                    results = runge_kutta_2nd(test_f, x0, y0, h, steps)
                    st.session_state.rk_results = results
                    
            except Exception as e:
                st.error(f"Error in function: {str(e)}")

    # Display RK results
    if st.session_state.rk_results:
        st.subheader("📊 Results")
        results = st.session_state.rk_results
        
        # Display final value prominently
        x_final, y_final = results[-1]
        st.success(f"**Final value:** y({x_final:.4f}) ≈ {y_final:.6f}")
        
        # Display results table
        st.subheader("Iteration Details")
        results_data = []
        for i, (x, y) in enumerate(results):
            results_data.append({
                'Step': i,
                'x': f"{x:.6f}",
                'y': f"{y:.6f}"
            })
        
        st.dataframe(results_data, use_container_width=True)
        
        # Plot the results
        st.subheader("📈 Solution Plot")
        x_vals = [p[0] for p in results]
        y_vals = [p[1] for p in results]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, 'bo-', linewidth=2, markersize=4, label="RK2 Solution")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"Runge-Kutta 2nd Order Solution for dy/dx = {function_input}")
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)

else:  # Image to Text Converter
    st.header("🖼️ Image to Text Converter")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Image")
        
        uploaded_file = st.file_uploader(
            "Choose an image file", 
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Upload a JPG, PNG, or BMP image"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_column_width=True)
            
            # Resize options
            st.subheader("Processing Options")
            resize_option = st.selectbox(
                "Image size for processing:",
                ["32x32 (Fast)", "64x64 (Medium)", "128x128 (Slow)", "Keep original"]
            )
            
            if resize_option == "32x32 (Fast)":
                new_size = (32, 32)
            elif resize_option == "64x64 (Medium)":
                new_size = (64, 64)
            elif resize_option == "128x128 (Slow)":
                new_size = (128, 128)
            else:
                new_size = image.size
            
    with col2:
        st.subheader("Converter Information")
        st.info("""
        **Image to Text Converter:**
        - Converts image pixels to text format
        - Stores RGB values in a text file
        - Can reconstruct image from text data
        - Useful for image processing and analysis
        """)
        
        if uploaded_file is not None:
            st.subheader("Image Details")
            st.write(f"**Original size:** {image.size}")
            st.write(f"**Mode:** {image.mode}")
            st.write(f"**Format:** {uploaded_file.type}")
            
            if st.button("🔄 Convert Image to Text", type="primary", key="img_button"):
                with st.spinner("Processing image..."):
                    try:
                        # Process image
                        processed_img = image.resize(new_size)
                        img_array = np.array(processed_img)
                        
                        # Save to text file
                        if len(img_array.shape) == 3:  # Color image
                            np.savetxt("converted_pixels.txt", img_array.reshape(-1, img_array.shape[2]), fmt='%d')
                        else:  # Grayscale image
                            np.savetxt("converted_pixels.txt", img_array.reshape(-1, 1), fmt='%d')
                        
                        # Load back and reconstruct
                        if len(img_array.shape) == 3:
                            loaded_array = np.loadtxt("converted_pixels.txt", dtype=np.uint8)
                            loaded_array = loaded_array.reshape(img_array.shape)
                        else:
                            loaded_array = np.loadtxt("converted_pixels.txt", dtype=np.uint8)
                            loaded_array = loaded_array.reshape(img_array.shape)
                        
                        reconstructed_img = Image.fromarray(loaded_array)
                        reconstructed_img.save("reconstructed_image.jpg")
                        
                        st.session_state.image_processed = True
                        st.session_state.processed_data = {
                            'original': image,
                            'processed': processed_img,
                            'reconstructed': reconstructed_img,
                            'array_shape': img_array.shape,
                            'pixel_count': img_array.size
                        }
                        
                        st.success("✅ Conversion successful!")
                        
                    except Exception as e:
                        st.error(f"Error processing image: {str(e)}")

    # Display image processing results
    if st.session_state.get('image_processed', False):
        data = st.session_state.processed_data
        
        st.subheader("📋 Conversion Results")
        
        col_stats, col_download = st.columns([2, 1])
        
        with col_stats:
            st.write(f"**Processed size:** {data['processed'].size}")
            st.write(f"**Array shape:** {data['array_shape']}")
            st.write(f"**Total pixels:** {data['pixel_count']:,}")
            
            # Show sample of text data
            try:
                with open("converted_pixels.txt", "r") as f:
                    lines = f.readlines()[:10]  # First 10 lines
                st.subheader("Sample Text Data (First 10 lines):")
                st.code(''.join(lines), language='text')
            except:
                pass
        
        with col_download:
            st.subheader("📥 Download")
            
            # Download text file
            with open("converted_pixels.txt", "rb") as file:
                st.download_button(
                    label="📄 Download Text File",
                    data=file,
                    file_name="converted_pixels.txt",
                    mime="text/plain"
                )
            
            # Download reconstructed image
            with open("reconstructed_image.jpg", "rb") as file:
                st.download_button(
                    label="🖼️ Download Reconstructed Image",
                    data=file,
                    file_name="reconstructed_image.jpg",
                    mime="image/jpeg"
                )
        
        # Display comparison
        st.subheader("🔄 Before & After Comparison")
        comp_col1, comp_col2 = st.columns(2)
        
        with comp_col1:
            st.image(data['original'], caption="Original Image", use_column_width=True)
        
        with comp_col2:
            st.image(data['reconstructed'], caption="Reconstructed Image", use_column_width=True)

# Instructions section
st.markdown("---")
st.subheader("ℹ️ Instructions")

if method == "Runge-Kutta 2nd Order Method":
    st.markdown("""
    ### Runge-Kutta Method Instructions:
    1. **Enter your ODE** in the form dy/dx = f(x, y)
    2. **Set initial conditions** (x₀, y₀)
    3. **Choose step size** (h) and number of steps
    4. **Click 'Solve ODE'** to compute the solution
    5. **View results** in table and plot format
    
    **Function Syntax:**
    - Use `x` and `y` as variables
    - Supported: `+`, `-`, `*`, `/`, `**`
    - Functions: `sin(x)`, `cos(x)`, `exp(x)`, `log(x)`, `sqrt(x)`
    - Constants: `pi`, `e`
    """)
else:
    st.markdown("""
    ### Image Converter Instructions:
    1. **Upload an image** (JPG, PNG, BMP)
    2. **Choose processing size** based on your needs
    3. **Click 'Convert Image to Text'** to process
    4. **Download** the text file and reconstructed image
    5. **Compare** original vs reconstructed images
    
    **Features:**
    - Converts RGB pixel values to text format
    - Maintains image dimensions in output
    - Allows reconstruction from text data
    - Suitable for image processing applications
    """)

# Footer
st.markdown("---")
st.markdown(
    "**Multi-Tool Application** | "
    "Runge-Kutta Solver • Image Converter | "
    "Made with Streamlit"
)
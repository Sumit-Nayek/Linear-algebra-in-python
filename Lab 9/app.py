import streamlit as st
import numpy as np

st.set_page_config(page_title="Graph Analysis Tool", layout="wide")

st.title("🎯 Graph Analysis Tool")
st.markdown("---")

# Initialize session state
if 'current_method' not in st.session_state:
    st.session_state.current_method = "Adjacency Matrix"
if 'adj_matrix' not in st.session_state:
    st.session_state.adj_matrix = None
if 'vertices' not in st.session_state:
    st.session_state.vertices = 0
if 'edges' not in st.session_state:
    st.session_state.edges = []

# Method selection
method = st.selectbox(
    "Select Graph Operation",
    ["Adjacency Matrix", "Bipartite Check"],
    key="method_selector"
)

if method == "Adjacency Matrix":
    st.header("📊 Adjacency Matrix Creator")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Graph Input")
        
        # Input number of vertices
        num_vertices = st.number_input(
            "Number of vertices:",
            min_value=1,
            max_value=20,
            value=5,
            key="vertices_input",
            help="Enter the number of vertices in the graph (1-20)"
        )
        
        st.markdown("**Enter edges (0-indexed):**")
        st.info("Format: '0,1' for edge between vertex 0 and 1")
        
        # Input edges
        edges_input = st.text_area(
            "Edges (one per line):",
            value="0,1\n1,2\n2,3\n3,4\n0,4",
            height=150,
            key="edges_input",
            help="Enter edges as comma-separated pairs. Example:\n0,1\n1,2\n2,3"
        )
    
    with col2:
        st.subheader("Instructions & Examples")
        st.info("""
        **Adjacency Matrix:**
        - Square matrix representing the graph
        - Rows and columns represent vertices
        - 1 indicates an edge between vertices
        - 0 indicates no edge
        """)
        
        # Quick examples with proper handling
        st.markdown("**Quick Examples:**")
        example_graphs = {
            "Select an example": "",
            "Triangle Graph": "0,1\n1,2\n2,0",
            "Path Graph (4 vertices)": "0,1\n1,2\n2,3", 
            "Star Graph": "0,1\n0,2\n0,3",
            "Complete Graph K3": "0,1\n0,2\n1,2"
        }
        
        example_choice = st.selectbox("Choose example:", list(example_graphs.keys()), key="example_selector")
        
        if example_choice != "Select an example":
            # Update the edges input when example is selected
            example_edges = example_graphs[example_choice]
            if example_choice == "Triangle Graph":
                st.session_state.vertices_input = 3
            elif example_choice == "Path Graph (4 vertices)":
                st.session_state.vertices_input = 4
            elif example_choice == "Star Graph":
                st.session_state.vertices_input = 4
            elif example_choice == "Complete Graph K3":
                st.session_state.vertices_input = 3
            
            # Use a button to apply the example
            if st.button("Apply Example", key="apply_example"):
                st.session_state.edges_input = example_edges
                st.rerun()

    # Process edges and create adjacency matrix
    if st.button("🚀 Create Adjacency Matrix", type="primary", key="create_matrix"):
        if num_vertices <= 0:
            st.error("Number of vertices must be positive")
        elif not edges_input.strip():
            st.error("Please enter at least one edge")
        else:
            try:
                # Initialize adjacency matrix with zeros
                adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
                
                # Parse edges
                edges = []
                valid_edges = 0
                invalid_edges = []
                
                for line_num, line in enumerate(edges_input.strip().split('\n'), 1):
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            try:
                                u = int(parts[0].strip())
                                v = int(parts[1].strip())
                                if 0 <= u < num_vertices and 0 <= v < num_vertices:
                                    edges.append((u, v))
                                    adj_matrix[u][v] = 1
                                    adj_matrix[v][u] = 1  # For undirected graph
                                    valid_edges += 1
                                else:
                                    invalid_edges.append(f"Line {line_num}: ({u},{v}) - vertex index out of range")
                            except ValueError:
                                invalid_edges.append(f"Line {line_num}: '{line}' - invalid format")
                        else:
                            invalid_edges.append(f"Line {line_num}: '{line}' - expected format 'u,v'")
                
                # Store in session state
                st.session_state.adj_matrix = adj_matrix
                st.session_state.edges = edges
                st.session_state.vertices = num_vertices
                
                # Show warnings for invalid edges
                if invalid_edges:
                    st.warning(f"**Invalid edges skipped:**")
                    for warning in invalid_edges:
                        st.write(f"• {warning}")
                
                st.success(f"✅ Matrix created with {valid_edges} valid edges!")
                
            except Exception as e:
                st.error(f"Error processing input: {str(e)}")

    # Display results
    if st.session_state.adj_matrix is not None:
        st.subheader("📋 Results")
        
        adj_matrix = st.session_state.adj_matrix
        edges = st.session_state.edges
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.success("**Adjacency Matrix Created Successfully!**")
            st.write(f"**Number of vertices:** {len(adj_matrix)}")
            st.write(f"**Number of edges:** {len(edges)}")
            st.write("**Valid edges:**", edges)
            
            # Display matrix in a nice format
            st.subheader("🧮 Adjacency Matrix")
            
            # Create HTML table for matrix
            matrix_html = """
            <div style='display: flex; justify-content: center;'>
            <table style='border-collapse: collapse; margin: 10px;'>
            <tr>
                <th style='border: 1px solid black; padding: 10px; background-color: #f0f0f0;'></th>
            """
            
            # Header row
            for i in range(len(adj_matrix)):
                matrix_html += f"<th style='border: 1px solid black; padding: 10px; background-color: #f0f0f0;'>V{i}</th>"
            matrix_html += "</tr>"
            
            # Data rows
            for i in range(len(adj_matrix)):
                matrix_html += f"<tr><th style='border: 1px solid black; padding: 10px; background-color: #f0f0f0;'>V{i}</th>"
                for j in range(len(adj_matrix[i])):
                    color = "#d4edda" if adj_matrix[i][j] == 1 else "white"
                    matrix_html += f"<td style='border: 1px solid black; padding: 10px; text-align: center; background-color: {color}; font-weight: bold;'>{adj_matrix[i][j]}</td>"
                matrix_html += "</tr>"
            
            matrix_html += "</table></div>"
            st.markdown(matrix_html, unsafe_allow_html=True)
        
        with col_res2:
            # Display matrix as code
            st.subheader("🔢 Matrix Array")
            st.code(f"import numpy as np\nadj_matrix = np.array({adj_matrix.tolist()})")
            
            # Degree information
            st.subheader("📈 Vertex Degrees")
            degrees = []
            for i in range(len(adj_matrix)):
                degree = np.sum(adj_matrix[i])
                degrees.append(degree)
                st.write(f"• Vertex {i}: Degree {degree}")
            
            st.write(f"**Average degree:** {np.mean(degrees):.2f}")
            
            # Graph properties
            st.subheader("🔗 Graph Properties")
            total_possible_edges = num_vertices * (num_vertices - 1) // 2
            if total_possible_edges > 0:
                density = len(edges) / total_possible_edges
                st.write(f"**Graph density:** {density:.3f}")
            st.write(f"**Is complete graph:** {len(edges) == total_possible_edges}")

else:  # Bipartite Check
    st.header("🎨 Bipartite Graph Checker")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Graph Input")
        
        # Input options
        input_method = st.radio(
            "Input method:",
            ["Manual Input", "Use Previous Matrix"],
            key="input_method"
        )
        
        if input_method == "Manual Input":
            num_vertices = st.number_input(
                "Number of vertices:",
                min_value=1,
                max_value=20,
                value=4,
                key="bipartite_vertices"
            )
            
            st.markdown("**Enter edges (0-indexed):**")
            edges_input = st.text_area(
                "Edges (one per line):",
                value="0,1\n1,2\n2,3\n3,0",
                height=150,
                key="bipartite_edges",
                help="Example bipartite graph:\n0,1\n0,3\n1,2\n2,3"
            )
        else:
            if st.session_state.adj_matrix is None:
                st.warning("No previous adjacency matrix found. Please use manual input.")
                num_vertices = 4
                edges_input = "0,1\n1,2\n2,3\n3,0"
            else:
                st.success("Using previously created adjacency matrix")
                num_vertices = st.session_state.vertices
                edges = st.session_state.edges
                edges_input = '\n'.join([f"{u},{v}" for u, v in edges])
                st.info(f"Loaded: {num_vertices} vertices, {len(edges)} edges")
    
    with col2:
        st.subheader("Bipartite Graph Information")
        st.info("""
        **Bipartite Graph:**
        - Vertices can be divided into two disjoint sets
        - Every edge connects vertices from different sets
        - No edge between vertices in the same set
        - Can be colored with 2 colors
        """)
        
        # Bipartite examples
        st.markdown("**Bipartite Examples:**")
        bipartite_examples = {
            "Select an example": "",
            "Simple Bipartite": "0,1\n0,3\n1,2\n2,3",
            "Tree (always bipartite)": "0,1\n0,2\n1,3\n1,4", 
            "Non-Bipartite (triangle)": "0,1\n1,2\n2,0"
        }
        
        bip_example_choice = st.selectbox("Choose example:", list(bipartite_examples.keys()), key="bip_example_selector")
        
        if bip_example_choice != "Select an example":
            example_edges = bipartite_examples[bip_example_choice]
            if bip_example_choice == "Simple Bipartite":
                st.session_state.bipartite_vertices = 4
            elif bip_example_choice == "Tree (always bipartite)":
                st.session_state.bipartite_vertices = 5
            elif bip_example_choice == "Non-Bipartite (triangle)":
                st.session_state.bipartite_vertices = 3
            
            if st.button("Apply Example", key="apply_bip_example"):
                st.session_state.bipartite_edges = example_edges
                st.rerun()

    # Bipartite check function
    def is_bipartite(adj_matrix):
        n = len(adj_matrix)
        color = [-1] * n  # -1: uncolored, 0: color1, 1: color2
        
        for start in range(n):
            if color[start] == -1:
                color[start] = 0
                queue = [start]
                
                while queue:
                    u = queue.pop(0)
                    
                    for v in range(n):
                        if adj_matrix[u][v] == 1:
                            if color[v] == -1:
                                color[v] = 1 - color[u]
                                queue.append(v)
                            elif color[v] == color[u]:
                                return False, None
        
        # Separate vertices into two sets
        v1 = [i for i in range(n) if color[i] == 0]
        v2 = [i for i in range(n) if color[i] == 1]
        
        return True, (v1, v2)

    # Check bipartite button
    if st.button("🔍 Check Bipartite", type="primary", key="check_bipartite"):
        if num_vertices <= 0:
            st.error("Number of vertices must be positive")
        elif not edges_input.strip():
            st.error("Please enter at least one edge")
        else:
            try:
                # Create adjacency matrix from input
                adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
                edges = []
                valid_edges = 0
                
                for line in edges_input.strip().split('\n'):
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            u = int(parts[0].strip())
                            v = int(parts[1].strip())
                            if 0 <= u < num_vertices and 0 <= v < num_vertices:
                                edges.append((u, v))
                                adj_matrix[u][v] = 1
                                adj_matrix[v][u] = 1
                                valid_edges += 1
                
                if valid_edges == 0:
                    st.error("No valid edges found. Please check your input.")
                else:
                    # Perform bipartite check
                    is_bip, sets = is_bipartite(adj_matrix)
                    
                    st.subheader("📊 Results")
                    
                    # Display graph summary first
                    st.write(f"**Graph Summary:**")
                    st.write(f"• Vertices: {num_vertices}")
                    st.write(f"• Edges: {valid_edges}")
                    st.write(f"• Edge list: {edges}")
                    
                    st.markdown("---")
                    
                    if is_bip:
                        v1, v2 = sets
                        st.success("🎉 **The graph is BIPARTITE!**")
                        
                        col_bip1, col_bip2 = st.columns(2)
                        
                        with col_bip1:
                            st.subheader("Set V1")
                            for vertex in v1:
                                st.write(f"• Vertex {vertex}")
                            st.write(f"**Total:** {len(v1)} vertices")
                        
                        with col_bip2:
                            st.subheader("Set V2")
                            for vertex in v2:
                                st.write(f"• Vertex {vertex}")
                            st.write(f"**Total:** {len(v2)} vertices")
                        
                        # Validation
                        st.subheader("✅ Validation Check")
                        valid_partition = True
                        for u, v in edges:
                            if (u in v1 and v in v1) or (u in v2 and v in v2):
                                valid_partition = False
                                break
                        
                        if valid_partition:
                            st.success("✓ All edges connect vertices from different sets")
                        else:
                            st.error("✗ Partition validation failed")
                            
                    else:
                        st.error("❌ **The graph is NOT BIPARTITE**")
                        st.info("""
                        **Why it's not bipartite:**
                        - Contains odd-length cycles
                        - Cannot be colored with 2 colors
                        - Vertices cannot be divided into two independent sets
                        """)
                
            except Exception as e:
                st.error(f"Error processing graph: {str(e)}")

# Instructions section
st.markdown("---")
st.subheader("ℹ️ Instructions")

if method == "Adjacency Matrix":
    st.markdown("""
    ### Adjacency Matrix Instructions:
    1. **Enter number of vertices** (1-20)
    2. **Enter edges** as comma-separated pairs, one per line
    3. **Click 'Create Adjacency Matrix'** to generate
    4. **View results** including visualization and properties
    
    **Edge Format:**
    ```
    0,1    # Edge between vertex 0 and 1
    1,2    # Edge between vertex 1 and 2  
    2,3    # Edge between vertex 2 and 3
    ```
    
    **Note:** Graph is undirected (edges are bidirectional)
    """)
else:
    st.markdown("""
    ### Bipartite Check Instructions:
    1. **Choose input method** - manual or previous matrix
    2. **Enter graph data** (vertices and edges)
    3. **Click 'Check Bipartite'** to analyze
    4. **View results** - status and vertex sets if bipartite
    
    **Bipartite Properties:**
    - No odd-length cycles
    - 2-colorable
    - Vertices split into two independent sets
    """)

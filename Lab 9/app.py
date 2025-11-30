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
    st.session_state.vertices = 5
if 'edges' not in st.session_state:
    st.session_state.edges = []
if 'edges_input' not in st.session_state:
    st.session_state.edges_input = "0,1\n1,2\n2,3\n3,4\n0,4"
if 'bipartite_edges_input' not in st.session_state:
    st.session_state.bipartite_edges_input = "0,1\n1,2\n2,3\n3,0"

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
            value=st.session_state.vertices,
            key="vertices_input",
            help="Enter the number of vertices in the graph (1-20)"
        )
        
        st.markdown("**Enter edges (0-indexed):**")
        st.info("Format: '0,1' for edge between vertex 0 and 1")
        
        # Input edges - use session state
        edges_input = st.text_area(
            "Edges (one per line):",
            value=st.session_state.edges_input,
            height=150,
            key="edges_input_area",
            help="Enter edges as comma-separated pairs. Example:\n0,1\n1,2\n2,3"
        )
        
        # Update session state
        st.session_state.edges_input = edges_input
    
    with col2:
        st.subheader("Instructions")
        st.info("""
        **Adjacency Matrix:**
        - Square matrix representing the graph
        - Rows and columns represent vertices
        - 1 indicates an edge between vertices
        - 0 indicates no edge
        
        **Example Input:**
        - Vertices: 4
        - Edges: 
          0,1
          1,2  
          2,3
          3,0
        
        Creates a 4x4 matrix with 1s at 
        positions (0,1), (1,2), (2,3), (3,0)
        """)

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
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 2:
                            try:
                                u = int(parts[0].strip())
                                v = int(parts[1].strip())
                                if 0 <= u < num_vertices and 0 <= v < num_vertices:
                                    # Add edge to both directions for undirected graph
                                    edges.append((u, v))
                                    adj_matrix[u][v] = 1
                                    adj_matrix[v][u] = 1
                                    valid_edges += 1
                                else:
                                    invalid_edges.append(f"Line {line_num}: ({u},{v}) - vertex index must be between 0 and {num_vertices-1}")
                            except ValueError:
                                invalid_edges.append(f"Line {line_num}: '{line}' - must contain numbers only")
                        else:
                            invalid_edges.append(f"Line {line_num}: '{line}' - expected format 'u,v'")
                
                # Store in session state
                st.session_state.adj_matrix = adj_matrix
                st.session_state.edges = edges
                st.session_state.vertices = num_vertices
                
                # Show results
                st.success(f"✅ Matrix created successfully!")
                st.write(f"**Valid edges processed:** {valid_edges}")
                
                # Show warnings for invalid edges
                if invalid_edges:
                    st.warning("**Some edges were skipped:**")
                    for warning in invalid_edges[:5]:  # Show first 5 warnings
                        st.write(f"• {warning}")
                    if len(invalid_edges) > 5:
                        st.write(f"• ... and {len(invalid_edges) - 5} more")
                
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
            st.write(f"**Number of valid edges:** {len(edges)}")
            st.write("**Edge list:**", edges)
            
            # Display matrix in a nice format
            st.subheader("🧮 Adjacency Matrix")
            
            # Create HTML table for matrix
            matrix_html = """
            <div style='display: flex; justify-content: center;'>
            <table style='border-collapse: collapse; margin: 10px; border: 2px solid #333;'>
            <tr>
                <th style='border: 1px solid #666; padding: 12px; background-color: #4CAF50; color: white; font-weight: bold;'>V</th>
            """
            
            # Header row
            for i in range(len(adj_matrix)):
                matrix_html += f"<th style='border: 1px solid #666; padding: 12px; background-color: #4CAF50; color: white; font-weight: bold;'>{i}</th>"
            matrix_html += "</tr>"
            
            # Data rows
            for i in range(len(adj_matrix)):
                matrix_html += f"<tr><th style='border: 1px solid #666; padding: 12px; background-color: #4CAF50; color: white; font-weight: bold;'>{i}</th>"
                for j in range(len(adj_matrix[i])):
                    color = "#90EE90" if adj_matrix[i][j] == 1 else "white"  # Light green for edges
                    weight = "bold" if adj_matrix[i][j] == 1 else "normal"
                    matrix_html += f"<td style='border: 1px solid #666; padding: 12px; text-align: center; background-color: {color}; font-weight: {weight};'>{adj_matrix[i][j]}</td>"
                matrix_html += "</tr>"
            
            matrix_html += "</table></div>"
            st.markdown(matrix_html, unsafe_allow_html=True)
        
        with col_res2:
            # Display matrix as code
            st.subheader("🔢 Python Code")
            st.code(f"import numpy as np\n\n# Adjacency matrix for graph with {len(adj_matrix)} vertices\nadj_matrix = np.array({adj_matrix.tolist()})")
            
            # Degree information
            st.subheader("📈 Vertex Degrees")
            total_degree = 0
            for i in range(len(adj_matrix)):
                degree = np.sum(adj_matrix[i])
                total_degree += degree
                st.write(f"• Vertex {i}: Degree {degree}")
            
            avg_degree = total_degree / len(adj_matrix) if len(adj_matrix) > 0 else 0
            st.write(f"**Average degree:** {avg_degree:.2f}")
            
            # Graph properties
            st.subheader("🔗 Graph Properties")
            total_possible_edges = len(adj_matrix) * (len(adj_matrix) - 1) // 2
            if total_possible_edges > 0:
                density = len(edges) / total_possible_edges
                st.write(f"**Graph density:** {density:.3f}")
                st.write(f"**Is complete graph:** {len(edges) == total_possible_edges}")
            
            # Check if graph is connected
            def is_connected(adj_matrix):
                n = len(adj_matrix)
                if n == 0:
                    return True
                visited = [False] * n
                stack = [0]
                visited[0] = True
                count = 1
                
                while stack:
                    node = stack.pop()
                    for neighbor in range(n):
                        if adj_matrix[node][neighbor] == 1 and not visited[neighbor]:
                            visited[neighbor] = True
                            stack.append(neighbor)
                            count += 1
                
                return count == n
            
            st.write(f"**Is connected:** {is_connected(adj_matrix)}")

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
            
            # Use session state for bipartite edges
            bipartite_edges_input = st.text_area(
                "Edges (one per line):",
                value=st.session_state.bipartite_edges_input,
                height=150,
                key="bipartite_edges_area",
                help="Example: 0,1 for edge between vertex 0 and 1"
            )
            st.session_state.bipartite_edges_input = bipartite_edges_input
            
        else:
            if st.session_state.adj_matrix is None:
                st.warning("No previous adjacency matrix found. Please use manual input.")
                num_vertices = 4
                bipartite_edges_input = st.session_state.bipartite_edges_input
            else:
                st.success("Using previously created adjacency matrix")
                num_vertices = st.session_state.vertices
                edges = st.session_state.edges
                bipartite_edges_input = '\n'.join([f"{u},{v}" for u, v in edges])
                st.info(f"Loaded: {num_vertices} vertices, {len(edges)} edges")
    
    with col2:
        st.subheader("Bipartite Graph Information")
        st.info("""
        **Bipartite Graph:**
        - Vertices can be divided into two disjoint sets
        - Every edge connects vertices from different sets
        - No edge between vertices in the same set
        - Can be colored with 2 colors
        
        **Examples:**
        - Bipartite: 0,1 and 1,2 and 2,3 and 3,0
        - Not Bipartite: 0,1 and 1,2 and 2,0 (triangle)
        """)

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
        if input_method == "Use Previous Matrix" and st.session_state.adj_matrix is not None:
            # Use the existing matrix
            adj_matrix = st.session_state.adj_matrix
            edges = st.session_state.edges
            num_vertices = st.session_state.vertices
        else:
            # Create new matrix from manual input
            if num_vertices <= 0:
                st.error("Number of vertices must be positive")
                st.stop()
            elif not bipartite_edges_input.strip():
                st.error("Please enter at least one edge")
                st.stop()
            
            try:
                adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
                edges = []
                valid_edges = 0
                
                for line in bipartite_edges_input.strip().split('\n'):
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) == 2:
                            try:
                                u = int(parts[0].strip())
                                v = int(parts[1].strip())
                                if 0 <= u < num_vertices and 0 <= v < num_vertices:
                                    edges.append((u, v))
                                    adj_matrix[u][v] = 1
                                    adj_matrix[v][u] = 1
                                    valid_edges += 1
                            except ValueError:
                                pass
                
                if valid_edges == 0:
                    st.error("No valid edges found. Please check your input.")
                    st.stop()
                    
            except Exception as e:
                st.error(f"Error processing input: {str(e)}")
                st.stop()
        
        # Perform bipartite check
        is_bip, sets = is_bipartite(adj_matrix)
        
        st.subheader("📊 Results")
        
        # Display graph summary
        st.write(f"**Graph Summary:**")
        st.write(f"• Vertices: {num_vertices}")
        st.write(f"• Edges: {len(edges)}")
        st.write(f"• Edge list: {edges}")
        
        st.markdown("---")
        
        if is_bip:
            v1, v2 = sets
            st.success("🎉 **The graph is BIPARTITE!**")
            
            col_bip1, col_bip2 = st.columns(2)
            
            with col_bip1:
                st.subheader("📍 Set V1")
                for vertex in v1:
                    st.write(f"• Vertex {vertex}")
                st.write(f"**Total:** {len(v1)} vertices")
            
            with col_bip2:
                st.subheader("📍 Set V2")
                for vertex in v2:
                    st.write(f"• Vertex {vertex}")
                st.write(f"**Total:** {len(v2)} vertices")
            
            # Validation
            st.subheader("✅ Validation Check")
            valid_partition = True
            problematic_edges = []
            for u, v in edges:
                if (u in v1 and v in v1) or (u in v2 and v in v2):
                    valid_partition = False
                    problematic_edges.append((u, v))
            
            if valid_partition:
                st.success("✓ Perfect! All edges connect vertices from different sets")
            else:
                st.error(f"✗ Partition issue: edges {problematic_edges} connect vertices in same set")
                
        else:
            st.error("❌ **The graph is NOT BIPARTITE**")
            st.info("""
            **Why it's not bipartite:**
            - Contains odd-length cycles
            - Cannot be colored with 2 colors
            - Vertices cannot be divided into two independent sets
            """)

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
    
    **Note:** The graph is undirected (edges are bidirectional)
    """)
else:
    st.markdown("""
    ### Bipartite Check Instructions:
    1. **Choose input method** - manual or previous matrix
    2. **Enter graph data** (vertices and edges)
    3. **Click 'Check Bipartite'** to analyze
    4. **View results** - status and vertex sets if bipartite
    
    **What makes a graph bipartite:**
    - Can be colored with exactly 2 colors
    - No edges between vertices of the same color
    - All cycles have even length
    """)

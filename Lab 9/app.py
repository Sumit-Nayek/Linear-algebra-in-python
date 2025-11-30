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

# Sidebar for method selection
method = st.sidebar.selectbox(
    "Select Graph Operation",
    ["Adjacency Matrix", "Bipartite Check"]
)

st.session_state.current_method = method

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
            help="Enter the number of vertices in the graph (1-20)"
        )
        
        st.session_state.vertices = num_vertices
        
        st.markdown("**Enter edges (0-indexed):**")
        st.info("Format: '0,1' for edge between vertex 0 and 1")
        
        # Input edges
        edges_input = st.text_area(
            "Edges (one per line):",
            value="0,1\n1,2\n2,3\n3,4\n0,4",
            height=150,
            help="Enter edges as comma-separated pairs. Example:\n0,1\n1,2\n2,3"
        )
    
    with col2:
        st.subheader("Instructions")
        st.info("""
        **Adjacency Matrix:**
        - Square matrix representing the graph
        - Rows and columns represent vertices
        - 1 indicates an edge between vertices
        - 0 indicates no edge
        
        **Example:**
        - Vertices: 4
        - Edges: 0,1  1,2  2,3
        Creates a 4x4 matrix with 1s at 
        positions (0,1), (1,2), (2,3)
        """)
        
        st.markdown("**Quick Examples:**")
        example_graphs = {
            "Triangle Graph": "3\n0,1\n1,2\n2,0",
            "Path Graph": "4\n0,1\n1,2\n2,3",
            "Star Graph": "4\n0,1\n0,2\n0,3",
            "Complete Graph K3": "3\n0,1\n0,2\n1,2"
        }
        
        example_choice = st.selectbox("Load example:", list(example_graphs.keys()))
        if st.button("Load Example"):
            example_data = example_graphs[example_choice].split('\n')
            num_vertices = int(example_data[0])
            edges_input = '\n'.join(example_data[1:])
            st.session_state.vertices = num_vertices
            st.rerun()

    # Process edges and create adjacency matrix
    if st.button("🚀 Create Adjacency Matrix", type="primary"):
        if num_vertices <= 0:
            st.error("Number of vertices must be positive")
        else:
            try:
                # Initialize adjacency matrix with zeros
                adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
                
                # Parse edges
                edges = []
                for line in edges_input.strip().split('\n'):
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            u = int(parts[0].strip())
                            v = int(parts[1].strip())
                            if u < num_vertices and v < num_vertices:
                                edges.append((u, v))
                                adj_matrix[u][v] = 1
                                adj_matrix[v][u] = 1  # For undirected graph
                            else:
                                st.warning(f"Edge ({u},{v}) skipped - vertex index out of range")
                
                st.session_state.adj_matrix = adj_matrix
                st.session_state.edges = edges
                
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
            st.write("**Edges:**", edges)
            
            # Display matrix in a nice format
            st.subheader("🧮 Adjacency Matrix")
            matrix_html = "<div style='text-align: center;'>"
            matrix_html += "<table style='margin: 0 auto; border-collapse: collapse;'>"
            
            # Header row
            matrix_html += "<tr><th></th>"
            for i in range(len(adj_matrix)):
                matrix_html += f"<th style='border: 1px solid black; padding: 8px; background-color: #f0f0f0;'>V{i}</th>"
            matrix_html += "</tr>"
            
            # Data rows
            for i in range(len(adj_matrix)):
                matrix_html += f"<tr><th style='border: 1px solid black; padding: 8px; background-color: #f0f0f0;'>V{i}</th>"
                for j in range(len(adj_matrix[i])):
                    color = "#e6f3ff" if adj_matrix[i][j] == 1 else "white"
                    matrix_html += f"<td style='border: 1px solid black; padding: 8px; text-align: center; background-color: {color};'>{adj_matrix[i][j]}</td>"
                matrix_html += "</tr>"
            
            matrix_html += "</table></div>"
            st.markdown(matrix_html, unsafe_allow_html=True)
        
        with col_res2:
            # Display matrix as numpy array
            st.subheader("🔢 Matrix Array")
            st.code(f"np.array({adj_matrix.tolist()})")
            
            # Degree information
            st.subheader("📈 Vertex Degrees")
            degrees = []
            for i in range(len(adj_matrix)):
                degree = np.sum(adj_matrix[i])
                degrees.append(degree)
                st.write(f"Vertex {i}: Degree {degree}")
            
            st.write(f"**Average degree:** {np.mean(degrees):.2f}")
            
            # Connected components information
            st.subheader("🔗 Graph Connectivity")
            visited = [False] * len(adj_matrix)
            
            def dfs(node):
                stack = [node]
                component = []
                while stack:
                    current = stack.pop()
                    if not visited[current]:
                        visited[current] = True
                        component.append(current)
                        for neighbor in range(len(adj_matrix)):
                            if adj_matrix[current][neighbor] == 1 and not visited[neighbor]:
                                stack.append(neighbor)
                return component
            
            components = []
            for i in range(len(adj_matrix)):
                if not visited[i]:
                    component = dfs(i)
                    components.append(component)
            
            st.write(f"**Number of connected components:** {len(components)}")
            for i, comp in enumerate(components):
                st.write(f"Component {i+1}: {comp}")

else:  # Bipartite Check
    st.header("🎨 Bipartite Graph Checker")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Graph Input")
        
        # Input options
        input_method = st.radio(
            "Input method:",
            ["Manual Input", "Use Previous Matrix"]
        )
        
        if input_method == "Manual Input":
            num_vertices = st.number_input(
                "Number of vertices:",
                min_value=1,
                max_value=20,
                value=5,
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
                num_vertices = 0
                edges_input = ""
            else:
                st.success("Using previously created adjacency matrix")
                num_vertices = len(st.session_state.adj_matrix)
                edges = st.session_state.edges
                edges_input = '\n'.join([f"{u},{v}" for u, v in edges])
    
    with col2:
        st.subheader("Bipartite Graph Information")
        st.info("""
        **Bipartite Graph:**
        - Vertices can be divided into two disjoint sets
        - Every edge connects vertices from different sets
        - No edge between vertices in the same set
        - Can be colored with 2 colors
        
        **Properties:**
        - No odd-length cycles
        - Chromatic number = 2
        - Common examples: Trees, Grids
        """)
        
        st.markdown("**Bipartite Examples:**")
        bipartite_examples = {
            "Simple Bipartite": "4\n0,1\n0,3\n1,2\n2,3",
            "Tree (always bipartite)": "5\n0,1\n0,2\n1,3\n1,4",
            "Non-Bipartite (triangle)": "3\n0,1\n1,2\n2,0"
        }
        
        example_choice = st.selectbox("Load example:", list(bipartite_examples.keys()))
        if st.button("Load Bipartite Example"):
            example_data = bipartite_examples[example_choice].split('\n')
            num_vertices = int(example_data[0])
            edges_input = '\n'.join(example_data[1:])
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
    if st.button("🔍 Check Bipartite", type="primary"):
        if num_vertices <= 0:
            st.error("Number of vertices must be positive")
        else:
            try:
                # Create adjacency matrix from input
                adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
                edges = []
                
                for line in edges_input.strip().split('\n'):
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            u = int(parts[0].strip())
                            v = int(parts[1].strip())
                            if u < num_vertices and v < num_vertices:
                                edges.append((u, v))
                                adj_matrix[u][v] = 1
                                adj_matrix[v][u] = 1
                            else:
                                st.warning(f"Edge ({u},{v}) skipped - vertex index out of range")
                
                # Perform bipartite check
                is_bip, sets = is_bipartite(adj_matrix)
                
                st.subheader("📊 Results")
                
                if is_bip:
                    v1, v2 = sets
                    st.success("🎉 **The graph is BIPARTITE!**")
                    
                    col_bip1, col_bip2 = st.columns(2)
                    
                    with col_bip1:
                        st.subheader("Set V1")
                        st.write([f"V{i}" for i in v1])
                        st.write(f"**Size:** {len(v1)} vertices")
                    
                    with col_bip2:
                        st.subheader("Set V2")
                        st.write([f"V{i}" for i in v2])
                        st.write(f"**Size:** {len(v2)} vertices")
                    
                    # Display coloring
                    st.subheader("🎨 Vertex Coloring")
                    coloring_info = []
                    for i in range(num_vertices):
                        color_set = "V1" if i in v1 else "V2"
                        coloring_info.append(f"Vertex {i} → {color_set}")
                    
                    # Display in chunks to avoid horizontal scrolling
                    chunk_size = 5
                    for i in range(0, len(coloring_info), chunk_size):
                        st.write(" | ".join(coloring_info[i:i+chunk_size]))
                    
                    # Validation
                    st.subheader("✅ Validation")
                    valid = True
                    problematic_edges = []
                    for u, v in edges:
                        if (u in v1 and v in v1) or (u in v2 and v in v2):
                            valid = False
                            problematic_edges.append((u, v))
                    
                    if valid:
                        st.success("✓ All edges connect vertices from different sets")
                    else:
                        st.error(f"✗ Invalid bipartition detected in edges: {problematic_edges}")
                        
                else:
                    st.error("❌ **The graph is NOT BIPARTITE**")
                    st.info("""
                    **Why it's not bipartite:**
                    - Contains odd-length cycles
                    - Cannot be colored with 2 colors
                    - Vertices cannot be divided into two independent sets
                    """)
                
                # Display the graph summary
                st.subheader("📋 Graph Summary")
                st.write(f"**Vertices:** {num_vertices}")
                st.write(f"**Edges:** {len(edges)}")
                st.write(f"**Edge list:** {edges}")
                
                # Additional graph properties
                st.subheader("🔍 Graph Properties")
                
                # Check if graph is connected
                visited = [False] * num_vertices
                def dfs(node):
                    stack = [node]
                    component_size = 0
                    while stack:
                        current = stack.pop()
                        if not visited[current]:
                            visited[current] = True
                            component_size += 1
                            for neighbor in range(num_vertices):
                                if adj_matrix[current][neighbor] == 1 and not visited[neighbor]:
                                    stack.append(neighbor)
                    return component_size
                
                components = 0
                for i in range(num_vertices):
                    if not visited[i]:
                        comp_size = dfs(i)
                        components += 1
                
                st.write(f"**Connected components:** {components}")
                st.write(f"**Graph is connected:** {components == 1}")
                
            except Exception as e:
                st.error(f"Error processing graph: {str(e)}")

# Instructions section
st.markdown("---")
st.subheader("ℹ️ Instructions")

if method == "Adjacency Matrix":
    st.markdown("""
    ### Adjacency Matrix Instructions:
    1. **Enter number of vertices** (1-20 for display purposes)
    2. **Enter edges** as comma-separated pairs, one per line
    3. **Click 'Create Adjacency Matrix'** to generate the matrix
    4. **View results** including matrix visualization and vertex degrees
    
    **Edge Format Examples:**
    - `0,1` - Edge between vertex 0 and 1
    - `2,3` - Edge between vertex 2 and 3
    - `4,0` - Edge between vertex 4 and 0
    
    **Note:** The graph is assumed to be undirected
    """)
else:
    st.markdown("""
    ### Bipartite Check Instructions:
    1. **Choose input method** - manual or use previous matrix
    2. **Enter graph data** (vertices and edges)
    3. **Click 'Check Bipartite'** to analyze the graph
    4. **View results** - bipartite status and vertex sets if applicable
    
    **What makes a graph bipartite:**
    - Can be colored with exactly 2 colors
    - No edges between vertices of the same color
    - All cycles have even length
    
    **Common Bipartite Graphs:**
    - Trees
    - Grid graphs
    - Graphs with no odd cycles
    """)

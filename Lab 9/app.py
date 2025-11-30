import streamlit as st
import numpy as np

st.title("Graph Analysis Tool")

# Method selection
method = st.selectbox("Select Operation", ["Adjacency Matrix", "Bipartite Check"])

if method == "Adjacency Matrix":
    st.header("Create Adjacency Matrix")
    
    # Input
    num_vertices = st.number_input("Number of vertices:", min_value=1, max_value=10, value=4)
    
    st.write("Enter edges (format: 0,1 for edge between vertex 0 and 1):")
    edges_input = st.text_area("Edges (one per line):", value="0,1\n1,2\n2,3\n3,0", height=100)
    
    if st.button("Create Matrix"):
        if num_vertices > 0 and edges_input.strip():
            # Create matrix
            adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
            edges = []
            
            # Parse edges
            for line in edges_input.strip().split('\n'):
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        try:
                            u = int(parts[0])
                            v = int(parts[1])
                            if 0 <= u < num_vertices and 0 <= v < num_vertices:
                                adj_matrix[u][v] = 1
                                adj_matrix[v][u] = 1
                                edges.append((u, v))
                        except:
                            pass
            
            # Display results
            st.subheader("Adjacency Matrix")
            st.write(adj_matrix)
            
            st.subheader("Edge List")
            st.write(edges)

else:  # Bipartite Check
    st.header("Check Bipartite Graph")
    
    # Input
    num_vertices = st.number_input("Number of vertices:", min_value=1, max_value=10, value=4, key="bip_vertices")
    
    st.write("Enter edges (format: 0,1 for edge between vertex 0 and 1):")
    edges_input = st.text_area("Edges (one per line):", value="0,1\n1,2\n2,3\n3,0", height=100, key="bip_edges")
    
    if st.button("Check Bipartite"):
        if num_vertices > 0 and edges_input.strip():
            # Create matrix
            adj_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
            
            # Parse edges
            for line in edges_input.strip().split('\n'):
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        try:
                            u = int(parts[0])
                            v = int(parts[1])
                            if 0 <= u < num_vertices and 0 <= v < num_vertices:
                                adj_matrix[u][v] = 1
                                adj_matrix[v][u] = 1
                        except:
                            pass
            
            # Bipartite check function
            def is_bipartite(adj_matrix):
                n = len(adj_matrix)
                color = [-1] * n
                
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
                
                v1 = [i for i in range(n) if color[i] == 0]
                v2 = [i for i in range(n) if color[i] == 1]
                return True, (v1, v2)
            
            # Check bipartite
            is_bip, sets = is_bipartite(adj_matrix)
            
            if is_bip:
                v1, v2 = sets
                st.success("Graph is BIPARTITE")
                st.write("Set V1:", v1)
                st.write("Set V2:", v2)
            else:
                st.error("Graph is NOT BIPARTITE")

# Instructions
st.markdown("---")
st.write("**Instructions:**")
st.write("- Enter number of vertices")
st.write("- Enter edges as 'u,v' on separate lines")
st.write("- Click the button to see results")
import streamlit as st
import numpy as np
from itertools import permutations

st.title("Simple Math Tools")

# Tool selection
tool = st.selectbox("Select Tool", ["Graph Isomorphism", "Inclusion-Exclusion Count"])

if tool == "Graph Isomorphism":
    st.header("Graph Isomorphism Checker")
    
    # Simple matrix input
    st.write("Enter adjacency matrices (use 0/1, comma separated)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Graph G1")
        g1_input = st.text_area("G1 Matrix:", value="0,1,1\n1,0,1\n1,1,0", height=100)
    
    with col2:
        st.subheader("Graph G2")  
        g2_input = st.text_area("G2 Matrix:", value="0,1,1\n1,0,1\n1,1,0", height=100)

    def check_isomorphic(g1, g2):
        n1, n2 = len(g1), len(g2)
        if n1 != n2:
            return False
        
        # Try all permutations
        for perm in permutations(range(n1)):
            # Check if permutation makes matrices equal
            match = True
            for i in range(n1):
                for j in range(n1):
                    if g1[i][j] != g2[perm[i]][perm[j]]:
                        match = False
                        break
                if not match:
                    break
            if match:
                return True
        return False

    if st.button("Check Isomorphism"):
        try:
            # Parse matrices
            g1 = [[int(x) for x in row.split(',')] for row in g1_input.strip().split('\n') if row.strip()]
            g2 = [[int(x) for x in row.split(',')] for row in g2_input.strip().split('\n') if row.strip()]
            
            if len(g1) != len(g2):
                st.error("Graphs must have same number of vertices!")
            else:
                if check_isomorphic(g1, g2):
                    st.success("✅ Graphs are ISOMORPHIC")
                else:
                    st.error("❌ Graphs are NOT isomorphic")
                    
        except Exception as e:
            st.error(f"Error: Check your matrix format!")

else:  # Inclusion-Exclusion
    st.header("Inclusion-Exclusion Counter")
    
    n = st.number_input("Enter N:", min_value=1, max_value=100000, value=100)
    
    if st.button("Count Numbers"):
        # Using Principle of Inclusion-Exclusion
        count_2 = n // 2      # divisible by 2
        count_3 = n // 3      # divisible by 3  
        count_5 = n // 5      # divisible by 5
        
        count_2_3 = n // 6    # divisible by 2 and 3 (lcm=6)
        count_2_5 = n // 10   # divisible by 2 and 5 (lcm=10)
        count_3_5 = n // 15   # divisible by 3 and 5 (lcm=15)
        
        count_2_3_5 = n // 30  # divisible by 2,3,5 (lcm=30)
        
        # PIE formula
        total = count_2 + count_3 + count_5 - count_2_3 - count_2_5 - count_3_5 + count_2_3_5
        
        st.success(f"Numbers from 1 to {n} divisible by 2, 3, or 5: {total}")
        
        # Show breakdown
        st.write("**Breakdown:**")
        st.write(f"Divisible by 2: {count_2}")
        st.write(f"Divisible by 3: {count_3}")
        st.write(f"Divisible by 5: {count_5}")
        st.write(f"Divisible by 2 and 3: {count_2_3}")
        st.write(f"Divisible by 2 and 5: {count_2_5}") 
        st.write(f"Divisible by 3 and 5: {count_3_5}")
        st.write(f"Divisible by 2, 3 and 5: {count_2_3_5}")

# Instructions
st.markdown("---")
st.write("**Instructions:**")

if tool == "Graph Isomorphism":
    st.write("- Enter adjacency matrices with 0s and 1s")
    st.write("- Use commas to separate values, new lines for rows")
    st.write("- Example: '0,1,1' on first line, '1,0,1' on second, etc.")
else:
    st.write("- Enter a number N")
    st.write("- Counts numbers divisible by 2, 3, or 5 using Inclusion-Exclusion")
# Input for Graph G1
print("Graph G1:")
vertices1 = int(input("Enter number of vertices for G1: "))
matrix1 = [[0]*vertices1 for _ in range(vertices1)]
edges1 = int(input("Enter number of edges for G1: "))

print("Enter edges for G1 (vertex1 vertex2):")
for _ in range(edges1):
    v1, v2 = map(int, input().split())
    matrix1[v1][v2] = 1
    matrix1[v2][v1] = 1

# Input for Graph G2
print("\nGraph G2:")
vertices2 = int(input("Enter number of vertices for G2: "))
matrix2 = [[0]*vertices2 for _ in range(vertices2)]
edges2 = int(input("Enter number of edges for G2: "))

print("Enter edges for G2 (vertex1 vertex2):")
for _ in range(edges2):
    v1, v2 = map(int, input().split())
    matrix2[v1][v2] = 1
    matrix2[v2][v1] = 1

# Print both matrices
print("\nAdjacency Matrix G1:")
for row in matrix1:
    print(row)

print("\nAdjacency Matrix G2:")
for row in matrix2:
    print(row)

# Check basic conditions for isomorphism
if vertices1 != vertices2 or edges1 != edges2:
    print("\nGraphs are NOT ISOMORPHIC")
    print("(Different number of vertices or edges)")
else:
    # Check degree sequences
    deg1 = sorted([sum(row) for row in matrix1])
    deg2 = sorted([sum(row) for row in matrix2])
    
    if deg1 != deg2:
        print("\nGraphs are NOT ISOMORPHIC")
        print("(Different degree sequences)")
    else:
        # Try all permutations (brute force)
        from itertools import permutations
        
        n = vertices1
        found = False
        
        for perm in permutations(range(n)):
            # Check if this permutation makes matrices equal
            match = True
            for i in range(n):
                for j in range(n):
                    if matrix1[i][j] != matrix2[perm[i]][perm[j]]:
                        match = False
                        break
                if not match:
                    break
            
            if match:
                print("\nGraphs are ISOMORPHIC")
                print("Isomorphism mapping:")
                for i in range(n):
                    print(f"Vertex {i} in G1 -> Vertex {perm[i]} in G2")
                found = True
                break
        
        if not found:
            print("\nGraphs are NOT ISOMORPHIC")
            print("(No isomorphism found after checking all permutations)")
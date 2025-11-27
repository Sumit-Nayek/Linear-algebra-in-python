# Input number of vertices and edges
vertices = int(input("Enter number of vertices: "))
edges = int(input("Enter number of edges: "))

# Create empty adjacency matrix
matrix = [[0]*vertices for _ in range(vertices)]

# Fill the matrix with edges
print("Enter edges (vertex1 vertex2):")
for _ in range(edges):
    v1, v2 = map(int, input().split())
    matrix[v1][v2] = 1
    matrix[v2][v1] = 1  # for undirected graph

# Print the matrix
print("\nAdjacency Matrix:")
for row in matrix:
    print(row)
from collections import deque

# Input and create adjacency matrix
vertices = int(input("Enter number of vertices: "))
edges = int(input("Enter number of edges: "))

matrix = [[0]*vertices for _ in range(vertices)]
print("Enter edges (vertex1 vertex2):")
for _ in range(edges):
    v1, v2 = map(int, input().split())
    matrix[v1][v2] = 1
    matrix[v2][v1] = 1

# Check if bipartite
color = [-1] * vertices
is_bipartite = True
V1 = []
V2 = []

for i in range(vertices):
    if color[i] == -1:
        queue = deque([i])
        color[i] = 0
        V1.append(i)
        
        while queue:
            current = queue.popleft()
            for neighbor in range(vertices):
                if matrix[current][neighbor] == 1:
                    if color[neighbor] == -1:
                        color[neighbor] = 1 - color[current]
                        if color[neighbor] == 0:
                            V1.append(neighbor)
                        else:
                            V2.append(neighbor)
                        queue.append(neighbor)
                    elif color[neighbor] == color[current]:
                        is_bipartite = False
                        break

# Print result
if is_bipartite:
    print("\nGraph is BIPARTITE")
    print("V1:", V1)
    print("V2:", V2)
else:
    print("\nGraph is NOT BIPARTITE")
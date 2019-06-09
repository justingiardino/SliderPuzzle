#only care about nodes, not distance between nodes
#stack keeps track of alternate vertices

adjacency_matrix = {1: [2, 3],
                    2: [4, 5],
                    3: [5],
                    4: [6],
                    5: [6],
                    6: [7],
                    7: []}

def dfs_iterative(graph, start):
    stack, path = [start], []
    print("\nVertex : Adjacent Pieces\n" + "-"*22 + "\n")
    for vertex, adjacent_piece in graph.items():
        print("   {}   :   {}".format(vertex, adjacent_piece))

    while stack:
        print("Current value of stack: {}\nCurrent value of path: {}".format(stack,path))
        vertex = stack.pop()
        if vertex in path:
            print("Vertex ({}) is already in path".format(vertex))
            continue
        print("Adding vertex ({}) to path".format(vertex))
        path.append(vertex)
        for neighbor in graph[vertex]:
            print("Current neighbor: {}".format(neighbor))
            stack.append(neighbor)

    return path

print(dfs_iterative(adjacency_matrix, 1))

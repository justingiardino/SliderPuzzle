


# use set.add(Letter) to add to a set

# this is using a generator, so all values of set are not stored in memory
# cannot loop through a generator twice
# yield returns a generator object, in this case the output order I want
# in this case it is pushing multiple generator objects to the stack

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        print("Current stack: {}".format(stack))
        (vertex, path) = stack.pop()
        print("Vertex: {} Path: {}".format(vertex, path))
        print("Graph[vertex]: {}".format(graph[vertex]))
        for next in graph[vertex] - set(path):
            print("Next: {}".format(next))
            if next == goal:
                print("Hit yield\nNew path: {}".format(path + [next]))
                yield path + [next]
            else:
                stack.append((next, path + [next]))

if __name__ == '__main__':

    graph = {'A': set(['B', 'C']),
             'B': set(['A', 'D', 'E']),
             'C': set(['A', 'F']),
             'D': set(['B']),
             'E': set(['B', 'F']),
             'F': set(['C', 'E'])}
    print("\n\n" + "-"*28 + "\nVertex : Adjacent Directions")
    for vertex, direction in graph.items():
        print("   {}   :   {}".format(vertex, direction))


    multiple_paths = list(dfs_paths(graph, 'A', 'F'))
    print("All paths: {}".format(multiple_paths))
    min_size = 100
    out_path = []
    for path in multiple_paths:
        if len(path) < min_size:
            min_size = len(path)
            out_path = path

    print("Smallest path: {}".format(out_path))

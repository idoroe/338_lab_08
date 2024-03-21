class GraphNode:
    def __init__(self, data):
        self.data = data

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def addNode(self, data):
        if data not in self.adjacency_list:
            self.adjacency_list[data] = []
        return GraphNode(data)

    def removeNode(self, node):
        if node.data in self.adjacency_list:
            del self.adjacency_list[node.data]
            for connections in self.adjacency_list.values():
                connections[:] = [conn for conn in connections if conn[0] != node.data]

    def addEdge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data].append((n2.data, weight))
            self.adjacency_list[n2.data].append((n1.data, weight))

    def removeEdge(self, n1, n2):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data] = [conn for conn in self.adjacency_list[n1.data] if conn[0] != n2.data]
            self.adjacency_list[n2.data] = [conn for conn in self.adjacency_list[n2.data] if conn[0] != n1.data]

    def importFromFile(self, file_path):
        

     def _dfs_detect_cycle(self, node, visited, rec_stack):
        visited[node] = True
        rec_stack[node] = True

        for neighbour, _ in self.adjacency_list.get(node, []):
            if not visited.get(neighbour, False):
                if self._dfs_detect_cycle(neighbour, visited, rec_stack):
                    return True
            elif rec_stack.get(neighbour, False):
                return True

        rec_stack[node] = False
        return False

    def isdag(self):
        visited = {}
        rec_stack = {}
        for node in self.adjacency_list:
            if not visited.get(node, False):
                if self._dfs_detect_cycle(node, visited, rec_stack):
                    return False
        return True

    def _dfs_toposort(self, node, visited, stack):
        visited[node] = True
        for neighbour, _ in self.adjacency_list.get(node, []):
            if not visited.get(neighbour, False):
                self._dfs_toposort(neighbour, visited, stack)
        stack.insert(0, node)

    def toposort(self):
        if not self.isdag():
            return None
        visited = {}
        stack = []
        for node in self.adjacency_list:
            if not visited.get(node, False):
                self._dfs_toposort(node, visited, stack)
        return stack

#Depth-First Search (DFS) can be used for topological sorting. Because this algorithm investigates vertices as far as feasible along each branch before backtracking, it is well-suited for topological sorting. The main prerequisite of topological sorting is that all of a vertex's prerequisites must be visited before the vertex itself. This feature makes sure of that. DFS can be adjusted in a Directed Acyclic Graph (DAG) to generate a topological sort by listing vertices in the opposite order of when they finish (that is, when a vertex runs out of vertices to visit). 
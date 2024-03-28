import time

class GraphNode:
    def __init__(self, data):
        self.data = data


    def dfs(self, start_data):
        visited = set()
        order = []

        def dfs_recursive(node_data):
            if node_data not in visited:
                visited.add(node_data)
                order.append(node_data)
                for neighbour, _ in self.adjacency_list[node_data]:
                    dfs_recursive(neighbour)
        dfs_recursive(start_data)
        return order

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def addNode(self, data):
        if data not in self.adjacency_list:
            self.adjacency_list[data] = []
        return GraphNode(data)

    def addEdge(self, n1, n2, weight=1):
        if n1.data in self.adjacency_list and n2.data in self.adjacency_list:
            self.adjacency_list[n1.data].append((n2.data, weight))
            self.adjacency_list[n2.data].append((n1.data, weight))

    def dfs(self, start_data):
        visited = set()
        order = []

        def dfs_recursive(node_data):
            if node_data not in visited:
                visited.add(node_data)
                order.append(node_data)
                for neighbour, _ in self.adjacency_list[node_data]:
                    dfs_recursive(neighbour)
        dfs_recursive(start_data)
        return order


    def importFromFile(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        lines = content.split('\n')[1:-1]  # Skip the first and last lines
        for line in lines:
            line = line.strip()
            if not line or line.startswith("//"):  # Skip empty lines or comments
                continue
            parts = line.strip(';').split(' -- ')
            if len(parts) < 2: 
                continue
            n1_data, rest = parts[0], parts[1]
            weight = 1  
            if '[' in rest:
                node2_data, weight_part = rest.split('[')
                weight = int(weight_part.split('=')[1].rstrip(']'))
            else:
                node2_data = rest
            n1 = self.addNode(n1_data)
            n2 = self.addNode(node2_data)
            self.addEdge(n1, n2, weight)



class Graph2(Graph):
    def __init__(self):
        super().__init__()
        self.node_indices = {}
        self.matrix = []

    def addNode(self, data):
        node = super().addNode(data)
        if data not in self.node_indices:
            self.node_indices[data] = len(self.node_indices)
            for row in self.matrix:
                row.append(0)
            self.matrix.append([0] * (len(self.matrix) + 1))
        return node

    def addEdge(self, n1, n2, weight=1):
        super().addEdge(n1, n2, weight)
        i = self.node_indices[n1.data]
        j = self.node_indices[n2.data]
        self.matrix[i][j] = weight
        self.matrix[j][i] = weight

    def dfs(self, start_data):
        visited = set()
        order = []
        start_index = self.node_indices[start_data]

        def dfs_recursive(current_index):
            node_data = self.nodes[current_index]
            if node_data not in visited:
                visited.add(node_data)
                order.append(node_data)
                for i, weight in enumerate(self.matrix[current_index]):
                    if weight > 0 and self.nodes[i] not in visited:
                        dfs_recursive(i)

        dfs_recursive(start_index)
        return order

    def importFromFile(self, file_path):
        super().importFromFile(file_path)
        self.nodes = list(self.adjacency_list.keys())
        self.matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
        for node, edges in self.adjacency_list.items():
            i = self.node_indices[node]
            for edge, weight in edges:
                j = self.node_indices[edge]
                self.matrix[i][j] = weight
                self.matrix[j][i] = weight

def measure_dfs_performance(graph, start_data):
    times = []
    for _ in range(10):
        start_time = time.time()
        graph.dfs(start_data)
        end_time = time.time()
        times.append(end_time - start_time)

    return max(times), min(times), sum(times) / len(times)


graph = Graph()
graph2 = Graph2()
graph.importFromFile('random.dot')
graph2.importFromFile('random.dot')
print(measure_dfs_performance(graph, '0'))  
print(measure_dfs_performance(graph2, '0'))  


#(0.0010001659393310547(max1), 0.0(min1), 0.0006999969482421875(average1))
#(0.06900215148925781(max2), 0.06400036811828613(min2), 0.06689999103546143(average2))
#after running the tests, we see that graph 1 will be faster for sparse graghs due to the efficient representation of edges. gragh 2 is straightforward in edge look up, but takes more time due to its need to traverse the entire matrix, afecting its performance negativley for sparse gragps.
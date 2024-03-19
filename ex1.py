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
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            if not content.startswith("strict graph G"):
                return None
            
            self.adjacency_list.clear()
            content = content[content.find("{")+1:content.rfind("}")]
            for line in content.splitlines():
                line = line.strip().rstrip(';')
                if not line:  
                    continue
                parts = line.split("--")
                if len(parts) != 2:
                    return None
                
                node1_data, rest = parts[0].strip(), parts[1].strip()
                if '[' in rest:
                    node2_data, weight_part = rest.split('[')
                    weight = int(weight_part.split('=')[1].rstrip(']'))
                else:
                    node2_data = rest
                    weight = 1  
                
                n1 = self.addNode(node1_data)
                n2 = self.addNode(node2_data)
                self.addEdge(n1, n2, weight)
        except Exception as e:
            print(f"Error importing graph: {e}")
            return None

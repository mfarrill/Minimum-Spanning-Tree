import sys, csv
import networkx as nx
import matplotlib.pyplot as plt

class Graph():
    def __init__(self, order=0):
        self.order = order
        self.edges = []

    def read_graph(self, filename):
        try:
            with open(filename) as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    u, v, weight = int(row[0]), int(row[1]), float(row[2])
                    self.edges.append([u, v, weight])
                    # get the order of a graph with only a list of edges
                    self.order = max([self.order, u, v])
        except(FileNotFoundError):
            print(f"Invaid filename: {filename}")
            sys.exit()

    def write_graph(self, filename):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for edge in self.edges:
               writer.writerow([edge[0], edge[1], edge[2]])

    def kruskal(self):
        # Sort the edge list by weight 
        sorted_edges = sorted(self.edges, key = lambda x: x[2])
        ds = DisjointSet(self.order)     
        mwst = Graph(self.order)
        
        for edge in sorted_edges:
            root_u = ds.find(edge[0])
            root_v = ds.find(edge[1])
            if root_u != root_v:
                ds.union(root_u, root_v)
                mwst.edges.append(edge)
        return mwst

class DisjointSet():
    def __init__(self, size):
        # Initialize with size+1 since we start with 1st index
        self.parents = [i for i in range(size+1)]
        self.ranks = [0 for _ in range(size+1)]


    # Find the root of a tree and minimize height with path compression
    def find(self, x):
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    # Union by rank to minimize tree height
    def union(self, root_u, root_v):
        if self.ranks[root_u] > self.ranks[root_v]:
            self.parents[root_v] = root_u

        elif self.ranks[root_u] < self.ranks[root_v]:
            self.parents[root_u] = root_v
        
        else:
            self.parents[root_v] = root_u
            self.ranks[root_u] += 1

def main():
    if len(sys.argv) == 3:
        graph = Graph()
        graph.read_graph(sys.argv[1])
        mwst = graph.kruskal()
        mwst.write_graph(sys.argv[2])
    else:        
        print(f"Usage: python3 {sys.argv[0]} input output")
        
if __name__ == '__main__':
    main()

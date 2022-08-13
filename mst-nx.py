'''Kruskal's algorithm visualized using matplotlib and networkx'''
import sys
import networkx as nx
import matplotlib.pyplot as plt

class Graph():

    def __init__(self, filename):
            self.G = self.read_graph(filename) 
            self.init_disjoint_set()
            self.init_figure()

    def read_graph(self, filename):
        try:
            G = nx.read_weighted_edgelist(filename, nodetype=int, delimiter=',')
        except(FileNotFoundError):
            sys.exit(f'File not found: {filename}')
        else:
            return G

    def kruskals(self):
        sorted_edges = [[u, v, data['weight']] for u, v, data in self.G.edges(data=True)]
        sorted_edges.sort(key = lambda x: x[2])
        self.draw()
        for edge in sorted_edges:
            root_u = self.find(edge[0])
            root_v = self.find(edge[1])
            self.fig.text(0.125, 0.89, f'Examine vertices of edge({edge[0]}, {edge[1]}):\nCall find({edge[0]}), find({edge[1]}).', style = 'italic',fontsize=14, color='magenta')
            self.draw(examined=[(edge[0], edge[1])])
            if root_u != root_v:
                self.union(root_u, root_v)
                self.accepted.append((edge[0], edge[1]))
                self.fig.text(0.125, 0.89, f'Vertices have different roots:\nAdd edge to tree, call union({edge[0]}, {edge[1]}).', style = 'italic',fontsize=14, color='green')
                self.draw()
            else:
                self.rejected.append((edge[0], edge[1]))
                self.fig.text(0.125, 0.89, f'Vertices have the same root:\nReject edge({edge[0]}, {edge[1]}).', style = 'italic',fontsize=14, color='red')
                self.draw()
        
        plt.title('Completed: Minimum Weight Spanning Tree', style = 'italic', fontsize=16,)
        self.draw(last_frame=True)

    '''Disjoint set methods'''
    def init_disjoint_set(self):
        order = self.G.number_of_nodes()
        # Initialize with order+1 since we use assume vertices start with 1
        self.parents = [i for i in range(order+1)]
        self.ranks = [0 for _ in range(order+1)] 

    def find(self, x):
        if self.parents[x] != x:
            # Path compression to minimize tree height
            self.parents[x] = self.find(self.parents[x])
        self.table_data[1][x-1] = self.parents[x]
        return self.parents[x]

    def union(self, root_u, root_v):
        # Union by rank to further minimize tree height
        if self.ranks[root_u] > self.ranks[root_v]:
            self.parents[root_v] = root_u
            self.table_data[1][root_v-1] = root_u

        elif self.ranks[root_u] < self.ranks[root_v]:
            self.parents[root_u] = root_v
            self.table_data[1][root_u-1] = root_v
        
        else:
            self.parents[root_v] = root_u
            self.table_data[1][root_v-1] = root_u
            self.ranks[root_u] += 1

    '''Visualization methods'''
    def init_figure(self):
        # Setup figure size, plots, and layout
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.pos = nx.spring_layout(self.G)

        # Edge lists for highlighting
        self.accepted = []
        self.rejected = []

        # Initialize disjoint set table
        order = self.G.number_of_nodes()
        self.loc = 'bottom'
        self.table_data = [[i for i in range(1, order+1)], [i for i in range(1, order+1)]] 
        self.cell_colors = [['lightgray' for i in range(1, order+1)],['white' for i in range(1, order+1)]]
        self.row_labels = ['Vertex', 'Root']
        self.label_colors = ['lightgray', 'white']
    
    def draw(self, examined=[], last_frame=False):
        self.fig.text(0.4445, 0.03, 'Disjoint Set', fontsize=16)
        plt.table(cellText=self.table_data, rowLabels=self.row_labels, rowColours=self.label_colors, loc=self.loc, cellColours=self.cell_colors)
        plt.suptitle("Kruskal's algorithm", fontsize=20)
        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        if not last_frame:
            nx.draw_networkx(self.G, self.pos, with_labels=True, font_size=10, font_color='white')
            # Highlight edge differently when examined, accepted, rejected
            if examined:
                nx.draw_networkx_edges(self.G, self.pos, edgelist = examined, edge_color = 'magenta', width = 3.5, alpha = 0.6)
            if self.accepted:
                nx.draw_networkx_edges(self.G, self.pos, edgelist = self.accepted, edge_color = 'green', width = 3.0, alpha = 0.6)
            if self.rejected:
                nx.draw_networkx_edges(self.G, self.pos, edgelist = self.rejected, edge_color = 'red', width = 3.0, alpha = 0.6)
        else:
            # Draw only MST edges and edge labels for the last frame
            nx.draw_networkx_nodes(self.G, self.pos)
            nx.draw_networkx_labels(self.G, self.pos, font_size=10, font_color='white')
            for edge in list(edge_labels.keys()):
                if edge not in self.accepted:
                    del edge_labels[edge]
            # draw edges twice for consistant appearance, black edge and highlight
            nx.draw_networkx_edges(self.G, self.pos, edgelist = self.accepted, edge_color= 'black')
            nx.draw_networkx_edges(self.G, self.pos, edgelist = self.accepted, edge_color = 'green', width = 3.0, alpha = 0.7)
        
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, font_size=10, font_color='blue')
        plt.draw()
        plt.pause(0.6)
        plt.clf()

def main(argv): 
    default = 'input.csv'
    G = Graph(default if len(argv) < 2 else argv[1])
    G.kruskals()
    plt.show()
    
if __name__ == '__main__':
    main(sys.argv)

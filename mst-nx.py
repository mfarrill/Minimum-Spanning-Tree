import sys
import networkx as nx
import matplotlib.pyplot as plt

'''Kruskal's algorithm visualized with matplotlib'''
def Kruskals(G):
    plt.rcParams['figure.figsize'] = (12, 8)
    fig, ax = plt.subplots()
    size = len(G.edges())
    pos = nx.spring_layout(G) # create one layout for all figures drawn
    # parents and ranks used for disjoint set functions   
    parents = [i for i in range(size+1)]
    ranks = [0 for _ in range(size+1)]
    sorted_edges = [[u, v, data['weight']] for u, v, data in G.edges(data=True)]
    sorted_edges.sort(key = lambda x: x[2])
    # Create accepted and rejected edge lists for highlighting 
    acc = []
    rej = []
    draw_graph(G, pos)
    for edge in sorted_edges:
        fig.text(0.125, 0.9, f'find_root({edge[0]}), find_root({edge[1]}).', style = 'italic',fontsize = 16, color='magenta')
        draw_graph(G, pos, examined=[(edge[0], (edge[1]))], accepted=acc, rejected=rej)
        root_u = ds_find(parents, edge[0])
        root_v = ds_find(parents, edge[1])
        if root_u != root_v:
            fig.text(0.125, 0.9, f'Vertices have different roots.\nAdd edge to tree: union({edge[0]}, {edge[1]}).', style = 'italic',fontsize = 16, color='green')
            ds_union(parents, ranks, root_u, root_v)
            acc.append((edge[0], edge[1]))
            draw_graph(G, pos, accepted=acc, rejected=rej)
        else:
            fig.text(0.125, 0.9, f'Vertices have the same root.\nreject edge({edge[0]}, {edge[1]}).', style = 'italic',fontsize = 16, color='red')
            rej.append((edge[0], edge[1]))
            draw_graph(G, pos, accepted=acc, rejected=rej)
    
    fig.text(0.125, 0.9, 'Completed: Minimum Weight Spanning Tree.',fontsize = 16)
    draw_graph(G, pos, accepted=acc, last_frame=True)

'''Disjoint set functions'''
def ds_find(parents, x):
    if parents[x] != x:
        # Path compression to minimize tree height
        parents[x] = ds_find(parents, parents[x])
    return parents[x]

def ds_union(parents, ranks, root_u, root_v):
    # Union by rank to minimize tree height
    if ranks[root_u] > ranks[root_v]:
        parents[root_v] = root_u

    elif ranks[root_u] < ranks[root_v]:
        parents[root_u] = root_v
    
    else:
        parents[root_v] = root_u
        ranks[root_u] += 1

''' Drawing method that highlights each edge as it's examined and accepted into the MST'''
def draw_graph(G, pos, examined=[], accepted=[], rejected=[], last_frame=False):
    plt.suptitle("Kruskal's algorithm visualized", fontsize=20)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    if not last_frame:
        nx.draw_networkx(G, pos, with_labels=True, font_size=10, font_color='white')
        if examined:
            nx.draw_networkx_edges(G, pos, edgelist = examined, edge_color = 'magenta', width = 3.5, alpha = 0.6)
        if accepted:
            nx.draw_networkx_edges(G, pos, edgelist = accepted, edge_color = 'green', width = 3.0, alpha = 0.6)
        if rejected:
            nx.draw_networkx_edges(G, pos, edgelist = rejected, edge_color = 'red', width = 3.0, alpha = 0.6)

    else:
        # Draw only edges and edge labels in the MST for the last figure
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_labels(G, pos, font_size=10, font_color='white')
        for edge in list(edge_labels.keys()):
            if edge not in accepted:
                del edge_labels[edge]
        # draw edges twice for consistant appearance, black edge green highlight
        nx.draw_networkx_edges(G, pos, edgelist = accepted, edge_color= 'black')
        nx.draw_networkx_edges(G, pos, edgelist = accepted, edge_color = 'green', width = 3.0, alpha = 0.7)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, font_color='blue')
    plt.draw()
    plt.pause(0.8)
    plt.clf()

def read_graph(filename=''):
    try:
        G = nx.read_weighted_edgelist(filename, nodetype=int, delimiter=',')
    except(FileNotFoundError):
        sys.exit(f'File not found: {filename}')
    else:
        return G

def main(argv):
    # read_graph accepts a graph csv, default provided
    default = 'input.csv'
    G = read_graph(default if len(argv) < 2 else argv[1])
    Kruskals(G)
    plt.show()

if __name__ == '__main__':
    main(sys.argv)

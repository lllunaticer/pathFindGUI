import networkx as nx
import matplotlib.pyplot as plt
# 画网路图
def draw(w,path):
    # 传入参数 w 矩阵和 path向量

    G = nx.DiGraph()

    for li in w:
        G.add_weighted_edges_from([(li[0], li[1], li[2])])

    val_map = {1: 1.0,
               4: 0.5714285714285714,
               8: 0.0}

    values = [val_map.get(node, 0.25) for node in G.nodes()]
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])

    # Specify the edges you want here
    red_edges = path
    edge_colours = ['black' if not edge in red_edges else 'red'
                    for edge in G.edges()]
    black_edges = [edge for edge in G.edges() if edge not in red_edges]

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
                           node_color=values, node_size=500)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
    plt.show()

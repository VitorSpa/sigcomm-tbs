import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network


def draw_graph(G, save_path, draw_weights=False):
    # Draw the graph
    fig = plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    pos = nx.spring_layout(G)  # You can try different layouts like 'circular', 'spectral',
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black",
            font_weight="bold", width=1.5, edge_color="gray")
    if draw_weights:
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
    fig.savefig(save_path)

def draw_interactive_graph(G, save_path):
    nt = Network('500px', '1345px')
    nt.from_nx(G)
    for e in nt.edges:
        e['label'] = str(round(e['width'], 2))
        e['width'] = 2
        e["font"] = {"size": 20}
    for n in nt.nodes:
        n["size"] = 15
        n["font"] = {"size": 25}
    nt.save_graph(save_path)
    html_file = open(save_path, 'r', encoding='utf-8')
    source_code = html_file.read()
    return source_code


def update_weight(G, path_list, transfer_size, capacity_scaler):
    for node_a, node_b in zip(path_list, path_list[1:]):
        G[node_a][node_b]['weight'] += capacity_scaler * transfer_size

def path_weights(G, path_list):
    w_list = []
    for node_a, node_b in zip(path_list, path_list[1:]):
        w_list.append(G[node_a][node_b]['weight'])
    return w_list
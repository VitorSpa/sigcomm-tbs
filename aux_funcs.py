import networkx as nx
import matplotlib.pyplot as plt


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


def update_weight(G, path_list, transfer_size, capacity_scaler):
    for node_a, node_b in zip(path_list, path_list[1:]):
        G[node_a][node_b]['weight'] += capacity_scaler * transfer_size
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product


def draw_graph(G, save_path):
    # Draw the graph
    fig = plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    pos = nx.spring_layout(G)  # You can try different layouts like 'circular', 'spectral',
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_color="black",
            font_weight="bold", width=1.5, edge_color="gray")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    fig.savefig(save_path)


def update_weight(G, path_list, transfer_size):
    for node_a, node_b in zip(path_list, path_list[1:]):
        G[node_a][node_b]['weight'] += transfer_size


def fat_tree_menu():
    st.write(r'''
        A fat-tree topology is composed of Pods (edge and aggregation switches), Core Switches and Hosts.
        Typically it is defined in terms of the number of pods. For **k** Pods, there are:
        * k switches (each with k ports) in each pod;
        * $\frac{k}{2}^2$ core switches;
        * $\frac{k^3}{4}$ maximum hosts.
        ''')
    st.image("Figures/Fat_tree_network.svg",
             caption="A Fat Tree")
    n_pods = st.slider("How many Pods?", min_value=2, max_value=10, value=2, step=2)

    cores = [f"Core_{x}" for x in range(int(n_pods / 2) ** 2)]
    pods = [f"Pod_{x}" for x in range(n_pods)]
    max_hosts = ((n_pods ** 3) // 4) // n_pods

    G = nx.Graph()
    for core, pod in product(cores, pods):
        G.add_edge(core, pod, weight=0)

    if max_hosts > 1:
        n_hosts = st.slider("How many Hosts per Pod?", min_value=1, max_value=max_hosts, value=1, step=1)
    else:
        n_hosts = 1

    i = 0
    for pod in pods:
        for host in range(n_hosts):
            G.add_edge(pod, f"Host_{host + i}", weight=0)
        i += n_hosts

    draw_graph(G, "Figures/fat_tree.png")
    st.image("Figures/fat_tree.png", caption="Tree")

    return G

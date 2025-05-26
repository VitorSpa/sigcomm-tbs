import networkx as nx
from itertools import product
from aux_funcs import update_weight


def shortest_path(G, transfer_size, capacity_scaler):
    paths_lst = []
    hosts = [x for x in G.nodes() if "Host" in x]
    for h_i, h_j in product(hosts, hosts):
        if h_i != h_j:
            s_path = nx.shortest_path(G, source=h_i, target=h_j)
            paths_lst.append((
                h_i,
                h_j,
                s_path))
            update_weight(G, s_path, transfer_size, capacity_scaler)
    return paths_lst

def weighted_shortest_path(G, transfer_size, capacity_scaler):
    paths_lst = []
    hosts = [x for x in G.nodes() if "Host" in x]
    for h_i, h_j in product(hosts, hosts):
        if h_i != h_j:
            s_path = nx.dijkstra_path(G, source=h_i, target=h_j)
            paths_lst.append((
                h_i,
                h_j,
                s_path))
            update_weight(G, s_path, transfer_size, capacity_scaler)
    return paths_lst


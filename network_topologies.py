from io import StringIO

import streamlit as st
import json
import networkx as nx
from networkx.readwrite import json_graph

from itertools import product, combinations
import numpy as np

from aux_funcs import draw_graph


@st.fragment
def custom_topo():
    st.write(r'''
        User defined custom topology. 
        Provide a JSON with the following structure:
        ''')
    st.json(
        {
            "nodes": [
                {"id": "A"},
                {"id": "B"},
                {"id": "C"},
            ],
            "links": [
                {"source": "A", "target": "B", "value": 1},
                {"source": "B", "target": "C", "value": 2},
            ]
        }, expanded=2,
    )
    uploaded_file = st.file_uploader(
        "Topology file", accept_multiple_files=False, type=['json']
    )

    G = nx.Graph()
    if uploaded_file is not None:
        js_graph = json.load(uploaded_file)
        G = json_graph.node_link_graph(js_graph)
        print(G)
    return G

@st.fragment
def fat_tree():
    st.write(r'''
        A fat-tree topology is composed of Pods (edge and aggregation switches), Core Switches and Hosts.
        Typically it is defined in terms of the number of pods. For **k** Pods, there are:
        * k switches (each with k ports) in each pod;
        * $\frac{k}{2}^2$ core switches;
        * $\frac{k^3}{4}$ maximum hosts.
        ''')

    col1, col2 = st.columns(2)
    with col1:
        n_pods = st.slider("How many Pods?", min_value=2, max_value=10, value=2, step=2)

    cores = [f"Core_{x}" for x in range(int(n_pods / 2) ** 2)]
    pods = [f"Pod_{x}" for x in range(n_pods)]
    max_hosts = ((n_pods ** 3) // 4) // n_pods

    G = nx.Graph()
    for core, pod in product(cores, pods):
        G.add_edge(core, pod, weight=0)

    if max_hosts > 1:
        with col2:
            n_hosts = st.slider("How many Hosts per Pod?", min_value=1, max_value=max_hosts, value=1, step=1)
    else:
        n_hosts = 1
        with col2:
            st.write("Number of Hosts per Pod:", n_hosts)

    i = 0
    for pod in pods:
        for host in range(n_hosts):
            G.add_edge(pod, f"Host_{host + i}", weight=0)
        i += n_hosts

    return G


@st.fragment
def twin_graph():
    st.write(r'''
        A Twin-graph topology is a recursively constructed, server-centric interconnection model defined by twin pairs
        (nodes with identical neighborhoods). It is controlled by two primary parameters:
        * **n** — the total number of nodes in the graph;
        * **$\beta$ ∈ [0, 0.5, 1]** — a trade-off factor balancing:
            * lower maximum node degree ($\beta$ = 1);
            * lower network diameter ($\beta$ = 0);

        For a Twin graph of order n:
        * The number of links is fixed at 2n − 4;
        * The minimum possible diameter is 2, and in general, diameter ∈ [2, ⌊n⁄2⌋];
        * The minimum possible maximum degree is 2, and in practice, degree ∈ [2, n−1];
        Twin graphs are 2-geodetically-connected, ensuring two node-disjoint shortest paths between all non-adjacent nodes.
        ''')

    # st.image("Figures/twin-graph.jpg",
    #         caption="A Twin-Graph-Based Topology")

    col1, col2 = st.columns(2)
    with col1:
        n = st.slider("How many nodes?", min_value=4, max_value=16, value=4, step=1)
    with col2:
        beta = st.slider(r"Trade-off factor ($\beta$)", min_value=.0, max_value=1.0, value=.5, step=.5)

    G = heuristic_zscore_twin_graph(n, beta)

    return G


def create_base_twin_graph():
    G = nx.Graph()
    G.add_edges_from([("Host_0", "Host_1"), ("Host_1", "Host_2"), ("Host_2", "Host_3"), ("Host_3", "Host_0")], weight=0)
    return G


def find_twin_pairs(G):
    pairs = []
    for u, v in combinations(G.nodes, 2):
        nu = set(G.neighbors(u)) - {v}
        nv = set(G.neighbors(v)) - {u}
        if nu == nv:
            pairs.append((u, v))
    return pairs


def heuristic_zscore_twin_graph(n, beta=0.5):
    if n < 4:
        raise ValueError("n must be ≥ 4")
    if not (0 <= beta <= 1):
        raise ValueError("beta must be between 0 e 1")

    G = create_base_twin_graph()
    next_node = 4

    while G.number_of_nodes() < n:
        candidates = []
        for u, v in find_twin_pairs(G):
            G.add_node(f"Host_{next_node}")
            G.add_edges_from([(u, f"Host_{next_node}"), (v, f"Host_{next_node}")], weight=0)

            deg_max = max(dict(G.degree()).values())
            try:
                diam = nx.diameter(G)
            except nx.NetworkXError:
                diam = float('inf')

            candidates.append({
                "pair": (u, v),
                "deg": deg_max,
                "diam": diam
            })

            G.remove_node(f"Host_{next_node}")

        if not candidates:
            raise RuntimeError("No valid twin pairs found.")

        degs = np.array([c["deg"] for c in candidates])
        diams = np.array([c["diam"] for c in candidates])

        # Calculate Z-scores
        mean_deg, std_deg = np.mean(degs), np.std(degs)
        mean_diam, std_diam = np.mean(diams), np.std(diams)

        std_deg = std_deg if std_deg > 0 else 1
        std_diam = std_diam if std_diam > 0 else 1

        best_cost = float('inf')
        best_pair = None

        for c in candidates:
            z_deg = (c["deg"] - mean_deg) / std_deg
            z_diam = (c["diam"] - mean_diam) / std_diam
            cost = beta * z_deg + (1 - beta) * z_diam

            if cost < best_cost:
                best_cost = cost
                best_pair = c["pair"]

        # Aplica melhor expansão
        u, v = best_pair
        G.add_node(f"Host_{next_node}")
        G.add_edges_from([(u, f"Host_{next_node}"), (v, f"Host_{next_node}")], weight=0)
        next_node += 1

    return G

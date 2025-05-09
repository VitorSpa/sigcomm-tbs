import streamlit as st
import networkx as nx
from itertools import product

from aux_funcs import draw_graph

@st.fragment
def fat_tree():
    st.write(r'''
        A fat-tree topology is composed of Pods (edge and aggregation switches), Core Switches and Hosts.
        Typically it is defined in terms of the number of pods. For **k** Pods, there are:
        * k switches (each with k ports) in each pod;
        * $\frac{k}{2}^2$ core switches;
        * $\frac{k^3}{4}$ maximum hosts.
        ''')
    st.image("Figures/fat_tree_2.jpg",
             caption="A Fat Tree")

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

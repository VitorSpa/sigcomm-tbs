import streamlit as st

from comm_patterns import all_to_all
from network_topologies import fat_tree, draw_graph
import pandas as pd

if __name__ == '__main__':

    # Introduction

    with open("Sections/intro.md") as f:
        md_intro = f.read()
    st.write(md_intro)

    # Experiment Selection

    network_topo = st.selectbox(
        "Please select the topology you wish to use",
        ["Other", "Fat Tree"],
        index=None,
    )

    match network_topo:
        case "Fat Tree":
            G = fat_tree()
        case _:
            G = None

    # Graph Construction

    if G:
        comm_pattern = st.selectbox(
            "Please select the communication pattern you wish to use",
            ["Other", "All-to-All"],
            index=None,
        )
        transfer_size = st.slider("How much data per flow?", min_value=1, max_value=10, value=1, step=1)
        capacity_scaler = st.slider(r"Scaler value ($\alpha$)?", min_value=0.01, max_value=2.0, value=1.0, step=0.01)

        match comm_pattern:
            case "All-to-All":
                paths_lst = all_to_all(G, transfer_size, capacity_scaler)
            case _:
                paths_lst = None

        if paths_lst:
            df = pd.DataFrame(paths_lst, columns=["Host A", "Host B", "Path"])
            df["Flow_Id"] = range(len(df))
            st.write("Flow table:")
            st.dataframe(df)
            draw_graph(G, "Figures/fat_tree_weights.png", draw_weights=True)
            st.image("Figures/fat_tree_weights.png", caption="Tree")
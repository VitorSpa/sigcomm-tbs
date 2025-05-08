import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

from comm_patterns import all_to_all
from network_topologies import fat_tree, draw_graph
import pandas as pd
import plotly.express as px

if __name__ == '__main__':

    # Introduction

    with open("Sections/intro.md") as f:
        md_intro = f.read()
    st.write(md_intro)

    # Experiment Selection
    st.write("## Network Topology")
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
        with st.form("my_form"):
            st.write("## Parameter selection")
            transfer_size = st.number_input("How much data per flow (bits)?", min_value=0.0, value=1.0, format="%0.4f")
            capacity_scaler = st.number_input(r"Scaler value ($\alpha$)?", min_value=0.0, value=1.0, format="%0.4f")
            computation_time = st.number_input(r"Computation time (seconds)?", min_value=0.0, value=1.0, format="%0.4f")
            training_rounds = st.number_input(r"Number of training rounds?", min_value=1, value=1)

            submitted = st.form_submit_button("Submit")

        if submitted:
            paths_lst = all_to_all(G, transfer_size, capacity_scaler)

            df = pd.DataFrame(paths_lst, columns=["Host A", "Host B", "Path"])
            df["Flow_Id"] = range(len(df))
            st.write("## Flow table:")
            st.dataframe(df)
            #draw_graph(G, "Figures/fat_tree_weights.png", draw_weights=True)

            st.write("## Wasteless Design")
            #st.image("Figures/fat_tree_weights.png", caption="Tree")
            nt = Network('600px', '800px')
            nt.from_nx(G)
            for e in nt.edges:
                e['label'] = str(e['width'])
            nt.save_graph('Figures/graph.html')
            HtmlFile = open('Figures/graph.html', 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=600, width=800)

            st.write("## Metrics")
            flow_completion = transfer_size /  capacity_scaler
            st.write("Flow completion time: ", flow_completion, "second(s).")
            st.write("Training completion time: ", max(flow_completion, computation_time) * training_rounds,
                     "second(s).")

            st.write("## Computation & Communication Timeline")

            stops = [max(flow_completion, computation_time) * i for i in range(training_rounds)]
            comps = [(i, i + computation_time) for i in stops]
            comms = [(i, i + flow_completion) for i in stops]

            df1 = pd.DataFrame()
            df1["Start"] = [x for (x,y) in comps]
            df1["Finish"] = [y for (x, y) in comps]
            df1["Round"] = range(df1.shape[0])
            df1["Task"] = "Computation"

            df2 = pd.DataFrame()
            df2["Start"] = [x for (x,y) in comms]
            df2["Finish"] = [y for (x, y) in comms]
            df2["Round"] = range(df2.shape[0])
            df2["Task"] = "Communication"

            dff = pd.concat([df1, df2], ignore_index=True)
            dff['Delta'] = dff['Finish'] - dff['Start']

            fig = px.bar(dff, base="Start", x="Delta", y="Task", color="Round", orientation="h")
            st.plotly_chart(fig)
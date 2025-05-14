import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

from comm_patterns import all_to_all
from network_topologies import fat_tree, draw_graph
import pandas as pd
import plotly.express as px

if __name__ == '__main__':

    # Introduction
    st.set_page_config(layout="wide")

    with open("Sections/intro.md") as f:
        md_intro = f.read()
    st.write(md_intro)

    # Experiment Selection
    st.write("## Network Topology")
    network_topo = st.selectbox(
        "Select the topology",
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
            col1, col2 = st.columns(2)
            with col1:
                transfer_size = st.number_input("How much data per flow (bits)?", min_value=0.0, value=1.0, format="%0.4f")
                capacity_scaler = st.number_input(r"Scaler value ($\alpha$)?", min_value=0.0, value=1.0, format="%0.4f")
            with col2:
                computation_time = st.number_input(r"Computation time (seconds)?", min_value=0.0, value=1.0, format="%0.4f")
                training_rounds = st.number_input(r"Number of training rounds?", min_value=1, value=1)

            submitted = st.form_submit_button("Submit")

        if submitted:
            paths_lst = all_to_all(G, transfer_size, capacity_scaler)

            df = pd.DataFrame(paths_lst, columns=["Host A", "Host B", "Path"])
            df["Flow_Id"] = range(len(df))
            st.write("## Flow table:")
            st.dataframe(df, height=200)

            st.write("## Wasteless Design")
            nt = Network('500px', '700px')
            nt.from_nx(G)
            for e in nt.edges:
                e['label'] = str(round(e['width'], 2))
            for e in nt.edges:
                e['width'] = 2
            nt.save_graph('Figures/graph.html')
            HtmlFile = open('Figures/graph.html', 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, height=600, width=1000)
            st.write("## Computation & Communication Timeline ")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Transferring gradients/weights after computing")
                flow_completion = transfer_size / capacity_scaler

                stops = [(flow_completion + computation_time) * i for i in range(training_rounds)]
                comps = [(i, i + computation_time) for i in stops]
                comms = [(i + computation_time, i + computation_time + flow_completion) for i in stops[:-1]]
                st.write("Flow completion time: ", round(flow_completion, 2), "second(s).")
                st.write("Flow rate: ", round(transfer_size / flow_completion, 2), "bits/second.")
                st.write("Task completion time: ", round(comps[-1][-1], 2),
                         "second(s).")

                df1 = pd.DataFrame()
                df1["Start"] = [x for (x, y) in comps]
                df1["Finish"] = [y for (x, y) in comps]
                df1["Round"] = range(df1.shape[0])
                df1["Task"] = "Computation"

                df2 = pd.DataFrame()
                df2["Start"] = [x for (x, y) in comms]
                df2["Finish"] = [y for (x, y) in comms]
                df2["Round"] = range(df2.shape[0])
                df2["Task"] = "Communication"

                dff1 = pd.concat([df1, df2], ignore_index=True)
                dff1['Delta'] = dff1['Finish'] - dff1['Start']

                fig2 = px.bar(dff1, base="Start", x="Delta", y="Task", color="Task", orientation="h")
                st.plotly_chart(fig2)

                with col2:
                    st.write("Data transfer while computing")
                    flow_completion = transfer_size / capacity_scaler
                    st.write("Flow completion time: ", round(flow_completion, 2), "second(s).")
                    st.write("Flow rate: ", round(transfer_size/flow_completion, 2), "bits/second.")
                    st.write("Task completion time: ", round(max(flow_completion, computation_time) * training_rounds, 2),
                             "second(s).")

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

                    if computation_time == flow_completion:
                        dff2 = pd.concat([df1, df2], ignore_index=True)
                    elif computation_time < flow_completion:
                        df3 = pd.DataFrame()
                        df3["Start"] =  df1["Finish"]
                        df3["Finish"] = df2["Finish"]
                        df3["Round"] = range(df3.shape[0])
                        df3["Task"] = "Computation Idle"
                        dff2 = pd.concat([df1, df2, df3], ignore_index=True)
                    else:
                        df3 = pd.DataFrame()
                        df3["Start"] =  df2["Finish"]
                        df3["Finish"] = df1["Finish"]
                        df3["Round"] = range(df3.shape[0])
                        df3["Task"] = "Communication Idle"
                        dff2 = pd.concat([df1, df2, df3], ignore_index=True)
                    dff2['Delta'] = dff2['Finish'] - dff2['Start']

                    fig = px.bar(dff2, base="Start", x="Delta", y="Task", color="Task", orientation="h")
                    st.plotly_chart(fig)
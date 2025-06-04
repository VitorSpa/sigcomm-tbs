import plotly
import streamlit as st
import streamlit.components.v1 as components

from aux_funcs import draw_interactive_graph
from comm_patterns import weighted_shortest_path, shortest_path
from network_topologies import fat_tree, dragonfly, twin_graph, draw_graph, custom_topo
import pandas as pd
import plotly.express as px

if __name__ == '__main__':

    # Introduction
    st.set_page_config(layout="wide")

    with open("Sections/intro.md") as f:
        md_intro = f.read()
    st.write(md_intro)

    with st.expander("Theoretical Background"):
        with open("Sections/theory.md") as f:
            md_intro = f.read()
        st.write(md_intro)

    with st.expander("Instructions"):
        with open("Sections/instructions.md") as f:
            md_intro = f.read()
        st.write(md_intro)

    # Experiment Selection
    st.write("## Network Topology")
    network_topo = st.selectbox(
        "Select the topology",
        ["Custom", "Fat Tree", "Dragonfly", "Twin-Graph-Based"],
        index=None,
    )

    match network_topo:
        case "Fat Tree":
            G = fat_tree()
        case "Dragonfly":
            G = dragonfly()
        case "Twin-Graph-Based":
            G = twin_graph()
        case "Custom":
            G = custom_topo()
        case _:
            G = None

    # Graph Construction

    if G:
        with st.form("parameter_form"):
            st.write("## Parameter selection")

            routing_algo = st.selectbox(
                "Routing Algorithm:",
                ["None", "Shortest Path", "Weighted Shortest Path"],
                index=None,
            )
            col1, col2 = st.columns(2)
            with col1:
                transfer_size = st.number_input("How much data per flow (Gb):", min_value=0.0, value=1.0, format="%0.4f")
                capacity_scaler = st.number_input(r"Scaler value ($\alpha$):", min_value=0.0, value=1.0, format="%0.4f")
            with col2:
                computation_time = st.number_input(r"Computation time (seconds):", min_value=0.0, value=1.0, format="%0.4f")
                training_rounds = st.number_input(r"Number of training rounds:", min_value=1, value=1)

            submitted = st.form_submit_button("Submit")

        if submitted:
            match routing_algo:
                case "Shortest Path":
                    paths_lst = shortest_path(G, transfer_size, capacity_scaler)
                case "Weighted Shortest Path":
                    paths_lst = weighted_shortest_path(G, transfer_size, capacity_scaler)
                case _:
                    G = None

            df = pd.DataFrame(paths_lst, columns=["Host A", "Host B", "Path"])
            df["Flow_Id"] = range(len(df))

            st.write("## Wasteless Design")

            graph_code = draw_interactive_graph(G, 'Figures/graph.html', )
            components.html(graph_code, height=550, width=1400)

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
                dff1['Time'] = dff1['Finish'] - dff1['Start']

                fig2 = px.bar(dff1, base="Start", x="Time", y="Task", color="Task", orientation="h")
                fig2.update_layout(
                    font=dict(
                        family="Helvetica Bold",
                        size=25,  # Set the font size here
                    ),
                    showlegend=False
                )
                fig2.update_xaxes(title=dict(font=dict(family="Helvetica Bold", size=25)), tickfont=dict(family="Helvetica Bold", size=25))
                fig2.update_yaxes(title=dict(font=dict(family="Helvetica Bold", size=25)), tickfont=dict(family="Helvetica Bold", size=25))
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
                    dff2['Time'] = dff2['Finish'] - dff2['Start']

                    fig = px.bar(dff2, base="Start", x="Time", y="Task", color="Task", orientation="h")
                    fig.update_layout(
                        yaxis_title=None,
                        font=dict(
                            family="Helvetica Bold",
                            size=25,  # Set the font size here
                        ),
                        showlegend=False
                    )
                    fig.update_xaxes(title=dict(font=dict(family="Helvetica Bold", size=25)), tickfont=dict(family="Helvetica Bold", size= 25))
                    fig.update_yaxes(title=dict(font=dict(family="Helvetica Bold", size=25)), tickfont=dict(family="Helvetica Bold", size= 25))
                    st.plotly_chart(fig)

            st.write("## Flow table:")
            st.dataframe(df, height=200)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("india.csv")
list_of_states = list(df["State"].unique())
list_of_states.insert(0, "Overall India")

st.sidebar.title("India Data")

selected_state = st.sidebar.selectbox("select a state", list_of_states)
primary = st.sidebar.selectbox(
    "select Primary Parameter",
    sorted(
        df[
            ["Population", "Households_with_Internet", "sex_ratio", "literacy_rate"]
        ].columns
    ),
)
secondary = st.sidebar.selectbox(
    "select Secondary Parameter",
    sorted(
        df[
            ["Population", "Households_with_Internet", "sex_ratio", "literacy_rate"]
        ].columns
    ),
)

plot = st.sidebar.button("Plot Graph")
if plot:
    if selected_state == "Overall India":
        # plot for India
        fig = px.scatter_map(
            df,
            lat="Latitude",
            lon="Longitude",
            zoom=3,
            map_style='carto-positron',
            size=primary,
            color=secondary,
            color_continuous_scale="Turbo",
            height=700,
            width=1200,
            hover_name='District'
        )
        st.plotly_chart(fig,use_container_width=True)

    else:
        pass
        # kmc

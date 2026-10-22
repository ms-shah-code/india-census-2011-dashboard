import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("india.csv")
temp_df = (
    df.groupby("State name")["Population"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
pop = df[['Male','Female']].sum().reset_index()
pop.rename(columns={0:'pop'},inplace=True)

st.set_page_config(
    page_title="India Census Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sidebar
st.markdown(
    """
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
[data-testid="stMetric"]{
    padding: 0px;
}
[data-testid="stMetricLabel"]{
    color: #38bdf8;
    font-size: 16px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.html("""
    <style>
        body {
            background: black;
            margin: 0;
            padding: 0;
        }

        .sidebar {
            background: rgb(38 39 48);
            min-height: 98vh;
            width: 20vw;
            border-radius: 10px;
            margin: 7px;
            color: #fff;
        }

        .sidebar ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        nav ul li {
            margin: 10px;
        }

        .sidebar li a {
            color: #fff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 19px;
            padding: 10px 12px;
            transition: all 0.2s ease;
            border-radius: 6px;
        }

        .sidebar li a:hover {
            background: rgb(46 47 55);
            color: #ffffff;
        }

        .sidebar li a.active {
            background: rgb(58 59 73);
            color: white;
            box-shadow: 0 3px 12px rgb(33 33 39);
        }

        .icon {
            display: inline-flex;
            width: 25px;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            color: #35c5ff;
        }
    </style>
    <div class='sidebar'>
            <nav>

                <ul>
                    <li>
                        <a href="" class="active">
                            <span class="icon"><i class="fa-solid fa-house"></i></span>
                            Overview
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-users"></i></span>
                            Population
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-map-location-dot"></i></span>
                            States &amp; UTs
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-location-dot"></i></span>
                            Districts
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-book-open"></i></span>
                            Literacy
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-briefcase"></i></span>
                            Workforce
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-earth-asia"></i></span>
                            Religion
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-language"></i></span>
                            Language
                        </a>
                    </li>

                    <li>
                        <a href="">
                            <span class="icon"><i class="fa-solid fa-house-chimney"></i></span>
                            Households
                        </a>
                    </li>
                </ul>

            </nav>
        </div>
""")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Population",
        value="1,202,222,22,2",
        delta="6.6%",
        border=True,
        icon=":material/groups:",
    )
with col2:
    st.metric(
        label="Total Population",
        value="1,202,222,22,2",
        delta="6.6%",
        border=True,
        icon=":material/groups:",
    )
with col3:
    st.metric(
        label="Total Population",
        value="1,202,222,22,2",
        delta="6.6%",
        border=True,
        icon=":material/groups:",
    )
with col4:
    st.metric(
        label="Total Population",
        value="1,202,222,22,2",
        delta="6.6%",
        border=True,
        icon=":material/groups:",
    )
with col5:
    st.metric(
        label="Total Population",
        value="1,202,222,22",
        delta="6.6%",
        border=True,
        icon=":material/groups:",
    )

st.divider()

col_1, col_2, col_3 = st.columns([2, 2, 1])
with col_1:
    fig = px.scatter_map(
        df,
        lat="Latitude",
        lon="Longitude",
        zoom=3,
        map_style="carto-positron",
        color_continuous_scale="Turbo",
        hover_name="District",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig.update_layout(
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_2:
    fig = px.bar(
        temp_df,
        x="Population",
        y="State name",
        color="State name",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="State-wise Population(Top 10)",
    )
    fig.update_layout(
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_3:
    fig = px.pie(
        pop,
        values="pop",
        names="index",
        color_discrete_sequence=px.colors.qualitative.Bold,
        title="Male and Female Population",
        hole=0.5,
    )
    fig.update_layout(
        template="plotly_white",
        annotations=[
            dict(
                text=(
                    'Total Population<br>'
                    '<b>1.21 Billion</b>'
                ),
                x=0.5,
                y=0.5,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(
                    size=9,
                    color="#DCEBFF"
                ),
                align='center'
            )
        ]
    )
    st.plotly_chart(fig, use_container_width=True)
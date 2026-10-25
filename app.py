import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("india.csv")

# Cards
total_population = df["Population"].sum()
total_male_population = df["Male"].sum()
total_female_population = df["Female"].sum()
total_households = df["Households"].sum()
total_district = df["District"].size
male_per = total_male_population * 100 / total_population
female_per = total_female_population * 100 / total_population

temp_df = (
    df.groupby("State name")["Population"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
pop = df[["Male", "Female"]].sum().reset_index()
pop.rename(columns={0: "pop", "index": "Gender"}, inplace=True)

# plot Info
total_male_literate = df["Male_Literate"].sum()
total_female_literate = df["Female_Literate"].sum()

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
    background-color:#1b1e25;
}
[data-testid='stMetricValue']{
    font-size:30px;
}
[data-testid='stMetricIcon']{
    border:1px solid #48494d;
    border-radius:50%;
    padding:10px;
    height:30px;
    font-size:25px;
    width:30px;
    background-color:#48494d;
    color:#fff;
}
[data-testid="stMetricLabel"]{
    color: #fff;
    font-size: 25px;
}
[data-testid="stMetricLabel"] > div {
    margin:0;
    display: flex;
    gap:12px;
    align-items: center;
}
div[data-testid="stPlotlyChart"]{
    border: none;

}
div[data=testid='stVerticalBlockBorderWrapper']{
    border: 1px solid rgb(92, 228, 136);
    border-radius: 12px;
    background-color: black;
    padding: 12px;
    box_shadow: 0 0 8px rgba(37,131,255,0.08);
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
        value=total_population,
        delta="6.6%",
        border=True,
        icon=":material/groups:",
    )
with col2:
    st.metric(
        label="Male Population",
        value=total_male_population,
        delta_arrow="off",
        border=True,
        icon=":material/man:",
        delta=f"{male_per:.2f}%",
        delta_color="blue",
    )
with col3:
    st.metric(
        label="Female Population",
        value=total_female_population,
        border=True,
        icon=":material/woman:",
        delta_arrow="off",
        delta=f"{female_per:.2f}%",
        delta_color="yellow",
    )
with col4:
    st.metric(
        label="Total Households",
        value=total_households,
        delta_arrow="off",
        delta="2.5%",
        border=True,
        icon=":material/house:",
        delta_color="violet",
    )
with col5:
    st.metric(
        label="Total Districts",
        value=total_district,
        delta_arrow="off",
        delta="0.0%",
        border=True,
        icon=":material/location_city:",
        delta_color="grey",
    )

st.divider()

col_1, col_2 = st.columns([2, 2], gap="medium")
with col_1:
    with st.container(border=True):
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
    with st.container(border=True):
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

with st.container(border=True):
    fig = px.pie(
        pop,
        values="pop",
        names="Gender",
        title="Male and Female Population",
        color="Gender",
        color_discrete_map={"Male": "#6BA7F0", "Female": "#ED98FA"},
        hole=0.6,
        hover_name="Gender",
        hover_data='pop'
    )
    fig.update_traces(
        sort=False, marker=dict(line=dict(color="#07172D", width=3))
    )
    fig.update_layout(
        showlegend=False,
        annotations=[
            dict(
                text=(
                    f"<b>{total_population/1e9:.2f}Billion</b><br><sup>Total Population</sup>"
                ),
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=15, color="#DCEBFF"),
                align="center",
            )
        ],
    )
    st.plotly_chart(fig, use_container_width=True)

col_4, col_5 = st.columns([1.2, 1])

with col_4:
    with st.container(border=True):
        fig = px.pie(
            names=["Male", "Female"],
            values=[total_male_literate, total_female_literate],
            title="Literacy Rate",
            hole=0.65,
            color=["Male", "Female"],
            color_discrete_map={"Male": "#1887E9", "Female": "#8ABFEE"},
        )
        fig.update_traces(
            sort=False,
            marker=dict(line=dict(color="#07172D", width=3)),
        )
        fig.update_layout(
            showlegend=False,
            annotations=[
                dict(
                    text=f"<b>{((total_male_literate+total_female_literate)*100)/total_population:.2f}%</b><br><sup>Literacy Rate</sup>",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=20, color="gray"),
                )
            ],
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=22, b=15, l=5, r=5),
            height=250,
        )
        st.plotly_chart(fig, use_container_width=True)

with col_5:
    st.markdown(f"""

""")

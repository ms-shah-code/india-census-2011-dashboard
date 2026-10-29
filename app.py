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

Temp_df = df.groupby("State")["Agricultural_Workers"].sum().reset_index()
worker_df = df.groupby("State")[
    [
        "Workers",
        "Male_Workers",
        "Female_Workers",
        "Main_Workers",
        "Marginal_Workers",
        "Cultivator_Workers",
        "Agricultural_Workers",
    ]
].sum()

# plot Info
total_male_literate = df["Male_Literate"].sum()
total_female_literate = df["Female_Literate"].sum()
total_rural = df["Rural_Households"].sum()
total_urban = df["Urban_Households"].sum()
total_households = total_urban + total_rural
rural_percentage = total_rural * 100 / total_households
urban_percentage = total_urban * 100 / total_households

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
    background-color:#1d1f23;
}
[data-testid='stMetricValue']{
    font-size:30px;
    color:#fff;
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
div[data-testid='stVerticalBlockBorderWrapper']{
    border: 1px solid rgb(92, 228, 136);
    border-radius: 12px;
    background-color: black;
    padding: 12px;
    box_shadow: 0 0 8px rgba(37,131,255,0.08);
}

div[data-testid='stHorizontalBlock']{
    display: flex;
    align-items: center;
}
</style>
""",
    unsafe_allow_html=True,
)

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
        delta_color="inverse",
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
            size="Population",
            color="sex_ratio",
            color_continuous_scale="Turbo",
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
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    col_pie, col_info = st.columns([1.2, 1])
    with col_pie:
        fig = px.pie(
            values=[total_rural, total_urban],
            names=["Rural", "Urban"],
            title="Rural and Urban Population",
            color=["Rural", "Urban"],
            color_discrete_map={"Rural": "#976BF0", "Urban": "#22FB71"},
            hole=0.6,
        )
        fig.update_traces(sort=False, marker=dict(line=dict(color="#07172D", width=3)))
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
    with col_info:
        st.markdown(
            f"""
        <div class='main' style='
                display: flex;
                align-items: center;
                width: 100%;
                flex-direction: column;
                justify-content: center;
        '>
        <div class="info" style='display: flex;
                            align-items: center;
                            flex-direction: column;'>
            <div class="detail"
                style="
                    display: flex;
                    align-items: center;
                    gap: 20px;
                    margin: 15px;
                    margin-bottom:2px;
                        "
            >
                <div class="dot"
                    style="
                        height: 20px;
                        width: 20px;
                        border: 1px solid;
                        border-radius: 50%;
                        background: #22fb71;
                    "
                ></div>
                <div class='type'
                    style="
                            color: #4ae381;
                            font-size: 23px;
                    "
                >Rural</div>
                </div>
                <div style="display: flex;
                            margin-left: 80px;
                            flex-direction: column;
                            margin-top:-8px;
                            ">
                    <span style="font-size: 22px; color: #90f1b4;">{total_rural}</span>
                    <span style="font-size: 17px; color: #bfffd7;margin-top:-8px;">({rural_percentage:.2f}%)</span>
                </div>
            
        </div>
        <div class="info" style='display: flex;
                            align-items: center;
                            flex-direction: column;'>
                <div class="detail"
                    style="
                        display: flex;
                        align-items: center;
                        gap: 20px;
                        margin: 15px;
                        margin-bottom:2px;
                            "
                >
                    <div class="dot"
                        style="
                            height: 20px;
                            width: 20px;
                            border: 1px solid;
                            border-radius: 50%;
                            background: rgb(151 107 240);
                        "
                    ></div>
                    <div class='type'
                        style="
                                color: #ae8def;
                                font-size: 23px;
                        "
                    >Urban</div>
                    </div>
                    <div style="display: flex;
                                margin-left: 80px;
                                flex-direction: column;
                                margin-top:-8px;
                                ">
                        <span style="font-size: 22px; color: #c1acec;">{total_urban}</span>
                        <span style="font-size: 17px; color: #c1acec;margin-top:-8px;">({urban_percentage:.2f}%)</span>
                    </div>
            </div>
                
    """,
            unsafe_allow_html=True,
        )


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
        st.divider()
        st.markdown(
            f"""
        <div style="
                        display: flex;
                        align-items: center;
                        justify-content: space-around;
                        margin-bottom: 28px;
                ">

        <div class='card'
            style="
                display: flex;
                align-items: center;
                gap: 20px;
            "
        >
        <div>
        <i class='fa-solid fa-male' style='font-size:50px;color:#20A4F3;'></i>
        </div>
        <div style="
                display: flex;
                align-items: center;
                flex-direction: column;
                justify-content: center;
        ">
        <span style='font-size: 30px;color: #54bbf9;'>Male</span>
        <span style='font-size: 25px;color: #a2d1f8;'>{(total_male_literate*100)/total_population:.2f}%</span>
        </div>
        </div>

        <div class='card'
            style="
                display: flex;
                align-items: center;
                gap: 20px;
                "
        >
                <div>
                <i class='fa-solid fa-female' style='font-size:50px;color:#e515e7;'></i>
                </div>
                <div style="
                        display: flex;
                        align-items: center;
                        flex-direction: column;
                        justify-content: center;
                ">
                <span style='font-size: 30px;color: #e515e7;'>Female</span>
                <span style='font-size: 25px;color: #f293f3;'>{(total_female_literate*100)/total_population:.2f}%</span>
                </div>
                </div>
        </div>

""",
            unsafe_allow_html=True,
        )

with col_5:
    with st.container(border=True):
        fig = px.bar(
            Temp_df,
            x="State",
            y="Agricultural_Workers",
            color="State",
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig.update_traces(marker=dict(line=dict(color="#07172D", width=3)))
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=430,
            template="plotly_white",
        )
        fig.update_xaxes(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    fig = px.bar(
        worker_df,
        x=worker_df.index,
        y=worker_df.columns,
        barmode="stack",
        title="Workforce Composition",
    )
    fig.update_traces(marker=dict(line=dict(color="#07172D", width=2)))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=700
    )
    fig.update_xaxes(tickangle=-90)
    st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    state = st.selectbox(
        "select state:",
        options=df["State"].value_counts().index.sort_values().to_list(),
    )
    if state:
        district = st.selectbox(
            "select district:",
            options=df[df["State"] == state]["District"]
            .value_counts()
            .index.sort_values()
            .to_list(),
        )
        col_bar, col_pie = st.columns(2)
        with col_bar:
            with st.container(border=True):
                district_df = df[(df["State"] == state) & (df["District"] == district)][
                    ["Male", "Female"]
                ]
                district_df = district_df.melt(
                    value_vars=["Male", "Female"],
                    var_name="Gender",
                    value_name="Population",
                )
                fig = px.bar(
                    district_df,
                    x="Gender",
                    y="Population",
                    color="Gender",
                    color_discrete_map={"Male": "#3498DB", "Female": "#FC5BA9"},
                    title="District-wise Male vs Female Population",
                    text="Population",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
        with col_pie:
            with st.container(border=True):
                district_df = df[(df["State"] == state) & (df["District"] == district)][
                    ["Male_Literate", "Female_Literate"]
                ]
                district_df = district_df.melt(
                    value_vars=["Male_Literate", "Female_Literate"],
                    var_name="Gender",
                    value_name="Population",
                )
                fig = px.pie(
                    district_df,
                    names="Gender",
                    values="Population",
                    color="Gender",
                    color_discrete_map={
                        "Male_Literate": "#3498DB",
                        "Female_Literate": "#FC5BA9",
                    },
                    title="District-wise Male vs Female Literate Population",
                    hole=0.6,
                )
                fig.update_traces(
                    sort=False, marker=dict(line=dict(color="#07172D", width=3))
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
        # col_workers = st.columns(1)
        # with col_workers:
        with st.container(border=True):
            temp = df[(df["State"] == state) & (df["District"] == district)][
                [
                    "Male_Workers",
                    "Female_Workers",
                    "Main_Workers",
                    "Marginal_Workers",
                    "Non_Workers",
                    "Cultivator_Workers",
                    "Agricultural_Workers",
                    "Household_Workers",
                    "Other_Workers",
                ]
            ]
            temp = temp.melt(
                value_vars=[
                    "Male_Workers",
                    "Female_Workers",
                    "Main_Workers",
                    "Marginal_Workers",
                    "Non_Workers",
                    "Cultivator_Workers",
                    "Agricultural_Workers",
                    "Household_Workers",
                    "Other_Workers",
                ],
                var_name="Workers_type",
                value_name="Population",
            )
            fig = px.bar(
                temp,
                x="Workers_type",
                y="Population",
                color="Workers_type",
                title="District wise Workers Population",
                text="Population",
            )
            fig.update_xaxes(tickangle=-45)
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True)

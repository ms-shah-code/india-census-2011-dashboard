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
            showlegend=False,
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=700,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.50,
            xanchor="center",
            x=0.5,
            font=dict(size=10),
        ),
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

        # cards
        selected_df = df[(df["State"] == state) & (df["District"] == district)]

        total_population = selected_df["Population"].sum()
        total_male_population = selected_df["Male"].sum()
        total_female_population = selected_df["Female"].sum()
        total_households = selected_df["Households"].sum()
        total_workers = selected_df["Workers"].sum()

        def format_number(value):
            return f"{value:,.0f}"

        col1, col2, col3 = st.columns(3)

        with col1:
            with st.container(border=True):
                st.markdown("#### Population Overview")
                st.metric(
                    label="Total Population",
                    value=format_number(total_population),
                    icon=":material/groups:",
                    border=True,
                )

        with col2:
            with st.container(border=True):
                st.markdown("#### Male Demographics")
                st.metric(
                    label="Male Population",
                    value=format_number(total_male_population),
                    icon=":material/man:",
                    border=True,
                )

        with col3:
            with st.container(border=True):
                st.markdown("#### Female Demographics")
                st.metric(
                    label="Female Population",
                    value=format_number(total_female_population),
                    icon=":material/woman:",
                    border=True,
                )

        col4, col5 = st.columns(2)

        with col4:
            with st.container(border=True):
                st.markdown("#### Household Overview")
                st.metric(
                    label="Total Households",
                    value=format_number(total_households),
                    icon=":material/house:",
                    border=True,
                )

        with col5:
            with st.container(border=True):
                st.markdown("#### Workforce Overview")
                st.metric(
                    label="Total Workers",
                    value=format_number(total_workers),
                    icon=":material/work:",
                    border=True,
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
                    showlegend=False,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.20,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10),
                    ),
                    margin=dict(l=25, r=25, t=70, b=75),
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
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.20,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10),
                    ),
                    margin=dict(l=25, r=25, t=70, b=75),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)
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
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.99,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10),
                ),
            )
            st.plotly_chart(fig, use_container_width=True)
        with st.container(border=True):
            age_cols = [
                "Age_Group_0_29",
                "Age_Group_30_49",
                "Age_Group_50",
                "Age not stated",
            ]

            age_df = df.groupby("State")[age_cols].sum().reset_index()

            fig = px.bar(
                age_df,
                x="State",
                y=age_cols,
                title="State-wise Age Group Distribution",
                labels={
                    "value": "Population",
                    "variable": "Age Group",
                    "State": "State",
                },
                barmode="stack",
                color_discrete_sequence=["#38BDF8", "#818CF8", "#F472B6", "#94A3B8"],
            )

            fig.update_layout(
                template="plotly_white",
                xaxis_tickangle=-45,
                legend_title_text="Age Group",
                margin=dict(l=20, r=20, t=60, b=100),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.99,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10),
                ),
            )

            st.plotly_chart(fig, use_container_width=True)
        col_religion, col_cast = st.columns([1, 1.8])
        with col_religion:
            with st.container(border=True):
                religion_cols = [
                    "Hindus",
                    "Muslims",
                    "Sikhs",
                    "Christians",
                    "Buddhists",
                    "Jains",
                    "Others",
                ]

                religion_cols = [
                    col for col in religion_cols if col in selected_df.columns
                ]

                religion_data = selected_df[religion_cols].sum().reset_index()

                religion_data.columns = ["Religion", "Population"]

                religion_data = religion_data[religion_data["Population"] > 0]

                total_religion_population = religion_data["Population"].sum()

                fig = px.pie(
                    religion_data,
                    names="Religion",
                    values="Population",
                    hole=0.68,
                    color_discrete_sequence=[
                        "#38BDF8",
                        "#818CF8",
                        "#F472B6",
                        "#34D399",
                        "#FBBF24",
                        "#FB7185",
                        "#A78BFA",
                    ],
                )

                fig.update_traces(
                    textinfo="percent",
                    textposition="outside",
                    textfont=dict(size=11),
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Population: %{value:,.0f}<br>"
                        "Share: %{percent}"
                        "<extra></extra>"
                    ),
                    marker=dict(line=dict(color="rgba(128,128,128,0.2)", width=2)),
                )

                fig.update_layout(
                    title=dict(
                        text=f"Religion Distribution — {district}",
                        x=0.5,
                        xanchor="center",
                    ),
                    height=450,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.20,
                        xanchor="center",
                        x=0.5,
                        font=dict(size=10),
                    ),
                    margin=dict(l=25, r=25, t=70, b=75),
                    annotations=[
                        dict(
                            text=(
                                f"<b>{total_religion_population:,.0f}</b>" "<br>Total"
                            ),
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(size=16),
                        )
                    ],
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )

                st.plotly_chart(fig, use_container_width=True)

        with col_cast:
            with st.container(border=True):
                st.subheader("SC vs ST Population Analysis")
                st.caption(f"District: {district}, {state}")

                sc_st_cols = ["SC", "ST"]
                missing_cols = [
                    col for col in sc_st_cols if col not in selected_df.columns
                ]

                if missing_cols:
                    st.warning(f"Missing columns: {', '.join(missing_cols)}")
                else:
                    population_data = pd.DataFrame(
                        {
                            "Category": ["SC", "ST"],
                            "Population": [
                                selected_df["SC"].sum(),
                                selected_df["ST"].sum(),
                            ],
                        }
                    )

                    fig = px.bar(
                        population_data,
                        x="Category",
                        y="Population",
                        color="Category",
                        text="Population",
                        title="Scheduled Caste vs Scheduled Tribe Population",
                        color_discrete_map={"SC": "#38BDF8", "ST": "#F472B6"},
                    )

                    fig.update_traces(
                        texttemplate="%{text:,.0f}",
                        textposition="outside",
                        hovertemplate=(
                            "<b>%{x}</b><br>" "Population: %{y:,.0f}" "<extra></extra>"
                        ),
                    )

                    fig.update_layout(
                        height=350,
                        showlegend=False,
                        xaxis_title="Category",
                        yaxis_title="Population",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=20, r=20, t=65, b=30),
                    )

                    st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
            st.subheader("Water & Sanitation Analysis")
            st.caption(f"District: {district}, {state}")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    water_cols = [
                        "Main_source_of_drinking_water_Tapwater_Households",
                        "Main_source_of_drinking_water_Tubewell_Borehole_Households",
                        "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households",
                        "Main_source_of_drinking_water_Un_covered_well_Households",
                        "Main_source_of_drinking_water_Tank_Pond_Lake_Households",
                        "Main_source_of_drinking_water_River_Canal_Households",
                        "Main_source_of_drinking_water_Spring_Households",
                        "Main_source_of_drinking_water_Other_sources_Households",
                    ]

                    water_cols = [c for c in water_cols if c in selected_df.columns]

                    water_data = selected_df[water_cols].sum()

                    water_data = water_data[water_data > 0]

                    water_data.index = [
                        c.replace("Main_source_of_drinking_water_", "")
                        .replace("_Households", "")
                        .replace("_", " ")
                        for c in water_data.index
                    ]

                    water_data = water_data.reset_index()
                    water_data.columns = ["Water Source", "Households"]

                    if not water_data.empty:
                        fig = px.bar(
                            water_data,
                            x="Households",
                            y="Water Source",
                            orientation="h",
                            title="Households by Drinking Water Source",
                            text="Households",
                            color="Households",
                            color_continuous_scale="Blues",
                        )

                        fig.update_traces(
                            texttemplate="%{text:,.0f}",
                            textposition="outside",
                            hovertemplate=(
                                "<b>%{y}</b><br>"
                                "Households: %{x:,.0f}"
                                "<extra></extra>"
                            ),
                        )

                        fig.update_layout(
                            height=480,
                            showlegend=False,
                            coloraxis_showscale=False,
                            margin=dict(l=10, r=30, t=65, b=25),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                        )

                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Drinking water source columns not available.")

            with col2:
                with st.container(border=True):
                    sanitation_cols = [
                        "Having_latrine_facility_within_the_premises_Total_Households",
                        "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households",
                    ]

                    sanitation_cols = [
                        c for c in sanitation_cols if c in selected_df.columns
                    ]

                    sanitation_data = selected_df[sanitation_cols].sum()

                    sanitation_data = sanitation_data[sanitation_data > 0]

                    sanitation_labels = {
                        "Having_latrine_facility_within_the_premises_Total_Households": "Latrine within premises",
                        "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households": "No latrine / open alternative",
                    }

                    sanitation_data.index = [
                        sanitation_labels.get(c, c.replace("_", " "))
                        for c in sanitation_data.index
                    ]

                    sanitation_data = sanitation_data.reset_index()
                    sanitation_data.columns = ["Sanitation Facility", "Households"]

                    if not sanitation_data.empty:
                        fig = px.pie(
                            sanitation_data,
                            names="Sanitation Facility",
                            values="Households",
                            hole=0.62,
                            title="Household Sanitation Facilities",
                            color_discrete_sequence=["#34D399", "#FB7185"],
                        )

                        fig.update_traces(
                            textinfo="percent",
                            hovertemplate=(
                                "<b>%{label}</b><br>"
                                "Households: %{value:,.0f}<br>"
                                "Share: %{percent}"
                                "<extra></extra>"
                            ),
                            
                        )

                        fig.update_layout(
                            height=480,
                            showlegend=True,
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=-0.20,
                                xanchor="center",
                                x=0.5,
                                font=dict(size=10),
                            ),
                            margin=dict(l=25, r=25, t=70, b=75),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                        )

                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Sanitation columns not available.")

import random

import pandas as pd
import plotly.express as px
import streamlit as st

from .chart_utils import filter_df


def run(df: pd.DataFrame):
    X = df.columns
    Y = df.columns
    Z = list(df.select_dtypes(include=["int", "float"])) + [None]
    group_columns = list(df.columns) + [
        None
    ]

    # Select columns to visualize
    cols = st.columns([1, 1, 1, 1])
    char_container = st.container()
    kwargs = {
        "x": cols[0].selectbox("X", X),
        "y": cols[1].selectbox("Y", Y, index=1),
        "size": cols[2].selectbox("Z", Z, index=Z.index(None)),
        "color": cols[3].selectbox(
            "Group", group_columns, index=group_columns.index(None)
        ),
        "marginal_x": "histogram",
        "data_frame": df.copy()
    }
    with st.spinner("Querying data..."):
        if (
            kwargs["x"] != kwargs["y"]
            and kwargs["y"] != kwargs["color"]
        ):
            data = df.copy()
            data = filter_df(**kwargs)

            if kwargs["color"]:
                kwargs.update({"symbol": kwargs["color"]})
            if kwargs["size"]:
                kwargs.update({"size": data[kwargs["size"]].values.tolist()})
            kwargs.update({"data_frame": data})

            #Trend line
            kwargs.update({"trendline": st.selectbox("Trend line", [None, "ols", "lowess", "expanding"])})

            fig = px.scatter(**kwargs)
            fig.update_layout(font_size=14, autosize=True)
            char_container.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Please select different columns between X - Y - Z")

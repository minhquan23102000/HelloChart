import random

import pandas as pd
import plotly.express as px
import streamlit as st

from .chart_utils import filter_df


def run(df: pd.DataFrame):
    X = df.columns
    Y = df.columns
    group_columns = list(df.select_dtypes(include=["category", "object", "string"])) + [
        None
    ]

    # Select columns to visualize
    cols = st.columns([1, 1, 1])
    char_container = st.container()
    kwargs = {
        "x": cols[0].selectbox("Series", X),
        "y": cols[1].selectbox("Value", Y, index=1),
        "color": cols[2].selectbox("Group", group_columns, index=group_columns.index(None)),
        "markers": True,
        "data_frame": df.copy()
    }
    with st.spinner("Querying data..."):
        if (
            kwargs["x"] != kwargs["y"]
            and kwargs["y"] != kwargs["color"]
        ):
            data = df.copy()
            if not kwargs["color"]:
                data = (
                    data[[kwargs["x"], kwargs["y"]]]
                    .groupby([kwargs["x"]])
                    .sum()
                    .reset_index()
                )
                data.columns = [kwargs["x"], kwargs["y"]]
            else:
                data = (
                    data[[kwargs["x"], kwargs["color"], kwargs["y"]]]
                    .groupby([kwargs["x"], kwargs["color"]])
                    .sum()
                    .reset_index()
                )
                data.columns = [kwargs["x"], kwargs["color"], kwargs["y"]]

            kwargs.update({"data_frame": data})
            data = filter_df(**kwargs)
            # Line chart create figure
            kwargs.update({"data_frame": data})
            fig = px.line(**kwargs)
            fig.update_layout(font_size=14, autosize=True)
            char_container.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Please select different columns between X - Y or Y - Group")

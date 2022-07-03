
import random

import pandas as pd
import plotly.express as px
import streamlit as st

from .chart_utils import filter_df


def run(df: pd.DataFrame):
    X = [None] + list(df.select_dtypes(include=["category", "object", "string"]))
    Y = list(df.select_dtypes(include=['int','float']))
    group_columns = list(df.select_dtypes(include=["category", "object", "string"])) + [
        None
    ]

    # Select columns to visualize
    cols = st.columns([1, 1, 1, 1])
    char_container = st.container()
    kwargs = {
        "x": cols[0].selectbox("Class", X),
        "y": cols[1].selectbox("Value", Y, index=1),
        "color": cols[2].selectbox(
            "Group", group_columns, index=group_columns.index(None)
        ),
        "data_frame": df.copy()
    }
    with st.spinner("Querying data..."):
        if (
            kwargs["x"] != kwargs["y"]
            and kwargs["y"] != kwargs["color"]
        ):
            data = df.copy()
            data = filter_df(**kwargs)

            kwargs.update({"data_frame": data})
            # Hisfunct for barchart
            cols_bar_mode = st.columns([1,1])

            # Create figure
            fig = px.box(**kwargs)
            fig.update_layout(font_size=14, autosize=True)
            char_container.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Please select different columns between X - Y")

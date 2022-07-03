
import random

import pandas as pd
import plotly.express as px
import streamlit as st

from .chart_utils import filter_df


def run(df: pd.DataFrame):
    X = list(df.select_dtypes(include=["category", "object", "string"]))
    Y = list(df.select_dtypes(include=["float", "int"]))
    group_columns = list(df.select_dtypes(include=["category", "object", "string"])) + [
        None
    ]

    # Select columns to visualize
    cols = st.columns([1, 1, 1, 1])
    char_container= st.container()
    kwargs = {
        "names": cols[0].selectbox("Class", X),
        "values": cols[1].selectbox("Value", Y, index=1),
        "color": cols[2].selectbox(
            "Group", group_columns, index=group_columns.index(None)
        ),
        "data_frame": df.copy()
    }
    with st.spinner("Querying data..."):
        if (
            kwargs["names"] != kwargs["values"]
            and kwargs["values"] != kwargs["color"]
        ):
            data = df.copy()
            data = filter_df(**kwargs)

            kwargs.update({"data_frame": data})

            # Create figure
            fig = px.pie(**kwargs)
            fig.update_layout(font_size=14, autosize=True)
            char_container.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Please select different columns between X - Y")

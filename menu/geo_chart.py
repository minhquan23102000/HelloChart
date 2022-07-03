
import json
import random

import pandas as pd
import plotly.express as px
import streamlit as st

from .chart_utils import filter_df

GEO_JSON_PATH = {
    'vi': 'static/data/vi-geo.json'
}

def run(df: pd.DataFrame):
    X = df.columns
    Y = df.columns
    group_columns = list(df.select_dtypes(include=["category", "object", "string"])) + [
        None
    ]
    with open(GEO_JSON_PATH['vi'], 'r') as f:
        geojson = json.load(f)

    # Select columns to visualize
    cols = st.columns([1, 1, 1, 1])
    kwargs = {
        "locations": cols[0].selectbox("Locations", X),
        "color": cols[1].selectbox("Value", Y, index=1),
        "data_frame": df.copy(),
        "height": 700,
        "geojson": geojson
    }
    with st.spinner("Querying data..."):
            data = df.copy()
           # data = filter_df(**kwargs)

            kwargs.update({"data_frame": data})

            # Create figure
            fig = px.choropleth(**kwargs)
            fig.update_layout(font_size=14, autosize=True)
            st.plotly_chart(fig, use_container_width=True)


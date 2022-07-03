import glob

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

from menu import (bar_chart, box_chart, geo_chart, line_chart, pie_chart,
                  scatter_plot)
from utils import auto_format

st.set_page_config(
    page_title="Hello Chart - Visualize your excels",
    page_icon="🌠",
    layout='wide'
)

st.write("# Welcome to Hello Chart! 👋")

# Chart menu
chart_menu = {"Bar chart": bar_chart, "Scatter chart": scatter_plot, "Line chart": line_chart, "Pie chart": pie_chart, "Box chart": box_chart}
with st.sidebar:
    selected_chart = option_menu(
        "Select a chart",
        options=list(chart_menu.keys()),
        menu_icon=["calendar4-week"],
        icons=["bar-chart","bar-chart-steps", "graph-up", "pie-chart", 'box'],
    )

#st.sidebar.success("Select a chart above for visualization.")

st.markdown(
    """
    Import an excel and start explore data with Hello Chart!
    At here you can view all types chart like: bar, line, scatter, histogram and etc.
"""
)

# Get upload a excel file
upfile = st.file_uploader("Upload Excel", type=["xlsx", "csv", "xls"])
df = None

if upfile:
    # if file type is csv, then read csv
    if upfile.type == "text/csv":
        df = pd.read_csv(upfile)
    else:
        df = pd.read_excel(upfile)
else:
    #Get available_files in static data path
    available_files = glob.glob('static\data\*.csv')
    #File upload event
    file_select = st.sidebar.selectbox("You can also select a data from list bellow for demo", available_files)

    if file_select:
        df = pd.read_csv(file_select)

if df is not None:
    df = auto_format(df)
    df.info()

    # View sample data
    with st.expander("Sample data", expanded=True):
        n_samples = st.slider("Number of sample", 1, df.shape[0], value=20)
        st.dataframe(df.iloc[1:n_samples+1])

    # Visualization data with selected type chart
    chart_menu[selected_chart].run(df)

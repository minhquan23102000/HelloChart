from tokenize import group

import numpy as np
import pandas as pd
import streamlit as st


def filter_category(df, col, container):
    row = container.columns([1,1])
    exclude_group = row[0].multiselect(f"Exclue group of {col}", set(df[col]))
    include_group = row[1].multiselect(f"Inclue group of {col}", set(df[col]))
    if include_group:
        df = df.loc[df[col].isin(include_group)]
    if exclude_group:
        df = df.loc[~df[col].isin(exclude_group)]

    return df

def filter_number_date(df, col, container):
    if np.issubdtype(df[col].dtype, np.number):
        min_x, max_x = int(df[col].min()), int(df[col].max()) + 1
    else:
        min_x, max_x = df[col].min().to_pydatetime(), df[col].max().to_pydatetime()

    range_x = container.slider(
        col, min_value=min_x, max_value=max_x, value=(min_x, max_x)
    )
    filter_condition = (df[col] >= range_x[0]) & (df[col] <= range_x[1])
    df = df.loc[filter_condition]

    return df

def filter_df(**kwargs):
    container_1 = st.container()
    container_2 = st.container()
    df: pd.DataFrame = kwargs.pop("data_frame", None)
    x = kwargs.pop("x", None)
    y = kwargs.pop("y", None)
    z = kwargs.pop("size", None)
    group = kwargs.pop("color", None)

    if not x:
        x = kwargs.pop("names", None)
    if not y:
        y = kwargs.pop("values", None)

    if x:
        try:
            if df[x].dtype.name in ['category', 'object', 'string', 'char']:
                df = filter_category(df, x, container_1)
            else:
                df = filter_number_date(df, x, container_2)
        except Exception as e:
            print(str(e))
            pass
    if y:
        try:
            if df[y].dtype.name in ['category', 'object', 'string', 'char']:
                df = filter_category(df, y, container_1)
            else:
                df = filter_number_date(df, y, container_2)
        except:
            pass
    if z:
        try:
            if df[z].dtype.name in ['category', 'object', 'string', 'char']:
                df = filter_category(df, z, container_1)
            else:
                df = filter_number_date(df, z, container_2)
        except:
            pass
    if group:
        try:
           df = filter_category(df, group, container_1)
        except:
            pass
    return df

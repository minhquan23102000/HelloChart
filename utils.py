import re

import numpy as np
import pandas as pd
from dateutil import parser


def merge_date_feature(x, **kwargs):
    year = kwargs.get("year")
    month = kwargs.get("month")
    day = kwargs.get("day")
    hour = kwargs.get("hour")
    week = kwargs.get("week")
    date_str = ""
    if year:
        date_str += str(x[year]) + "-"
    if month:
        date_str += str(x[month]) + "-"
    if day:
        date_str += str(x[day]) + " "
    if hour:
        date_str += f"{x[hour]}"

    try:
        date_obj = parser.parse(date_str.strip().strip("-"))
    except Exception as e:
        date_obj = date_str
    return date_obj


def auto_format(df: pd.DataFrame):
    data = df.copy()
    kwargs = {}

    data.columns = [col.lower().strip() for col in data.columns]
    for col in data.columns:
        print(col)
        if str(col) in ["year", "month", "day", "hour"]:
            kwargs.update({col: col})
            continue
        if np.issubdtype(data[col].dtype,np.number) or not re.search(r"(date|time)", col):
            continue
        try:
            data[col] = data[col].apply(lambda x: parser.parse(str(x)))
        except Exception as e:
            print(e.__cause__, str(e))
            continue

    if kwargs:
        data["date_auto_merge"] = pd.to_datetime(data.apply(lambda x: merge_date_feature(x, **kwargs), axis=1))

    return data

import numpy as np
import pandas as pd
import streamlit as st
from pyparsing import ABC

from chart_utils import filter_df


class Chart(ABC):
    def __init__(self, data_frame:pd.DataFrame, x=True, y=True, z=False, group=True,  **kwargs):
        if x:
            self.X = data_frame[x].columns

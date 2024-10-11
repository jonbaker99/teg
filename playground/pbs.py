import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import altair as alt
from streamlit.utils import load_all_data, get_teg_rounds

all_data = load_all_data()

# filter out TEG == TEG 50
#all_data = all_data[all_data['TEG'] != 'TEG 50']


#exclude incomplete TEGs where count unique of rounds is less than get_teg_rounds()
all_data = all_data[all_data.groupby('TEG')['Round'].transform('nunique') == get_teg_rounds(all_data['TEG'].unique()[0])]

# print unique TEGs in all_data
print(all_data['TEG'].unique())

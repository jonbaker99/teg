import streamlit as st
import pandas as pd
import altair as alt
from utils import load_all_data, get_teg_rounds

all_data = load_all_data()

# filter out TEG == TEG 50
#all_data = all_data[all_data['TEG'] != 'TEG 50']


#exclude incomplete TEGs where count unique of rounds is less than get_teg_rounds()
all_data = all_data[all_data.groupby('TEG')['round'].transform('nunique') == get_teg_rounds(all_data['TEG'].unique()[0])]

# print unique TEGs in all_data
print(all_data['TEG'].unique())
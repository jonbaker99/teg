import streamlit as st
import pandas as pd
import plotly.express as px
from golf_data import player_scores, stableford_data, avg_score_by_par


# Assume we have the data from the previous example
# player_scores, stableford_data, avg_score_by_par

st.title('Golf Tournament Dashboard')

# Data Table
st.header('Player Scores')
st.dataframe(player_scores)

# Line Chart
st.header('Stableford Race')
fig_line = px.line(stableford_data, x=stableford_data.index, y=stableford_data.columns,
                   labels={'index': 'Hole number', 'value': 'Stableford Points'},
                   title='Stableford Race')
st.plotly_chart(fig_line)

# Bar Chart
st.header('Average Score by Par')
fig_bar = px.bar(avg_score_by_par.melt(id_vars=['Player'], var_name='Par', value_name='Score'),
                 x='Player', y='Score', color='Par', barmode='group',
                 labels={'Score': 'Avg. Score over Par'},
                 title='Average Score by Par')
st.plotly_chart(fig_bar)
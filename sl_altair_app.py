import streamlit as st
import pandas as pd
import altair as alt

# Load data only once using Streamlit's caching mechanism
@st.cache_data 
def load_data():
    return pd.read_csv(r'data/teg-test-cumulation.csv')  # Or use Google Sheets if needed

# Data is only loaded once and cached
df = load_data()

# Dropdown to select 'TEG'
selected_teg = st.selectbox("Select TEG", df['TEG'].unique())

# Filter data based on dropdown selection
filtered_data = df[df['TEG'] == selected_teg]

# Create an Altair chart
chart = alt.Chart(filtered_data).mark_bar().encode(
    x='Pl',
    y='Sc'
).properties(
    title=f"Sum of 'Sc' by 'Pl' for TEG {selected_teg}"
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

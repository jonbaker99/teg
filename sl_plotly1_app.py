import pandas as pd
import streamlit as st
import plotly.express as px

# Load data only once using Streamlit's caching mechanism
@st.cache_data 
def load_data():
    return pd.read_csv(r'data/teg-test-cumulation.csv')  # Or use Google Sheets if needed

# Data is only loaded once and cached
df = load_data()


# Dropdown for selecting 'TEG'
selected_teg = st.selectbox("Select TEG", df['TEG'].unique())

# Filter the data based on the selected TEG
filtered_data = df[df['TEG'] == selected_teg]

# Group by 'Pl' and calculate the sum of 'Sc'
grouped_data = filtered_data.groupby('Pl')['Sc'].sum().reset_index()

# Create a Plotly bar chart
fig = px.bar(grouped_data, x='Pl', y='Sc', title=f"Sum of 'Sc' by 'Pl' for TEG {selected_teg}")

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

'TEST RANDOM TEXT'

# Sample pivot_table
pivot_table = pd.DataFrame({
    'Rank': [1, 2, 3, 4, 5],
    'Pl': ['GW', 'AB', 'JB', 'DM', 'HM'],
    '1': [38, 30, 34, 30, 29],
    '2': [41, 36, 34, 36, 27],
    '3': [29, 32, 35, 26, 34],
    '4': [41, 39, 28, 34, 21],
    'Total': [149, 137, 131, 126, 111]
})


st.dataframe(pivot_table.reset_index(drop=True))

# Format table with gradient
styled_df = pivot_table.style.background_gradient(subset=['Total'], cmap='Blues')


# Display the table with Streamlit
st.dataframe(styled_df.style.hide(axis='index'))
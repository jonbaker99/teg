import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Step 1: Load the data once (from CSV or Google Sheets)
df = pd.read_csv(r'data/teg-test-cumulation.csv')  # Or use Google Sheets if needed

# Step 2: Create a Plotly chart with direct dropdown
fig = go.Figure()

# Add traces for each unique TEG value
for teg in df['TEG'].unique():
    filtered_data = df[df['TEG'] == teg]
    grouped_data = filtered_data.groupby('Pl')['Sc'].sum().reset_index()
    fig.add_trace(go.Bar(x=grouped_data['Pl'], y=grouped_data['Sc'], name=f'TEG {teg}'))

# Add the dropdown menu to toggle between different TEGs
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[dict(method='update', label=teg, 
                          args=[{'visible': [teg == df['TEG'].unique()[i] for i in range(len(df['TEG'].unique()))]}]) 
                     for teg in df['TEG'].unique()],
            direction="down",
            showactive=True
        )
    ],
    title="Sum of 'Sc' by 'Pl' for each TEG"
)

# Step 3: Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

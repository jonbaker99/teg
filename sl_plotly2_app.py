import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# Sample data
data = {
    'TEG': ['A', 'A', 'B', 'B'],
    'Pl': ['Player 1', 'Player 2', 'Player 1', 'Player 2'],
    'Sc': [10, 20, 15, 25]
}

df = pd.DataFrame(data)


# Create an empty figure
fig = go.Figure()

# Loop through the unique 'TEG' values and add traces for each
for teg in df['TEG'].unique():
    filtered_data = df[df['TEG'] == teg]
    grouped_data = filtered_data.groupby('Pl')['Sc'].sum().reset_index()
    fig.add_trace(go.Bar(x=grouped_data['Pl'], y=grouped_data['Sc'], name=f'TEG {teg}'))

# Add dropdown for selecting TEG
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[dict(method='update', label=teg, args=[{'visible': [teg == df['TEG'].unique()[i] for i in range(len(df['TEG'].unique()))]}]) for teg in df['TEG'].unique()],
            direction="down",
            showactive=True
        )
    ],
    title="Sum of 'Sc' by 'Pl' for each TEG"
)

# Streamlit display of Plotly figure
st.plotly_chart(fig, use_container_width=True)


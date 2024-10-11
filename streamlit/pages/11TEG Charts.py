import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

def add_round_annotations(fig, max_round):
    for round_num in range(1, max_round + 1):
        x_pos = (round_num - 1) * 18
        fig.add_vline(x=x_pos, line=dict(color='lightgrey', width=1))
        fig.add_annotation(x=x_pos + 9, y=0.11, text=f'Round {round_num}', 
                           showarrow=False, yref='paper', yshift=-40)

def create_cumulative_graph(df, chosen_teg, cumulative_column, title):
    # Filter data based on the chosen TEG
    teg_data = df[df['TEG'] == chosen_teg].sort_values(['Round', 'Hole'])
    teg_data['x_value'] = (teg_data['Round'] - 1) * 18 + teg_data['Hole']  # Create x-axis value based on rounds and holes

    max_round = teg_data['Round'].max()
    x_axis_max = max_round * 18

    fig = go.Figure()

    # Generate color palette for players
    colors = px.colors.qualitative.Plotly[:len(teg_data['Pl'].unique())]
    color_map = dict(zip(teg_data['Pl'].unique(), colors))

    traces = []
    for player in teg_data['Pl'].unique():
        player_data = teg_data[teg_data['Pl'] == player]
        traces.append(go.Scatter(
            x=player_data['x_value'],
            y=player_data[cumulative_column],  # Use the pre-existing cumulative column
            mode='lines',
            name=player,
            line=dict(width=2),
        ))

    fig.add_traces(traces)

    fig.update_layout(
        title=title,
        xaxis_title='Rounds',
        yaxis_title=f'Cumulative {cumulative_column}',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, traceorder='normal', itemsizing='constant'),
        margin=dict(r=100)
    )

    add_round_annotations(fig, max_round)

    fig.update_xaxes(tickvals=[], range=[0, x_axis_max])

    for trace in fig.data:
        player = trace.name
        color = color_map[player]
        fig.update_traces(selector=dict(name=player), line=dict(color=color))

    return fig

def main():
    st.set_page_config(page_title="Cumulative Golf Scores", page_icon="⛳", layout="wide")
    
    st.title("Cumulative Golf Scores")

    df = load_data(r'../data/all-data.parquet')

    teg_order = df[['TEG', 'TEGNum']].drop_duplicates().sort_values('TEGNum')
    tegs = teg_order['TEG'].tolist()

    chosen_teg = st.radio('Select TEG', tegs, horizontal=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Cumulative GrossVP for {chosen_teg}")
        fig_grossvp = create_cumulative_graph(df, chosen_teg, 'GrossVP Cum TEG', f'Cumulative GrossVP for {chosen_teg}')
        st.plotly_chart(fig_grossvp, use_container_width=True)

    with col2:
        st.subheader(f"Cumulative Stableford for {chosen_teg}")
        fig_stableford = create_cumulative_graph(df, chosen_teg, 'Stableford Cum TEG', f'Cumulative Stableford for {chosen_teg}')
        st.plotly_chart(fig_stableford, use_container_width=True)

if __name__ == "__main__":
    main()

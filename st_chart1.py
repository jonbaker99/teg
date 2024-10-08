import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

def create_cumulative_graph(df, chosen_teg, value_column, title):
    teg_data = df[df['TEG'] == chosen_teg]
    teg_data = teg_data.sort_values(['Round', 'Hole'])
    teg_data['x_value'] = (teg_data['Round'] - 1) * 18 + teg_data['Hole']
    teg_data[f'Cumulative_{value_column}'] = teg_data.groupby('Pl')[value_column].cumsum()
    
    fig = go.Figure()
    
    for player in teg_data['Pl'].unique():
        player_data = teg_data[teg_data['Pl'] == player]
        last_point = player_data.iloc[-1]
        
        fig.add_trace(go.Scatter(
            x=player_data['x_value'],
            y=player_data[f'Cumulative_{value_column}'],
            mode='lines',
            name=player,
            line=dict(width=2),
            #marker=dict(size=6, symbol='circle'),
        ))
        
        # Add label and circle marker for the last point
        fig.add_trace(go.Scatter(
            x=[last_point['x_value']],
            y=[last_point[f'Cumulative_{value_column}']],
            mode='markers+text',
            #marker=dict(size=10, symbol='circle-open', line=dict(width=2)),
            marker=dict(size=6, symbol='circle'),
            text=f"{player}: {last_point[f'Cumulative_{value_column}']:.0f}",
            textposition="middle right",
            showlegend=False
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Rounds',
        yaxis_title=f'Cumulative {value_column}',
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add vertical lines for round breaks and axis labels
    for round_num in range(1, 5):
        x_pos = (round_num - 1) * 18
        fig.add_vline(x=x_pos, line=dict(color='lightgrey', width=1))
        fig.add_annotation(x=x_pos + 9, y=0.11, text=f'Round {round_num}', 
                           showarrow=False, yref='paper', yshift=-40)

    fig.update_xaxes(tickvals=[], range=[-1, 73])
    
    return fig

def main():
    st.set_page_config(page_title="Cumulative Golf Scores", page_icon="⛳", layout="wide")
    
    st.title("Cumulative Golf Scores")

    df = load_data(r'data/teg-all-data-long.csv')

    teg_order = df[['TEG', 'TEGNum']].drop_duplicates().sort_values('TEGNum')
    tegs = teg_order['TEG'].tolist()
    
    # Change from selectbox to radio buttons
    chosen_teg = st.radio('Select TEG', tegs, horizontal=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Cumulative GrossVP for {chosen_teg}")
        fig_grossvp = create_cumulative_graph(df, chosen_teg, 'GrossVP', f'Cumulative GrossVP for {chosen_teg}')
        st.plotly_chart(fig_grossvp, use_container_width=True)

    with col2:
        st.subheader(f"Cumulative Stableford for {chosen_teg}")
        fig_stableford = create_cumulative_graph(df, chosen_teg, 'Stableford', f'Cumulative Stableford for {chosen_teg}')
        st.plotly_chart(fig_stableford, use_container_width=True)

if __name__ == "__main__":
    main()
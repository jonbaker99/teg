import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

def add_round_annotations(max_round):
    annotations = []
    for round_num in range(1, max_round + 1):
        x_pos = (round_num - 1) * 18
        annotations.append({
            'x': x_pos + 9,
            'y': 0,
            'text': f'Round {round_num}'
        })
    return annotations

def create_cumulative_graph(df, chosen_teg, cumulative_column, title):
    # Filter data based on the chosen TEG
    teg_data = df[df['TEG'] == chosen_teg].sort_values(['Round', 'Hole'])
    teg_data['x_value'] = (teg_data['Round'] - 1) * 18 + teg_data['Hole']  # Create x-axis value based on rounds and holes
    
    max_round = teg_data['Round'].max()

    # Create Altair chart
    chart = alt.Chart(teg_data).mark_line().encode(
        x=alt.X('x_value', title='Rounds'),
        y=alt.Y(cumulative_column, title=f'Cumulative {cumulative_column}'),
        color='Pl:N',  # Color by player
        tooltip=['Pl', cumulative_column]  # Show player and cumulative value on hover
    ).properties(
        title=title,
        width=600,
        height=400
    )

    # Add round annotations (using vertical rules)
    round_annotations = alt.Chart(pd.DataFrame(add_round_annotations(max_round))).mark_text(
        dy=-10,
        align='center'
    ).encode(
        x='x:Q',
        text='text:N'
    )

    return chart + round_annotations

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
        alt_grossvp = create_cumulative_graph(df, chosen_teg, 'GrossVP Cum TEG', f'Cumulative GrossVP for {chosen_teg}')
        st.altair_chart(alt_grossvp, use_container_width=True)

    with col2:
        st.subheader(f"Cumulative Stableford for {chosen_teg}")
        alt_stableford = create_cumulative_graph(df, chosen_teg, 'Stableford Cum TEG', f'Cumulative Stableford for {chosen_teg}')
        st.altair_chart(alt_stableford, use_container_width=True)

if __name__ == "__main__":
    main()

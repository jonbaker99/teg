import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils import load_all_data
from make_charts import create_cumulative_graph


def main():
    st.set_page_config(page_title="Cumulative Golf Scores", page_icon="⛳", layout="wide")
    
    st.title("Cumulative Golf Scores")

    df = load_all_data(exclude_teg_50=True)

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

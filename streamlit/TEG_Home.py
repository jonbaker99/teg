import streamlit as st

st.set_page_config(
    page_title="TEG STATS",
    #page_icon="👋",
)

st.write("# The El Golfo stats & records")

#st.sidebar.success("Select a demo above.")

st.markdown(
    """
    ### Contents (use sidebar)
    1. TEG History
      a) Winners by year
      b) Results tables by TEG
        - Race for the title charts
    2. TEG Records
        a) Best TEGs, Rounds and 9s
        b) Top n TEGs and Rounds
        c) Personal Bests
        d) Other Records
    3. TEG Scoring
        a) Score by Par
        b) Career Eagles, Birdies and Pars
        c) Most birdies etc. in a round
        d) Best Streaks
    4. Current TEG info
        a) Leaderboard
        b) Latest round
        c) Data update
   
"""
)
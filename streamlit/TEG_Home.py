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
    1. **TEG History**
        - Winners by year
        - Results tables by TEG
        - Race for the title charts
      
    2. **TEG Records**
        - Best TEGs, Rounds and 9s
        - Top n TEGs and Rounds
        - Personal Bests
        - Other Records
      
    3. **TEG Scoring**
        - Score by Par
        - Career Eagles, Birdies and Pars
        - Most birdies etc. in a round
        - Best Streaks
      
    4. **Current TEG info**
        - Leaderboard
        - Latest round
        - Data update
   
"""
)
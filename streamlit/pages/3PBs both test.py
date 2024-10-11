import streamlit as st
import pbs
import pb_rounds    

# Set the page configuration
st.set_page_config(page_title="Tabbed Interface with Different Files", layout="wide")

# Create tabs for the interface
tab1, tab2, tab3 = st.tabs(["TEG", "Round", "Tab 3"])

# Add content to each tab by calling the respective function
with tab1:
    pbs.show()

with tab2:
    pb_rounds.show()

with tab3:
    'NOTHING HERE'
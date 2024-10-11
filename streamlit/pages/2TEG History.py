import streamlit as st
import pandas as pd
from utils import load_all_data, get_teg_winners

# Streamlit app starts here
st.title('TEG History')

# Load all data using the function from utils.py
all_data = load_all_data()

# Generate the TEG winners summary using the function from utils.py
teg_winners = get_teg_winners(all_data)

# Display the TEG winners DataFrame in Streamlit without the index
st.write(teg_winners.to_html(index=False, justify='left'), unsafe_allow_html=True)

# Display the caption with extra details
st.caption('*Green Jacket awarded in TEG 5 for best stableford round; DM had best gross score')

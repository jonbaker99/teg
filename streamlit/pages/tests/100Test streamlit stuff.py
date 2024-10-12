import streamlit as st, pandas as pd

# Constants
FILE_PATH = '../data/all-data.parquet'

# df = pd.read_parquet(FILE_PATH)
# data = df[df['TEGNum']==16]

# # Insert containers separated into tabs:
# tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
# tab1.write("this is tab 1")
# tab2.write("this is tab 2")

# # You can also use "with" notation:
# with tab1:
#    st.radio('Select one:', [1, 2])



# # st.balloons()
# # st.snow()
# st.toast('Mr Stay-Puft')
# st.error('Error message')
# st.warning('Warning message')
# st.info('Info message')
# st.success('Success message')

# st.sidebar.write("HELLO")

import streamlit as st
import pandas as pd
import numpy as np
import time

df = pd.DataFrame(np.random.randn(15, 3), columns=(["A", "B", "C"]))
my_data_element = st.line_chart(df)

for tick in range(10):
    time.sleep(.5)
    add_df = pd.DataFrame(np.random.randn(1, 3), columns=(["A", "B", "C"]))
    my_data_element.add_rows(add_df)

st.button("Regenerate")
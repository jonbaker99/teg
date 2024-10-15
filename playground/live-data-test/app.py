import streamlit as st
import pandas as pd
import numpy as np
import os

# Function to generate random data
def generate_data():
    return pd.DataFrame({
        'A': np.random.rand(100),
        'B': np.random.rand(100),
        'C': np.random.rand(100),
        'D': np.random.rand(100),
        'E': np.random.rand(100)
    })

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = generate_data()

# Streamlit app
st.title("Random Data Generator with Datawrapper Integration")

# Button to regenerate data
if st.button("Regenerate Data"):
    st.session_state.data = generate_data()
    st.success("Data regenerated!")

# Display the data
st.subheader("Generated Data")
st.dataframe(st.session_state.data)

# Button to save data to CSV
if st.button("Save Data to CSV"):
    csv = st.session_state.data.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='random_data.csv',
        mime='text/csv',
    )
    st.success("Data prepared for download!")

# Display Datawrapper chart
st.subheader("Datawrapper Chart")
st.markdown("Note: Replace this with your actual Datawrapper embed code")
datawrapper_embed_code = """
<iframe title="Live updating chart?" aria-label="Bar Chart" id="datawrapper-chart-x63Hk" src="https://datawrapper.dwcdn.net/x63Hk/1/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="161" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r=0;r<e.length;r++)if(e[r].contentWindow===a.source){var i=a.data["datawrapper-height"][t]+"px";e[r].style.height=i}}}))}();
</script>
"""
st.components.v1.html(datawrapper_embed_code, height=400)
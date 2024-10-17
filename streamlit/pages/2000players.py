import os
import streamlit as st
from pathlib import Path
from streamlit_extras.stylable_container import stylable_container

st.write('TEMPORARY PAGE')

# # Print current working directory
# current_dir = Path.cwd()
# st.write(f"Current working directory: {current_dir}")

# # List all files and folders in the current directory
# st.write("Files and directories in current directory:")
# for path in current_dir.iterdir():
#     st.write(path)


import pandas as pd

# Sample DataFrame
data = {
    'Player': ['John', 'Alice', 'Bob'],
    'Score': [10, 15, 12]
}

df = pd.DataFrame(data)
df = df.reset_index(drop=True)

# Apply Pandas Styler to left-align the 'Player' column
styled_df = df.style.set_properties(subset=['Player'], **{'text-align': 'left'})

with stylable_container(
    key="container_with_border",
    css_styles="""
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """,
):
    st.markdown("This is a container with a border.")
    st.write(styled_df.to_html(index=False, classes='datawrapper-table'), unsafe_allow_html=True)

# Display the styled DataFrame (in a Jupyter environment or export to HTML)
'index = false'

# 'no index false'
# st.write(styled_df.to_html(classes='datawrapper-table'), unsafe_allow_html=True)

# st.markdown(styled_df.to_html)
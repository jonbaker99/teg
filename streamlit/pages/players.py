import os
import streamlit as st
from pathlib import Path

st.write('TEMPORARY PAGE')

# Print current working directory
current_dir = Path.cwd()
st.write(f"Current working directory: {current_dir}")

# List all files and folders in the current directory
st.write("Files and directories in current directory:")
for path in current_dir.iterdir():
    st.write(path)
import streamlit as st
import pandas as pd
import random

def create_stat_section(title, value=None, df=None):
    # Create the title and value part
    title_html = f"<h2><span class='title'>{title}</span>"
    if value is not None:
        title_html += f"<span class='value'> {value}</span>"
    title_html += "</h2>"
    
    # Create the details part from the DataFrame
    details_html = ""
    if df is not None and not df.empty:
        rows = []
        for _, row in df.iterrows():
            row_str = " • ".join(f"<span class='{col}'>{row[col]}</span>" for col in df.columns)
            rows.append(f"<strong>{row_str}</strong>")
        details_html = "<br>".join(rows)
    
    # Combine all parts
    return f"""
    <div class="stat-section">
        {title_html}
        <div class="stat-details">
            {details_html}
        </div>
    </div>
    """

# Set page config
st.set_page_config(page_title="Golf Stats", page_icon="⛳", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    div[data-testid="column"] {
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 20px;
        height: 100%;
    }
    div[data-testid="column"]:first-child {
        margin-right: 20px;
        border-right: 1px solid #ccc;
        padding-right: 40px;
    }
    div[data-testid="column"]:last-child {
        margin-left: 20px;
        padding-left: 40px;
    }
    .stat-section {
        margin-bottom: 20px;
        background-color: rgb(240, 242, 246);
        padding: 20px;
        margin: 5px;
    }
    .stat-section h2 {
        margin-bottom: 5px;
        font-size: 22px;
        line-height: 1.0;
        color: #333;
        padding: 0;
    }
    .stat-section h2 .title {
        font-weight: normal;
    }
    .stat-section h2 .value {
        font-weight: bold;
    }
    .stat-details {
        font-size: 14px;
        color: #666;
        line-height: 1.4;
    }
    .stat-details .name {
        font-weight: bold;
    }
    .stat-details .course {
        font-style: italic;
    }
    .stat-details .year {
        color: #999;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Page Title")

# Create 2 columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("TEG Records")

with col2:
    st.subheader("Round Records")

# Function to generate random data
def generate_random_data(num_rows):
    names = ["John Smith", "Emma Johnson", "Michael Brown", "Olivia Davis", "William Wilson", "Sophia Taylor", "James Anderson", "Ava Thomas", "Robert Jackson", "Isabella White"]
    courses = ["Pebble Beach", "St Andrews", "Augusta National", "Royal Melbourne", "Pinehurst No. 2", "Muirfield", "Oakmont", "Valderrama", "Whistling Straits", "Turnberry"]
    years = [str(year) for year in range(2010, 2024)]
    
    data = []
    for _ in range(num_rows):
        data.append({
            "name": random.choice(names),
            "course": random.choice(courses),
            "year": random.choice(years)
        })
    return pd.DataFrame(data)

# Function to fill a column with stat sections
def fill_column(column):
    with column:
        st.markdown(create_stat_section("Best Score", "25", generate_random_data(2)), unsafe_allow_html=True)
        st.markdown(create_stat_section("Best Other Thing", "89", generate_random_data(1)), unsafe_allow_html=True)
        st.markdown(create_stat_section("And Another Thing", "+7", generate_random_data(1)), unsafe_allow_html=True)

# Fill both columns with different content
fill_column(col1)
fill_column(col2)
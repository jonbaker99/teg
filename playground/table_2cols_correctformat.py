import streamlit as st
import random

def format_section(title, details, value):
    return f"""
    <div class="stat-section">
        <h2><span class='title'>{title}</span><span class='value'> {value}</span></h2>
        <div class="stat-details">
            {details}
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

# Function to create a stat section within a column
def create_stat_column(column, title, details, value):
    with column:
        st.markdown(format_section(title, details, value), unsafe_allow_html=True)

# Function to generate random names and courses
def generate_random_data(num_entries=1):
    names = ["John Smith", "Emma Johnson", "Michael Brown", "Olivia Davis", "William Wilson", "Sophia Taylor", "James Anderson", "Ava Thomas", "Robert Jackson", "Isabella White"]
    courses = ["Pebble Beach", "St Andrews", "Augusta National", "Royal Melbourne", "Pinehurst No. 2", "Muirfield", "Oakmont", "Valderrama", "Whistling Straits", "Turnberry"]
    years = [str(year) for year in range(2010, 2024)]
    
    entries = []
    for _ in range(num_entries):
        name = random.choice(names)
        course = random.choice(courses)
        year = random.choice(years)
        entries.append(f"<strong>{name}</strong> ({course}, {year})")
    
    return "<br>".join(entries)

# Function to fill a column with all stat sections
def fill_column(column):
    create_stat_column(column, "Best Score", generate_random_data(2), "25")  # Two entries for a tie
    create_stat_column(column, "Best Other Thing", generate_random_data(1), "89")
    create_stat_column(column, "And Another Thing", generate_random_data(1), "+7")

# Fill both columns with different content
fill_column(col1)
fill_column(col2)
import streamlit as st

def format_section(title, name, course, year, value):
    return f"""
    <div class="stat-section">
        <h2><span class='title'>{title}</span><span class='value'> {value}</span></h2>
        <div class="stat-details">
            <span class="name">{name}</span>
            <span class="course">| {course} |</span>
            <span class="year">{year}</span>
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
        line-height: 1.0;
    }
    .stat-details .name {
        font-weight: bold;
    }
    .stat-details .course {
        //font-style: italic;
        //margin-left: 10px;
    }
    .stat-details .year {
        //color: #999;
        //margin-left: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("Page Title")
st.markdown("---")
st.subheader("TEG Records")

# Create columns
col1, col2, col3 = st.columns(3)

# Function to create a stat section within a column
def create_stat_column(column, title, name, course, year, value):
    with column:
        st.markdown(format_section(title, name, course, year, value), unsafe_allow_html=True)

# Fill columns with stat sections
create_stat_column(col1, "Best Score", "Firstname SURNAME", "Course Name", "2018", "25")
create_stat_column(col2, "Best Other Thing", "Firstname SURNAME", "Another Course", "2020", "89")
create_stat_column(col3, "And Another Thing", "Firstname SURNAME", "Third Course", "2022", "+7")
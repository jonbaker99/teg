import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Sample data for bar chart
bar_data = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E'],
    'y': [5, 3, 7, 2, 8]
})

# Generate data for line chart
def generate_cumulative_data(n_points=73, n_lines=5):
    data = []
    for line in range(n_lines):
        cumulative = 0
        for x in range(n_points):
            change = np.random.randint(-1, 4)  # Random int between -1 and 3
            cumulative += change
            data.append({'x': x, 'y': cumulative, 'line': f'Player {line+1}'})
    return pd.DataFrame(data)

line_data = generate_cumulative_data()

# Set up a centralized theme
def setup_altair_theme():
    font = "Arial"
    primary_color = "#3366CC"
    
    return {
        "config": {
            "title": {"font": font, "fontSize": 20},
            "axis": {
                "labelFont": font,
                "titleFont": font,
                "titleFontSize": 14,
                "labelFontSize": 12
            },
            "header": {"labelFont": font, "titleFont": font},
            "mark": {"font": font},
            "legend": {"labelFont": font, "titleFont": font},
            "bar": {"fill": primary_color}
        }
    }

# Apply the theme
alt.themes.register("custom_theme", setup_altair_theme)
alt.themes.enable("custom_theme")

# Create a bar chart
bar_chart = alt.Chart(bar_data).mark_bar().encode(
    x='x',
    y='y'
).properties(
    title='Sample Bar Chart',
    width=400,
    height=300
)

# Define color scheme for lines
color_scheme = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Create a line chart
lines = alt.Chart(line_data).mark_line().encode(
    x=alt.X('x', title='Hole Number'),
    y=alt.Y('y', title='Cumulative Score'),
    color=alt.Color('line:N', scale=alt.Scale(range=color_scheme),
                    legend=alt.Legend(title="Players", orient='right'))
)

# Create labels for the end of each line
labels = alt.Chart(line_data).mark_text(align='left', dx=5).encode(
    x='x:Q',
    y='y:Q',
    text='line:N',
    color=alt.Color('line:N', scale=alt.Scale(range=color_scheme))
).transform_filter(
    alt.datum.x == 72  # Filter to only the last point
)

# Combine the lines and labels
line_chart = (lines + labels).properties(
    title='Cumulative Scores Over 72 Holes',
    width=600,
    height=400
)

# Streamlit app
st.title("Golf Tournament Dashboard")

st.header("Bar Chart Example")
st.altair_chart(bar_chart)

st.header("Line Chart: Cumulative Scores")
st.altair_chart(line_chart)
import streamlit as st
import altair as alt
import pandas as pd

# Sample data
data = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E'],
    'y': [5, 3, 7, 2, 8]
})

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

# Create a chart
chart = alt.Chart(data).mark_bar().encode(
    x='x',
    y='y'
).properties(
    title='Sample Bar Chart',
    width=400,
    height=300
)

# Display the chart in Streamlit
st.altair_chart(chart)
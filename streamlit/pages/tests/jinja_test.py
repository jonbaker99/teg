import streamlit as st
from jinja2 import Template
import pandas as pd

# Sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Score': [95, 82, 88],
})

# Jinja2 template
template_string = """
<style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
</style>
<table>
    <tr>
        {% for col in data.columns %}
        <th>{{ col }}</th>
        {% endfor %}
    </tr>
    {% for _, row in data.iterrows() %}
    <tr>
        {% for col in data.columns %}
        <td>{{ row[col] }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
"""

# Render template
template = Template(template_string)
html_table = template.render(data=df)

# Streamlit app
st.title("Jinja2 Table in Streamlit")
st.components.v1.html(html_table, width=None, height=None, scrolling=False)
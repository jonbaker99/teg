import streamlit as st
import pandas as pd
from utils import aggregate_data, format_vs_par

# Import additional libraries for advanced table displays
# Make sure to install these packages if you haven't already:
# pip install streamlit-aggrid
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# Set the title of the app
st.title("Best Rounds")

# Sidebar for user input
st.sidebar.header("Settings")
n_keep = st.sidebar.number_input("Number of Rows to Keep", min_value=1, max_value=100, value=10, step=1)

@st.cache_data
def load_data():
    # Load the data from the Parquet file & exclude TEG 2 and 50
    data = pd.read_parquet('../data/all-data.parquet')
    data = data[~data['TEG'].isin(['TEG 2', 'TEG 50'])]
    return data

def find_best_rows(data, level_of_aggregation, fields_to_keep, field='GrossVP', top_n=10):
    # Aggregate the data based on the provided level of aggregation
    aggregated_data = aggregate_data(data, level_of_aggregation)
    
    # Define properties for each field
    field_properties = {
        'GrossVP': {'new_name': 'Gross', 'ascending': True, 'formatter': format_vs_par, 'additional_field': 'Sc'},
        'NetVP': {'new_name': 'Net', 'ascending': True, 'formatter': format_vs_par, 'additional_field': None},
        'Sc': {'new_name': 'Gross Score', 'ascending': True, 'formatter': lambda x: int(x), 'additional_field': 'GrossVP'},
        'Stableford': {'new_name': 'Stableford', 'ascending': False, 'formatter': lambda x: int(x), 'additional_field': None},
    }
    
    fields_to_keep = fields_to_keep.copy()

    # Get the properties for the selected field
    properties = field_properties.get(field)
    if not properties:
        raise ValueError(f"Invalid field: {field}")
    
    # Append additional_field to fields_to_keep if it's not None
    additional_field = properties['additional_field']
    fields_to_keep += [additional_field] if additional_field else []

    all_fields = fields_to_keep + [field]

    # Sort the data based on the 'ascending' property
    sorted_data = (aggregated_data[all_fields]
                   .sort_values(by=field, ascending=properties['ascending'])
                   .head(top_n))

    # Add ranking column (ranking order follows the 'ascending' property)
    sorted_data['Rank'] = sorted_data[field].rank(ascending=properties['ascending'], method='min').astype(int).astype(str)
    sorted_data.loc[sorted_data.duplicated('Rank', keep=False), 'Rank'] += '='
    
    # Reorder and rename columns
    sorted_data = sorted_data[['Rank'] + all_fields]
    sorted_data.rename(columns={field: properties['new_name']}, inplace=True)
    
    # Apply formatting to the chosen field
    sorted_data[properties['new_name']] = sorted_data[properties['new_name']].apply(properties['formatter'])
    
    # Apply formatting to all numeric columns
    sorted_data = sorted_data.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)

    return sorted_data

# Load data
all_data = load_data()

rd_fields = ['Player', 'TEG', 'Round']

# Find best rows for each category
lowest_rounds_gross = find_best_rows(all_data, 'Round', rd_fields, 'GrossVP', n_keep)
lowest_rounds_sc = find_best_rows(all_data, 'Round', rd_fields, 'Sc', n_keep)
lowest_rounds_net = find_best_rows(all_data, 'Round', rd_fields, 'NetVP', n_keep)
best_rounds_stableford = find_best_rows(all_data, 'Round', rd_fields, 'Stableford', n_keep)

# Display the results
st.header("Best Gross")
st.dataframe(lowest_rounds_gross, hide_index=True)

# st.header("Best Score")
# st.dataframe(lowest_rounds_sc, hide_index=True)

# st.header("Best Net")
# st.dataframe(lowest_rounds_net, hide_index=True)

# st.header("Best Stableford")
# st.dataframe(best_rounds_stableford, hide_index=True)

# -----------------------------------------------------------
# Additional Examples of Displaying Tables Using `lowest_rounds_gross`
# -----------------------------------------------------------

st.markdown("---")
st.header("Additional Table Display Examples using `lowest_rounds_gross`")

# 1. Using `st.table` (Static Table)
st.subheader("1. `st.table` - Static Table")
st.table(lowest_rounds_gross)

# 2. Using `st.write` (Automatic Rendering)
st.subheader("2. `st.write` - Automatic Rendering")
st.write("Here is the `lowest_rounds_gross` data displayed using `st.write`:")
st.write(lowest_rounds_gross)

# 3. Using `st.aggrid` (Interactive Table with AG Grid)
st.subheader("3. `st_aggrid` - Interactive AG Grid Table")

# Configure Grid Options
gb = GridOptionsBuilder.from_dataframe(lowest_rounds_gross)
gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
gb.configure_side_bar()  # Add a sidebar for additional options
gb.configure_selection(selection_mode="multiple", use_checkbox=True)  # Enable row selection
grid_options = gb.build()

# Display the grid
AgGrid(
    lowest_rounds_gross,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    theme='streamlit',  # Other themes: 'light', 'dark', etc.
    height=400,
    fit_columns_on_grid_load=True
)

# 4. Using `st.experimental_data_editor` (Editable Table)
st.subheader("4. `st.data_editor` - Editable Table")
edited_df = st.data_editor(lowest_rounds_gross, num_rows="dynamic")
st.write("Edited DataFrame:")
st.write(edited_df)

# 5. Using Custom HTML/CSS (Highly Customized Table)
st.subheader("5. Custom HTML/CSS Table")
# Apply custom styling to the DataFrame
def generate_html_table(df):
    return (df.style
              .set_table_styles([
                  {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('font-size', '14px')]},
                  {'selector': 'td', 'props': [('font-size', '12px')]}
              ])
              .to_html(index=False))  # Use to_html() instead of render() and set index=False

html_table = generate_html_table(lowest_rounds_gross)
st.markdown(html_table, unsafe_allow_html=True)

# 6. Using `streamlit-datatable` (Flexible and Interactive Datatable)
# Note: Uncomment the following lines if you have streamlit-datatable installed
# Make sure to install it first using: pip install streamlit-datatable

# from streamlit_datatable import st_datatable

# st.subheader("6. `streamlit-datatable` - Flexible Interactive Table")
# st_datatable(lowest_rounds_gross, hide_index=True)

# 7. Using `st.json` (JSON Representation)
st.subheader("7. `st.json` - JSON Representation")
st.json(lowest_rounds_gross.to_dict(orient='records'))

# 8. Using `st.metric` for Summary Statistics
st.subheader("8. `st.metric` - Summary Statistics")

def parse_gross_score(score):
    # Remove the '+' sign and split the string
    parts = score.replace('+', '').split()
    # Sum up all the numbers
    return sum(int(part) for part in parts)

if not lowest_rounds_gross.empty:
    # Convert 'Gross' column to numeric values
    gross_numeric = lowest_rounds_gross['Gross'].apply(parse_gross_score)
    
    min_gross = gross_numeric.min()
    max_gross = gross_numeric.max()
    avg_gross = gross_numeric.mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Minimum Gross", f"+{min_gross}")
    col2.metric("Average Gross", f"+{avg_gross:.2f}")
    col3.metric("Maximum Gross", f"+{max_gross}")
else:
    st.write("No data available for metrics.")

# 9. Using `st.plotly_chart` to Visualize Data
st.subheader("9. `st.plotly_chart` - Gross Values Bar Chart")
import plotly.express as px

if not lowest_rounds_gross.empty:
    fig = px.bar(lowest_rounds_gross, x='Player', y='Gross', title='Gross Values by Player')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available for plotting.")

# 10. Using `st.pyplot` with Matplotlib
st.subheader("10. `st.pyplot` - Gross Values Line Chart")
import matplotlib.pyplot as plt

if not lowest_rounds_gross.empty:
    fig, ax = plt.subplots()
    ax.plot(lowest_rounds_gross['Player'], lowest_rounds_gross['Gross'], marker='o')
    ax.set_title('Gross Values by Player')
    ax.set_xlabel('Player')
    ax.set_ylabel('Gross')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.write("No data available for plotting.")

# 11. Using `st.altair_chart` with Altair
st.subheader("11. `st.altair_chart` - Gross Values Scatter Plot")
import altair as alt

if not lowest_rounds_gross.empty:
    chart = alt.Chart(lowest_rounds_gross).mark_circle(size=60).encode(
        x='Player',
        y='Gross',
        tooltip=['Player', 'Gross']
    ).interactive().properties(
        title='Gross Values by Player'
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.write("No data available for plotting.")

# 12. Using `st.vega_lite_chart` with Vega-Lite
st.subheader("12. `st.vega_lite_chart` - Gross Values Area Chart")
if not lowest_rounds_gross.empty:
    st.vega_lite_chart(lowest_rounds_gross, {
        'mark': 'area',
        'encoding': {
            'x': {'field': 'Player', 'type': 'ordinal'},
            'y': {'field': 'Gross', 'type': 'quantitative'},
            'color': {'field': 'Player', 'type': 'nominal'}
        }
    }, use_container_width=True)
else:
    st.write("No data available for plotting.")

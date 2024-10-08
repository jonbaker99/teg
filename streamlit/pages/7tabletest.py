import streamlit as st
import pandas as pd
from utils import aggregate_data, format_vs_par

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
# st.dataframe(lowest_rounds_sc)

st.header("Best Stableford")
st.dataframe(best_rounds_stableford, hide_index=True)

st.header("Best Net")
st.dataframe(lowest_rounds_net, hide_index=True)
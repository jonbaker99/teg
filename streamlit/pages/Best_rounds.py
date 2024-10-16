# Standard Library Imports
import pandas as pd

# Third-Party Imports
import streamlit as st

# Local Imports
from utils import aggregate_data, format_vs_par, load_all_data

# Constants
DEFAULT_TOP_N = 3
RD_FIELDS = ['Player', 'TEG', 'Round', 'Course']
FIELD_PROPERTIES = {
    'GrossVP': {
        'new_name': 'Gross',
        'ascending': True,
        'formatter': format_vs_par,
        'additional_field': 'Sc'
    },
    'NetVP': {
        'new_name': 'Net',
        'ascending': True,
        'formatter': format_vs_par,
        'additional_field': None
    },
    'Sc': {
        'new_name': 'Gross Score',
        'ascending': True,
        'formatter': lambda x: int(x),
        'additional_field': 'GrossVP'
    },
    'Stableford': {
        'new_name': 'Stableford',
        'ascending': False,
        'formatter': lambda x: int(x),
        'additional_field': None
    },
}

# Set the title of the app
st.title("Best rounds")

# Sidebar for user input
#st.sidebar.header("Settings")
n_keep = st.number_input(
    "Number of rounds to show",
    min_value=1,
    max_value=100,
    value=DEFAULT_TOP_N,
    step=1
)

@st.cache_data(show_spinner=False, ttl=3600)
def load_data(exclude_teg_50=True):
    """
    Load all data with optional exclusions.

    Parameters:
        exclude_teg_50 (bool): Whether to exclude TEG 50 data.

    Returns:
        pd.DataFrame: The loaded data.
    """
    return load_all_data(exclude_teg_50=exclude_teg_50)

def find_best_rows(data, level_of_aggregation, fields_to_keep, field, top_n):
    """
    Aggregates data and finds the top N rows based on the specified field.

    Parameters:
        data (pd.DataFrame): The input data.
        level_of_aggregation (str): The level at which to aggregate data.
        fields_to_keep (list): List of fields to retain.
        field (str): The field to sort and rank by.
        top_n (int): Number of top rows to retrieve.

    Returns:
        pd.DataFrame: The top N rows with rankings.
    """
    # Aggregate the data
    aggregated_data = aggregate_data(data, level_of_aggregation)

    # Get properties for the specified field
    properties = FIELD_PROPERTIES.get(field)
    if not properties:
        st.error(f"The field '{field}' is invalid. Please select a valid field.")
        return pd.DataFrame()

    # Append additional_field to fields_to_keep if it's not None and not already present
    additional_field = properties['additional_field']
    if additional_field and additional_field not in fields_to_keep:
        fields_to_keep.append(additional_field)

    all_fields = fields_to_keep + [field]

    # Sort the data based on the 'ascending' property
    sorted_data = aggregated_data.sort_values(by=field, ascending=properties['ascending'])

    # Determine the nth value for filtering
    nth_index = min(top_n - 1, len(sorted_data) - 1)
    nth_value = sorted_data.iloc[nth_index][field]

    # Filter the data to include all rows that are at least as good as the nth value
    if properties['ascending']:
        result_data = sorted_data[sorted_data[field] <= nth_value]
    else:
        result_data = sorted_data[sorted_data[field] >= nth_value]

    # Add ranking column
    result_data = result_data.copy()
    result_data['Rank'] = result_data[field].rank(
        ascending=properties['ascending'],
        method='min'
    ).astype(int).astype(str)
    duplicated_ranks = result_data.duplicated('Rank', keep=False)
    result_data.loc[duplicated_ranks, 'Rank'] += '='

    # Reorder and rename columns
    result_data = result_data[['Rank'] + all_fields]
    result_data.rename(columns={field: properties['new_name']}, inplace=True)

    # Apply formatting to the chosen field
    result_data[properties['new_name']] = result_data[properties['new_name']].apply(properties['formatter'])

    # Apply formatting to all numeric columns
    numeric_cols = result_data.select_dtypes(include=['float', 'int']).columns
    result_data[numeric_cols] = result_data[numeric_cols].astype(int)

    return result_data

def combine_teg_and_round(df):
    """
    Combine 'TEG' and 'Round' columns into a single 'Round' column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The modified DataFrame with combined 'Round' column.
    """
    df = df.copy()
    df['Round'] = df['TEG'] + ' Round ' + df['Round'].astype(str)
    df.drop(columns=['TEG'], inplace=True)
    return df

def custom_align_data(df):
    """
    Apply custom HTML alignment to DataFrame columns.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with HTML-aligned columns.
    """
    aligned_df = df.copy()
    for col in aligned_df.columns:
        if col in ['Player', 'Round', 'Course']:
            # Left align Player and Round columns
            aligned_df[col] = aligned_df[col].apply(lambda x: f"<div style='text-align: left;'>{x}</div>")
        else:
            # Center align other columns
            aligned_df[col] = aligned_df[col].apply(lambda x: f"<div style='text-align: center;'>{x}</div>")
    return aligned_df

def display_custom_aligned_df(df, title):
    """
    Display DataFrame as an HTML table with custom alignment.

    Parameters:
        df (pd.DataFrame): The DataFrame to display.
        title (str): The title for the DataFrame section.
    """
    #st.subheader(title)
    aligned_df = custom_align_data(df)
    st.write(aligned_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Load data with a loading spinner
with st.spinner('Loading data...'):
    all_data = load_all_data(exclude_teg_50=True)

rd_fields = ['Player', 'TEG', 'Round', 'Course']

# Define metrics to display
fields_metrics = {
    "Best Gross": "GrossVP",
    "Best SC": "Sc",
    "Best Net": "NetVP",
    "Best Stableford": "Stableford"
}

# Find best rows for each category
results = {}
for title, field in fields_metrics.items():
    best_rows = find_best_rows(all_data, 'Round', rd_fields.copy(), field, n_keep)
    if not best_rows.empty:
        combined_df = combine_teg_and_round(best_rows)
        results[title] = combined_df

# Define Tabs
tab_labels = ["Gross vs Par", "Stableford", "Gross Score", "Net vs Par"]
tabs = st.tabs(tab_labels)

# Mapping between tab names and their corresponding titles in results
tab_to_title = {
    "Gross vs Par": "Best Gross",
    "Stableford": "Best Stableford",
    "Gross Score": "Best SC",
    "Net vs Par": "Best Net"
}

# Iterate through tabs and display content
for tab_label, tab in zip(tab_labels, tabs):
    with tab:

        st.markdown(f"### Best rounds: {tab_label}")
        #st.markdown("---")  # Separator


        # Display TEG Record Placeholder
        #st.markdown("**BEST TEGS**")
        #st.write("TEG Record - Coming Soon")
        
        # st.markdown("---")  # Separator
        
        # Display Round Record
        round_title = tab_to_title.get(tab_label)
        if round_title and round_title in results:
            #st.markdown("**BEST ROUNDS**")
            display_custom_aligned_df(results[round_title], round_title)
        else:
            st.write("No data available for this section.")
        
        st.markdown("---")  # Separator between sections if needed

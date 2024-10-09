import streamlit as st
import pandas as pd
from utils import aggregate_data, format_vs_par
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# Set the title of the app
st.title("Using streamlit table instead of html or dataframe")

n = 3

# Sidebar for user input
st.sidebar.header("Settings")
n_keep = st.sidebar.number_input("Number of Rows to Keep", min_value=1, max_value=100, value=n, step=1)

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
    sorted_data = aggregated_data[all_fields].sort_values(by=field, ascending=properties['ascending'])

    # Find the value at the nth position
    if len(sorted_data) >= top_n:
        nth_value = sorted_data.iloc[top_n - 1][field]
    else:
        nth_value = sorted_data.iloc[-1][field]

    # Filter the data to include all rows that are at least as good as the nth value
    if properties['ascending']:
        result_data = sorted_data[sorted_data[field] <= nth_value]
    else:
        result_data = sorted_data[sorted_data[field] >= nth_value]

    # Add ranking column
    result_data['Rank'] = result_data[field].rank(ascending=properties['ascending'], method='min').astype(int).astype(str)
    result_data.loc[result_data.duplicated('Rank', keep=False), 'Rank'] += '='
    
    # Reorder and rename columns
    result_data = result_data[['Rank'] + all_fields]
    result_data.rename(columns={field: properties['new_name']}, inplace=True)
    
    # Apply formatting to the chosen field
    result_data[properties['new_name']] = result_data[properties['new_name']].apply(properties['formatter'])
    
    # Apply formatting to all numeric columns
    result_data = result_data.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)

    return result_data

# Load data
all_data = load_data()

rd_fields = ['Player', 'TEG', 'Round']

# Find best rows for each category
lowest_rounds_gross = find_best_rows(all_data, 'Round', rd_fields, 'GrossVP', n_keep)
lowest_rounds_sc = find_best_rows(all_data, 'Round', rd_fields, 'Sc', n_keep)
lowest_rounds_net = find_best_rows(all_data, 'Round', rd_fields, 'NetVP', n_keep)
best_rounds_stableford = find_best_rows(all_data, 'Round', rd_fields, 'Stableford', n_keep)

def combine_teg_and_round(df):
    # Create a new 'Round' column by combining 'TEG' and 'Round'
    df['Round'] = df['TEG'] + ' | round ' + df['Round'].astype(str)
    
    # Remove the 'TEG' column
    df = df.drop(columns=['TEG'])
    
    return df

lowest_rounds_gross = combine_teg_and_round(lowest_rounds_gross)
lowest_rounds_sc = combine_teg_and_round(lowest_rounds_sc)
lowest_rounds_net = combine_teg_and_round(lowest_rounds_net)
best_rounds_stableford = combine_teg_and_round(best_rounds_stableford)

def display_streamlit_table(df, title):
    st.subheader(title)
    st.table(df)

# Display DataFrames
display_streamlit_table(lowest_rounds_gross, "Best Gross - streamlit table")
st.markdown("---")
display_streamlit_table(best_rounds_stableford, "Best Stableford - streamlit table")
st.markdown("---")
display_streamlit_table(lowest_rounds_net, "Best Net - streamlit table")




def display_aggrid_table(df, title):
    st.subheader(title)
    
    # Configure grid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        maxWidth = 100,
        cellStyle={'text-align': 'center'},  # Center align all columns by default
        #headerClass='center-aligned-header',  # Custom class for header alignment
        filterable = False,
        sortable = False
    )
    # gb.configure_default_column(filterable = False, sorteable = False, maxWidth = 100)
    gb.configure_column("Player", minWidth=130, maxWidth=150,  cellStyle={'text-align': 'left'})
    gb.configure_column("Round", minWidth=130,maxWidth=150, cellStyle={'text-align': 'left'})
    gb.configure_column("Rank", maxWidth=50, type=["numericColumn", "customNumericFormat"], precision=0)
    gb.configure_selection('disabled')  # Enable row selection
    gb.configure_grid_options(domLayout='normal')  # Ensures the grid size adapts to its container
    
    gridOptions = gb.build()
    
    # Display the grid
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        #height=300,  # Set a fixed height. Adjust as needed.
        data_return_mode='AS_INPUT', 
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True  # Set to True to allow jsfunction to be injected
    )
    
    # You can handle selection here if needed
    selected = grid_response['selected_rows']
    if selected:
        st.write("Selected row:", selected[0])

# ... (keep the existing data loading and processing code)

# Display DataFrames using ag-Grid
display_aggrid_table(lowest_rounds_gross, "Best Gross - aggrid_table")
st.markdown("---")
display_aggrid_table(best_rounds_stableford, "Best Stableford - aggrid_table")
st.markdown("---")
display_aggrid_table(lowest_rounds_net, "Best Net - aggrid_table")
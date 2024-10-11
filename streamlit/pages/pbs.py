import streamlit as st
import pandas as pd
import altair as alt
from utils import load_all_data, aggregate_data, get_teg_rounds

# Streamlit page configuration
st.set_page_config(page_title="Player Metrics Overview")

all_data = load_all_data(exclude_teg_50=True, exclude_incomplete_tegs=True)
teg_data = aggregate_data(data=all_data, aggregation_level='TEG')

# Find unique combinations of TEG and Year
unique_teg_year = all_data[['TEG', 'Year']].drop_duplicates()

# Merge teg_data with the unique TEG-Year combinations to add the Year column
df_merged = pd.merge(teg_data, unique_teg_year, on='TEG', how='left')

# Define metrics and aggregation functions (excluding Sc for TEG)
metrics = {
    'Gross': 'GrossVP',
    'Net': 'NetVP',
    'Stableford': 'Stableford'
}

# Streamlit App Layout
st.title("Player Metrics Overview")

# Loop over each metric and create the desired DataFrame (original min/max logic)
for metric_name, column in metrics.items():
    # Set up whether to find max or min for each metric
    if column == 'Stableford':
        best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
        sort_ascending = False
    else:
        best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
        sort_ascending = True

    # Select relevant columns and rename them
    output = best_values[['Player', column, 'TEG', 'Year']].rename(columns={column: metric_name})

    # Format the numerical columns to 0 decimal places
    if column in ['GrossVP', 'NetVP']:
        output[metric_name] = output[metric_name].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
    else:
        output[metric_name] = output[metric_name].apply(lambda x: f"{int(x):.0f}")

    # Shorten the column names to make tables narrower
    output.columns = ['Player', 'Value', 'TEG', 'Year']

    # Reset index to remove indices from display
    output = output.reset_index(drop=True)

    # Sort the DataFrame based on 'Value' column
    output = output.sort_values(by='Value', ascending=sort_ascending)

    # Display the output using Streamlit write with HTML rendering
    st.subheader(f"Best {metric_name.title()} by TEG")
    st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

# Loop over each metric and create the desired DataFrame (opposite min/max logic)
for metric_name, column in metrics.items():
    # Set up whether to find max or min for each metric (opposite logic)
    if column == 'Stableford':
        worst_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
        sort_ascending = True
    else:
        worst_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
        sort_ascending = False

    # Dynamically replace 'Best' with 'Worst' in the metric name
    worst_metric_name = metric_name.replace('Best', 'Worst')

    # Select relevant columns and rename them
    output = worst_values[['Player', column, 'TEG', 'Year']].rename(columns={column: worst_metric_name})

    # Format the numerical columns to 0 decimal places
    if column in ['GrossVP', 'NetVP']:
        output[worst_metric_name] = output[worst_metric_name].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
    else:
        output[worst_metric_name] = output[worst_metric_name].apply(lambda x: f"{int(x):.0f}")

    # Shorten the column names to make tables narrower
    output.columns = ['Player', 'Value', 'TEG', 'Year']

    # Reset index to remove indices from display
    output = output.reset_index(drop=True)

    # Sort the DataFrame based on 'Value' column (opposite sorting order)
    output = output.sort_values(by='Value', ascending=sort_ascending)

    # Display the output using Streamlit write with HTML rendering
    st.subheader(f"Worst {metric_name.title()} by TEG")
    st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

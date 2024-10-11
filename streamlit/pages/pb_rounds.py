import streamlit as st
import pandas as pd
import altair as alt
from utils import load_all_data, aggregate_data, get_teg_rounds

# Streamlit page configuration
st.set_page_config(page_title="Player Metrics Overview")

# Load the dataset and aggregate data at the 'Round' level
all_data = load_all_data(exclude_teg_50=True, exclude_incomplete_tegs=True)
round_data = aggregate_data(data=all_data, aggregation_level='Round')

# Load additional round information (Course and Date)
round_info = pd.read_csv('../data/round_info.csv')

# Drop 'Course' and 'Date' from round_data to avoid column conflicts during merge
if 'Course' in round_data.columns:
    round_data = round_data.drop(columns=['Course'])
if 'Date' in round_data.columns:
    round_data = round_data.drop(columns=['Date'])

# Merge round_data with round_info to add 'Course' and 'Date' columns based on 'TEG' and 'Round'
df_merged = pd.merge(round_data, round_info[['TEG', 'Round', 'Course', 'Date']], on=['TEG', 'Round'], how='left')

# Define metrics and aggregation functions (excluding Sc for Round)
metrics = {
    'Gross': 'GrossVP',
    'Net': 'NetVP',
    'Stableford': 'Stableford'
}

# Streamlit App Layout
st.title("Player Metrics Overview - Round Level")

# Loop over each metric and create the desired DataFrame (original min/max logic)
for metric_name, column in metrics.items():
    # Set up whether to find max or min for each metric
    if column == 'Stableford':
        best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
        sort_ascending = False
    else:
        best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
        sort_ascending = True

    # Create a new 'Round' column combining 'TEG' and 'Round'
    best_values['Round'] = best_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)

    # Select relevant columns and rename them
    output = best_values[['Player', column, 'Round', 'Course', 'Date']].rename(columns={column: metric_name})

    # Sort the DataFrame based on the 'PB' column before formatting
    output = output.sort_values(by=metric_name, ascending=sort_ascending)

    # Format the numerical columns to 0 decimal places
    if column in ['GrossVP', 'NetVP']:
        output[metric_name] = output[metric_name].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
    else:
        output[metric_name] = output[metric_name].apply(lambda x: f"{int(x):.0f}")

    # Shorten the column names to make tables narrower
    output.columns = ['Player', 'PB', 'Round', 'Course', 'Date']

    # Reset index to remove indices from display
    output = output.reset_index(drop=True)

    # Display the output using Streamlit write with HTML rendering
    st.subheader(f"Best {metric_name.title()} by Round")
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

    # Create a new 'Round' column combining 'TEG' and 'Round'
    worst_values['Round'] = worst_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)

    # Dynamically replace 'Best' with 'Worst' in the metric name
    worst_metric_name = metric_name.replace('Best', 'Worst')

    # Select relevant columns and rename them
    output = worst_values[['Player', column, 'Round', 'Course', 'Date']].rename(columns={column: worst_metric_name})

    # Sort the DataFrame based on the 'PB' column before formatting
    output = output.sort_values(by=worst_metric_name, ascending=sort_ascending)

    # Format the numerical columns to 0 decimal places
    if column in ['GrossVP', 'NetVP']:
        output[worst_metric_name] = output[worst_metric_name].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
    else:
        output[worst_metric_name] = output[worst_metric_name].apply(lambda x: f"{int(x):.0f}")

    # Shorten the column names to make tables narrower
    output.columns = ['Player', 'PB', 'Round', 'Course', 'Date']

    # Reset index to remove indices from display
    output = output.reset_index(drop=True)

    # Display the output using Streamlit write with HTML rendering
    st.subheader(f"Worst {metric_name.title()} by Round")
    st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

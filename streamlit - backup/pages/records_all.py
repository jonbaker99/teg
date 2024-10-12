import os
import pandas as pd
import streamlit as st
from utils import load_all_data, aggregate_data

def display_metric_overall(df, metric_name, column, aggregation='best'):
    """
    Returns the best or worst metric across all players for a specific score type.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing aggregated data.
    - metric_name (str): The name of the metric (e.g., 'Gross').
    - column (str): The column name corresponding to the metric in the DataFrame.
    - aggregation (str): 'best' to display best metrics, 'worst' for worst metrics.

    Returns:
    - pd.DataFrame: Aggregated DataFrame with added 'Measure' field.
    """
    if aggregation not in ['best', 'worst']:
        st.error("Invalid aggregation type. Choose 'best' or 'worst'.")
        return

    try:
        if column == 'Stableford':
            if aggregation == 'best':
                idx = df[column].idxmax()
                sort_ascending = False
            else:
                idx = df[column].idxmin()
                sort_ascending = True
        else:
            if aggregation == 'best':
                idx = df[column].idxmin()
                sort_ascending = True
            else:
                idx = df[column].idxmax()
                sort_ascending = False

        # Extract the best/worst metrics
        metric_values = df[df[column] == df.loc[idx, column]]

        # Include the 'Player' column
        if 'Round' in df.columns:
            metric_values['Round_Display'] = metric_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)
            selected_columns = ['Player', column, 'Round_Display']
            rename_dict = {
                column: 'Score',
                'Round_Display': 'Round'
            }
            if 'Course' in df.columns:
                selected_columns.append('Course')
            if 'Date' in df.columns:
                selected_columns.append('Date')
        else:
            selected_columns = ['Player', column, 'TEG']
            rename_dict = {
                column: 'Score'
            }
            if 'Year' in df.columns:
                selected_columns.append('Year')

        # Rename and select relevant columns
        output = metric_values[selected_columns].rename(columns=rename_dict)

        # Add a 'Measure' field to indicate the score type (e.g., Gross, Net, etc.)
        output['Measure'] = metric_name

        # Move the 'Measure' column to be the first column
        measure_col = output.pop('Measure')
        output.insert(0, 'Measure', measure_col)

        # Format numerical columns
        if column in ['GrossVP', 'NetVP']:
            output['Score'] = output['Score'].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
        else:
            output['Score'] = output['Score'].apply(lambda x: f"{int(x):.0f}")

        # Sort the DataFrame and reset index
        output = output.sort_values(by='Score', ascending=sort_ascending).reset_index(drop=True)

        # Return the DataFrame with 'Measure' added
        return output

    except KeyError as e:
        st.error(f"KeyError encountered while processing {metric_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    except Exception as e:
        st.error(f"An unexpected error occurred while processing {metric_name}: {e}")
        return pd.DataFrame()

def combine_metrics(data, aggregation_level, aggregation_type):
    """
    Combines the best or worst metrics across multiple score types into a single DataFrame.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing aggregated data.
    - aggregation_level (str): The level of aggregation ('TEG' or 'Round').
    - aggregation_type (str): 'best' for best metrics, 'worst' for worst metrics.

    Returns:
    - pd.DataFrame: Combined DataFrame with all measures, excluding 'Score'.
    """
    metrics = {
        'Gross': 'GrossVP',
        'Net': 'NetVP',
        'Stableford': 'Stableford'
        # 'Score': 'Sc' -> Excluding 'Score' from the final tables
    }
    
    combined_df = pd.DataFrame()
    
    for metric_name, column in metrics.items():
        metric_df = display_metric_overall(data, metric_name, column, aggregation=aggregation_type)
        combined_df = pd.concat([combined_df, metric_df], ignore_index=True)
    
    return combined_df

def show_combined_metrics(all_data):
    """
    Displays the combined best and worst TEGs and Rounds tables.
    """
    try:
        # Aggregate data for TEGs and Rounds
        teg_data = aggregate_data(data=all_data, aggregation_level='TEG')
        round_data = aggregate_data(data=all_data, aggregation_level='Round')

        # Combine best and worst TEGs
        best_tegs = combine_metrics(teg_data, aggregation_level='TEG', aggregation_type='best')
        worst_tegs = combine_metrics(teg_data, aggregation_level='TEG', aggregation_type='worst')

        # Combine best and worst Rounds
        best_rounds = combine_metrics(round_data, aggregation_level='Round', aggregation_type='best')
        worst_rounds = combine_metrics(round_data, aggregation_level='Round', aggregation_type='worst')

        # Display combined tables in Streamlit
        st.subheader("Best TEGs")
        st.write(best_tegs.to_html(index=False), unsafe_allow_html=True)

        st.subheader("Best Rounds")
        st.write(best_rounds.to_html(index=False), unsafe_allow_html=True)

        st.subheader("Worst TEGs")
        st.write(worst_tegs.to_html(index=False), unsafe_allow_html=True)

        st.subheader("Worst Rounds")
        st.write(worst_rounds.to_html(index=False), unsafe_allow_html=True)

    except KeyError as e:
        st.error(f"KeyError encountered in combined metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in combined metrics: {e}")



all_data = load_all_data(exclude_teg_50=True)
show_combined_metrics(all_data)


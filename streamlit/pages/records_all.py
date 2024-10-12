import os
import pandas as pd
import streamlit as st
from utils import load_all_data, aggregate_data

def display_metric_overall(df, metric_name, column, aggregation='best'):
    """
    Displays the best or worst metric across all players for a specific score type.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing aggregated data.
    - metric_name (str): The name of the metric (e.g., 'Gross').
    - column (str): The column name corresponding to the metric in the DataFrame.
    - aggregation (str): 'best' to display best metrics, 'worst' for worst metrics.
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

        # Format numerical columns
        if column in ['GrossVP', 'NetVP']:
            output['Score'] = output['Score'].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
        else:
            output['Score'] = output['Score'].apply(lambda x: f"{int(x):.0f}")

        # Sort the DataFrame and reset index
        output = output.sort_values(by='Score', ascending=sort_ascending).reset_index(drop=True)

        # Display the DataFrame
        display_title = f"Overall {aggregation.capitalize()} " + ("Round" if 'Round' in df.columns else "TEG") + f": {metric_name}"
        st.subheader(display_title)
        st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

    except KeyError as e:
        st.error(f"KeyError encountered while processing {metric_name}: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while processing {metric_name}: {e}")

def show_overall_teg_metrics(all_data):
    """
    Displays the overall best and worst TEG metrics across all players.
    """
    try:
        # Aggregate data at TEG level
        teg_data = aggregate_data(data=all_data, aggregation_level='TEG')

        # Define metrics and their corresponding columns
        metrics = {
            'Gross': 'GrossVP',
            'Net': 'NetVP',
            'Stableford': 'Stableford',
            'Score': 'Sc'
        }

        # Display best metrics across all players
        for metric_name, column in metrics.items():
            display_metric_overall(df=teg_data, metric_name=metric_name, column=column, aggregation='best')

        # Display worst metrics across all players
        for metric_name, column in metrics.items():
            display_metric_overall(df=teg_data, metric_name=metric_name, column=column, aggregation='worst')

    except KeyError as e:
        st.error(f"KeyError encountered in Overall TEG Metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in Overall TEG Metrics: {e}")

def show_overall_round_metrics(all_data):
    """
    Displays the overall best and worst round metrics across all players.
    """
    try:
        # Aggregate data at Round level
        #add_fld = ['Year']
        round_data = aggregate_data(data=all_data, aggregation_level='Round')

        # Load additional round information
        round_info_path = '../data/round_info.csv'
        if not os.path.exists(round_info_path):
            st.error(f"round_info.csv not found at path: {round_info_path}")
            return

        round_info = pd.read_csv(round_info_path)

        # Merge round_data with round_info to add 'Course' and 'Date'
        #df_merged = pd.merge(round_data, round_info[['TEG', 'Round', 'Course', 'Date']], on=['TEG', 'Round'], how='left')
        df_merged = round_data.copy()
        # Define metrics and their corresponding columns
        metrics = {
            'Gross': 'GrossVP',
            'Net': 'NetVP',
            'Stableford': 'Stableford',
            'Score': 'Sc'
        }

        # Display best metrics across all players
        for metric_name, column in metrics.items():
            display_metric_overall(df=df_merged, metric_name=metric_name, column=column, aggregation='best')

        # Display worst metrics across all players
        for metric_name, column in metrics.items():
            display_metric_overall(df=df_merged, metric_name=metric_name, column=column, aggregation='worst')

    except KeyError as e:
        st.error(f"KeyError encountered in Overall Round Metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in Overall Round Metrics: {e}")

all_data = load_all_data(exclude_teg_50=True)
show_overall_round_metrics(all_data)
show_overall_teg_metrics(all_data)
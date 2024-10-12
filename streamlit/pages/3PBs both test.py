# player_metrics_overview.py

import streamlit as st
import pandas as pd
import os

from utils import load_all_data, aggregate_data

# ---------------------------#
#       Helper Functions     #
# ---------------------------#

def display_metric(df, metric_name, column, group_by=['Player'], aggregation='best'):
    """
    Displays the best or worst metric for each player.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing aggregated data.
    - metric_name (str): The name of the metric (e.g., 'Gross').
    - column (str): The column name corresponding to the metric in the DataFrame.
    - group_by (list): Columns to group by.
    - aggregation (str): 'best' to display best metrics, 'worst' for worst metrics.
    """
    if aggregation not in ['best', 'worst']:
        st.error("Invalid aggregation type. Choose 'best' or 'worst'.")
        return

    try:
        if column == 'Stableford':
            if aggregation == 'best':
                idx = df.groupby(group_by)[column].idxmax()
                sort_ascending = False
            else:
                idx = df.groupby(group_by)[column].idxmin()
                sort_ascending = True
        else:
            if aggregation == 'best':
                idx = df.groupby(group_by)[column].idxmin()
                sort_ascending = True
            else:
                idx = df.groupby(group_by)[column].idxmax()
                sort_ascending = False

        metric_values = df.loc[idx]
        
        
        #st.write(group_by)
        # Create display names based on aggregation
        display_title = f"Personal {aggregation.capitalize()} " + ("Round" if 'Round' in df.columns else "TEG") + f": {metric_name}"

        # Select and rename relevant columns
        if 'Round' in df.columns:
            metric_values['Round_Display'] = metric_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)
            selected_columns = ['Player', column, 'Round_Display', 'Course', 'Date']
            rename_dict = {
                column: 'Score',
                'Round_Display': 'Round'
            }
        else:
            selected_columns = ['Player', column, 'TEG', 'Year']
            rename_dict = {
                column: 'Score'
            }

        output = metric_values[selected_columns].rename(columns=rename_dict)

        # Format numerical columns
        if column in ['GrossVP', 'NetVP']:
            output['Score'] = output['Score'].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
        else:
            output['Score'] = output['Score'].apply(lambda x: f"{int(x):.0f}")

        # Ensure 'Year' remains integer without formatting
        if 'Year' in output.columns:
            output['Year'] = output['Year'].astype(int)

        # Sort the DataFrame
        output = output.sort_values(by='Score', ascending=sort_ascending).reset_index(drop=True)

        # Display the DataFrame using Streamlit's native component without index
        st.subheader(display_title)
        st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

    except KeyError as e:
        st.error(f"KeyError encountered while processing {metric_name}: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while processing {metric_name}: {e}")

def show_teg_metrics(all_data):
    """
    Displays the TEG-level best and worst metrics.

    Parameters:
    - all_data (pd.DataFrame): The loaded and cleaned data.
    """
    #st.header("Best & Worst TEGs")

    try:
        # Aggregate data at TEG level
        teg_data = aggregate_data(data=all_data, aggregation_level='TEG')

        # Find unique combinations of TEG and Year
        if 'Year' in all_data.columns:
            unique_teg_year = all_data[['TEG', 'Year']].drop_duplicates()
        else:
            st.warning("'Year' column not found in data.")
            unique_teg_year = pd.DataFrame({'TEG': teg_data['TEG'].unique()})

        # Merge teg_data with unique_teg_year to add Year column
        df_merged = pd.merge(teg_data, unique_teg_year, on='TEG', how='left')

        # Define metrics and their corresponding columns
        metrics = {
            'Gross': 'GrossVP',
            'Net': 'NetVP',
            'Stableford': 'Stableford'
        }

        # Verify necessary columns
        required_columns = ['Player', 'Sc', 'GrossVP', 'NetVP', 'Stableford', 'TEG', 'Year']
        missing_columns = [col for col in required_columns if col not in df_merged.columns]
        if missing_columns:
            st.error(f"Missing columns in TEG data: {missing_columns}")
            return

        # Display best metrics
        for metric_name, column in metrics.items():
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='best')

        # Display worst metrics
        for metric_name, column in metrics.items():
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='worst')

    except KeyError as e:
        st.error(f"KeyError encountered in TEG Metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in TEG Metrics: {e}")

def show_round_metrics(all_data):
    """
    Displays the Round-level best and worst metrics.

    Parameters:
    - all_data (pd.DataFrame): The loaded and cleaned data.
    """
    #st.header("Best & Worst Rounds")

    try:
        # Aggregate data at Round level
        round_data = aggregate_data(data=all_data, aggregation_level='Round')

        # Load additional round information
        # Reverting the path to '../data/round_info.csv' as per user request
        #current_dir = os.path.dirname(os.path.abspath(__file__))
        round_info_path = '../data/round_info.csv'
        if not os.path.exists(round_info_path):
            st.error(f"round_info.csv not found at path: {round_info_path}")
            return

        round_info = pd.read_csv(round_info_path)

        # Drop 'Course' and 'Date' from round_data if they exist to avoid conflicts
        for col in ['Course', 'Date']:
            if col in round_data.columns:
                round_data = round_data.drop(columns=[col])

        # Merge round_data with round_info to add 'Course' and 'Date'
        df_merged = pd.merge(round_data, round_info[['TEG', 'Round', 'Course', 'Date']], on=['TEG', 'Round'], how='left')

        # Define metrics and their corresponding columns
        metrics = {
            'Gross': 'GrossVP',
            'Net': 'NetVP',
            'Stableford': 'Stableford'
        }

        # Verify necessary columns
        required_columns = ['Player', 'Sc', 'GrossVP', 'NetVP', 'Stableford', 'TEG', 'Round', 'Course', 'Date']
        missing_columns = [col for col in required_columns if col not in df_merged.columns]
        if missing_columns:
            st.error(f"Missing columns in Round data: {missing_columns}")
            return

        # Display best metrics
        for metric_name, column in metrics.items():
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='best')

        # Display worst metrics
        for metric_name, column in metrics.items():
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='worst')

    except KeyError as e:
        st.error(f"KeyError encountered in Round Metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in Round Metrics: {e}")

def show_about():
    """
    Displays information about the application.
    """
    st.header("About This Application")
    st.write("""
    ### Player Metrics Overview

    This application provides an overview of player metrics at both the TEG and Round levels. Navigate through the tabs to explore detailed statistics and performance indicators.

    **Tabs:**
    - **By TEG:** Displays the best and worst metrics for players aggregated at the TEG level.
    - **By Round:** Shows the best and worst metrics for players aggregated at the Round level.
    - **About:** Information about the application and its purpose.
    """)

    st.markdown("---")
    st.markdown("© 2024 Your Company Name. All rights reserved.")

# ---------------------------#
#        Caching Data        #
# ---------------------------#

@st.cache_data
def load_and_prepare_data(exclude_incomplete_tegs=True):
    """
    Loads and prepares the data for analysis.

    Parameters:
    - exclude_incomplete_tegs (bool): Whether to exclude incomplete TEGs.

    Returns:
    - pd.DataFrame: The loaded and cleaned data.
    """
    all_data = load_all_data(exclude_incomplete_tegs=exclude_incomplete_tegs)
    return all_data

# ---------------------------#
#            Main            #
# ---------------------------#

def main():
    st.title("Personal Bests (& Worsts)")

    # Create tabs for the interface
    tab1, tab2, tab3 = st.tabs(["By TEG", "By Round", "About"])

    # Load all data once to avoid redundancy with caching
    with st.spinner("Loading data..."):
        all_data = load_and_prepare_data()

    if all_data.empty:
        st.error("No data available to display. Please check your data sources.")
        return

    with tab1:
        show_teg_metrics(all_data)

    with tab2:
        show_round_metrics(all_data)

    with tab3:
        show_about()

    # Add a footer or additional information
    st.markdown("---")
    st.markdown("© 2024 Your Company Name. All rights reserved.")

if __name__ == "__main__":
    main()

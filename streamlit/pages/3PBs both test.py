# player_metrics_overview.py

import streamlit as st
import pandas as pd
import os

from utils import load_all_data, aggregate_data

# Set the page configuration once
st.set_page_config(
    page_title="Personal Bests (& Worsts)",
    #layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("Personal Bests (& Worsts)")

    # Create tabs for the interface
    tab1, tab2, tab3 = st.tabs(["By TEG", "By Round", "About"])

    # Load all data once to avoid redundancy
    all_data = load_all_data(exclude_incomplete_tegs=True)
    if all_data.empty:
        st.error("No data available to display. Please check your data sources.")
        return

    with tab1:
        show_teg_metrics(all_data)

    with tab2:
        show_round_metrics(all_data)

    with tab3:
        show_about()

    # Optional: Add a footer or additional information
    st.markdown("---")
    st.markdown("© 2024 Your Company Name. All rights reserved.")

def show_teg_metrics(all_data):
    st.header("Player Metrics Overview - TEG Level")
    
    try:
        # Aggregate data at TEG level
        teg_data = aggregate_data(data=all_data, aggregation_level='TEG')
        # st.write("**Aggregated TEG Data:**", teg_data.head())

        # Find unique combinations of TEG and Year
        if 'Year' in all_data.columns:
            unique_teg_year = all_data[['TEG', 'Year']].drop_duplicates()
            # st.write("**Unique TEG-Year Combinations:**", unique_teg_year.head())
        else:
            st.warning("'Year' column not found in data.")
            unique_teg_year = pd.DataFrame({'TEG': teg_data['TEG'].unique()})

        # Merge teg_data with unique_teg_year to add Year column
        df_merged = pd.merge(teg_data, unique_teg_year, on='TEG', how='left')
        # st.write("**Merged TEG Data:**", df_merged.head())

        # Define metrics and aggregation functions (excluding Sc for TEG)
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

        # Loop over each metric and display best values
        for metric_name, column in metrics.items():
            if column == 'Stableford':
                best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
                sort_ascending = False
            else:
                best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
                sort_ascending = True

            output = best_values[['Player', column, 'TEG', 'Year']].rename(columns={column: metric_name})

            # Format numerical columns
            if column in ['GrossVP', 'NetVP']:
                output[metric_name] = output[metric_name].apply(
                    lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}"
                )
            else:
                output[metric_name] = output[metric_name].apply(lambda x: f"{int(x):.0f}")

            # Shorten column names
            output.columns = ['Player', 'Score', 'TEG', 'Year']

            # Reset index
            output = output.reset_index(drop=True)

            # Sort the DataFrame
            output = output.sort_values(by='Score', ascending=sort_ascending)

            # Display
            st.subheader(f"Best {metric_name} by TEG")
            st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

        # Loop over each metric and display worst values
        for metric_name, column in metrics.items():
            if column == 'Stableford':
                worst_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
                sort_ascending = True
            else:
                worst_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
                sort_ascending = False

            worst_metric_name = f"Worst {metric_name}"

            output = worst_values[['Player', column, 'TEG', 'Year']].rename(columns={column: worst_metric_name})

            # Format numerical columns
            if column in ['GrossVP', 'NetVP']:
                output[worst_metric_name] = output[worst_metric_name].apply(
                    lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}"
                )
            else:
                output[worst_metric_name] = output[worst_metric_name].apply(lambda x: f"{int(x):.0f}")

            # Shorten column names
            output.columns = ['Player', 'Score', 'TEG', 'Year']

            # Reset index
            output = output.reset_index(drop=True)

            # Sort the DataFrame
            output = output.sort_values(by='Score', ascending=sort_ascending)

            # Display
            st.subheader(f"Worst {metric_name} by TEG")
            st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

    except KeyError as e:
        st.error(f"KeyError encountered in TEG Metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in TEG Metrics: {e}")

def show_round_metrics(all_data):
    st.header("Player Metrics Overview - Round Level")
    
    try:
        # Aggregate data at Round level
        round_data = aggregate_data(data=all_data, aggregation_level='Round')
        # st.write("**Aggregated Round Data:**", round_data.head())

        # Load additional round information
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #round_info_path = os.path.join(current_dir, 'data', 'round_info.csv')
        round_info_path = '../data/round_info.csv'
        if not os.path.exists(round_info_path):
            st.error(f"round_info.csv not found at path: {round_info_path}")
            return

        round_info = pd.read_csv(round_info_path)
        # st.write("**Round Info Data:**", round_info.head())

        # Drop 'Course' and 'Date' from round_data if they exist to avoid conflicts
        if 'Course' in round_data.columns:
            round_data = round_data.drop(columns=['Course'])
            # st.write("'Course' column dropped from Round Data to avoid conflicts.")
        if 'Date' in round_data.columns:
            round_data = round_data.drop(columns=['Date'])
            # st.write("'Date' column dropped from Round Data to avoid conflicts.")

        # Merge round_data with round_info to add 'Course' and 'Date'
        df_merged = pd.merge(round_data, round_info[['TEG', 'Round', 'Course', 'Date']], on=['TEG', 'Round'], how='left')
        # st.write("**Merged Round Data:**", df_merged.head())

        # Define metrics and aggregation functions (excluding Sc for Round)
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

        # Loop over each metric and display best values
        for metric_name, column in metrics.items():
            if column == 'Stableford':
                best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
                sort_ascending = False
            else:
                best_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
                sort_ascending = True

            # Create 'Round' column
            best_values['Round_Display'] = best_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)

            output = best_values[['Player', column, 'Round_Display', 'Course', 'Date']].rename(columns={
                column: 'Score',
                'Round_Display': 'Round'
            })

            # Sort before formatting
            output = output.sort_values(by='Score', ascending=sort_ascending)

            # Format numerical columns
            if column in ['GrossVP', 'NetVP']:
                output['Score'] = output['Score'].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
            else:
                output['Score'] = output['Score'].apply(lambda x: f"{int(x):.0f}")

            # Shorten column names
            output.columns = ['Player', 'Score', 'Round', 'Course', 'Date']

            # Reset index
            output = output.reset_index(drop=True)

            # Display
            st.subheader(f"Best {metric_name} by Round")
            st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

        # Loop over each metric and display worst values
        for metric_name, column in metrics.items():
            if column == 'Stableford':
                worst_values = df_merged.loc[df_merged.groupby('Player')[column].idxmin()]
                sort_ascending = True
            else:
                worst_values = df_merged.loc[df_merged.groupby('Player')[column].idxmax()]
                sort_ascending = False

            # Create 'Round' column
            worst_values['Round_Display'] = worst_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)

            output = worst_values[['Player', column, 'Round_Display', 'Course', 'Date']].rename(columns={
                column: 'Score',
                'Round_Display': 'Round'
            })

            # Sort before formatting
            output = output.sort_values(by='Score', ascending=sort_ascending)

            # Format numerical columns
            if column in ['GrossVP', 'NetVP']:
                output['Score'] = output['Score'].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}")
            else:
                output['Score'] = output['Score'].apply(lambda x: f"{int(x):.0f}")

            # Shorten column names
            output.columns = ['Player', 'Score', 'Round', 'Course', 'Date']

            # Reset index
            output = output.reset_index(drop=True)

            # Display
            st.subheader(f"Worst {metric_name} by Round")
            st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

    except KeyError as e:
        st.error(f"KeyError encountered in Round Metrics: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred in Round Metrics: {e}")

def show_about():
    st.header("About This Application")
    st.write("""
    ### Player Metrics Overview

    This application provides an overview of player metrics at both the TEG and Round levels. Navigate through the tabs to explore detailed statistics and performance indicators.

    **Tabs:**
    - **TEG Metrics:** Displays the best and worst metrics for players aggregated at the TEG level.
    - **Round Metrics:** Shows the best and worst metrics for players aggregated at the Round level.
    - **About:** Information about the application and its purpose.
    """)


if __name__ == "__main__":
    main()

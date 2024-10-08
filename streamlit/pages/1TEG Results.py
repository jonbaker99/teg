import streamlit as st
import pandas as pd
from typing import Any
import os
import logging
from utils import get_teg_rounds


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
FILE_PATH = '../data/all-data.parquet'
PAGE_TITLE = "Golf Scores"
PAGE_ICON = "⛳"
MEASURES = ['Sc', 'GrossVP', 'NetVP', 'Stableford']

def get_player_column(df: pd.DataFrame) -> str:
    """Determine the player column name."""
    if 'Player' in df.columns:
        return 'Player'
    elif 'Pl' in df.columns:
        return 'Pl'
    else:
        logger.error("Neither 'Player' nor 'Pl' column found in data.")
        raise KeyError("Data must contain either 'Player' or 'Pl' column.")

@st.cache_data
def load_data(file_path: str, file_mtime: float) -> pd.DataFrame:
    """
    Load data from a Parquet file.

    Args:
        file_path (str): Path to the Parquet file.
        file_mtime (float): Last modification time of the file.

    Returns:
        pd.DataFrame: Loaded data.

    Raises:
        FileNotFoundError: If the file is not found.
    """
    if not os.path.exists(file_path):
        logger.error(f"The file {file_path} does not exist.")
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    try:
        df = pd.read_parquet(file_path)
        logger.info(f"Data loaded successfully from {file_path}.")
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise e

@st.cache_data
def aggregate_to_round_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate data to round level.

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        pd.DataFrame: Aggregated dataframe.
    """
    player_column = get_player_column(df)
    group_columns = [player_column, 'TEGNum', 'TEG', 'Round']
    aggregated_df = df.groupby(group_columns, as_index=False)[MEASURES].sum()
    aggregated_df = aggregated_df.sort_values(by=[player_column, 'TEGNum', 'Round'])
    logger.info("Data aggregated to round level.")
    return aggregated_df

@st.cache_data
def create_leaderboard(leaderboard_df: pd.DataFrame, value_column: str, ascending: bool = True) -> pd.DataFrame:
    """
    Create a leaderboard from the given dataframe.

    Args:
        leaderboard_df (pd.DataFrame): Input dataframe.
        value_column (str): Column to use for ranking.
        ascending (bool): Whether to sort in ascending order.

    Returns:
        pd.DataFrame: Leaderboard dataframe.
    """
    player_column = get_player_column(leaderboard_df)

    pivot_df = leaderboard_df.pivot_table(
        index=player_column, 
        columns='Round', 
        values=value_column, 
        aggfunc='sum', 
        fill_value=0
    ).assign(Total=lambda x: x.sum(axis=1)).sort_values('Total', ascending=ascending)

    pivot_df.columns = [f'R{col}' if isinstance(col, int) else col for col in pivot_df.columns]
    pivot_df = pivot_df.reset_index()
    pivot_df['Rank'] = pivot_df['Total'].rank(method='min', ascending=ascending).astype(int)

    duplicated_scores = pivot_df['Total'].duplicated(keep=False)
    pivot_df.loc[duplicated_scores, 'Rank'] = pivot_df.loc[duplicated_scores, 'Rank'].astype(str) + '='

    columns = ['Rank', player_column] + [col for col in pivot_df.columns if col not in ['Rank', player_column]]
    leaderboard = pivot_df[columns]
    logger.info(f"Leaderboard created for {value_column}.")
    return leaderboard

def get_custom_css() -> str:
    """
    Get custom CSS for the Streamlit app.

    Returns:
        str: Custom CSS string.
    """
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        .datawrapper-table {
            font-family: Roboto, Arial, sans-serif !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            font-size: 14px !important;
            width: 100%;
            max-width: 600px; /* Set maximum width to 600px */
            margin-bottom: 40px !important;
        }
        .datawrapper-table th, .datawrapper-table td {
            text-align: center !important;
            padding: 12px 8px !important;
            border: none !important;
            border-bottom: 1px solid #e0e0e0 !important;
            word-wrap: break-word; /* Ensure text wraps within flexible widths */
        }
        .datawrapper-table th {
            font-weight: bold !important;
            border-bottom: 2px solid #000 !important;
        }
        .datawrapper-table th.rank-header { /* Specific class for Rank header */
            /* Leave content empty to hide the Rank header text but keep the border */
            padding: 12px 8px !important; /* Maintain padding for the horizontal rule */
        }
        .datawrapper-table tr:hover {
            background-color: #f5f5f5 !important;
        }
        .datawrapper-table .total {
            font-weight: bold !important;
        }
        .datawrapper-table td:nth-child(2),
        .datawrapper-table th:nth-child(2) {
            text-align: left !important;
        }
        .datawrapper-table td:first-child,
        .datawrapper-table th:first-child {
            font-size: 12px !important;
            width: 30px !important;
            max-width: 30px !important;
        }
        .datawrapper-table .top-rank {
            background-color: #f7f7f7 !important;
        }
        .leaderboard-header {
            font-size: 18px !important;
            margin-top: 30px !important;
            margin-bottom: 0px !important;
            padding: 0px;
        }
        .divider {
            border-top: 1px solid #e0e0e0;
            margin: 40px 0;
        }

        /* Responsive design: hide specific columns on very small screens */
        @media (max-width: 300px) {
            /* Hide all columns except first two and last */
            .datawrapper-table th:not(:first-child):not(:nth-child(2)):not(:last-child),
            .datawrapper-table td:not(:first-child):not(:nth-child(2)):not(:last-child) {
                display: none;
            }
        }
    </style>
    """

def generate_table_html(df: pd.DataFrame) -> str:
    """
    Generate HTML table from dataframe.

    Args:
        df (pd.DataFrame): Input dataframe.

    Returns:
        str: HTML table string.
    """
    html = ["<table class='datawrapper-table'>"]
    # Modified header: blank header for 'Rank'
    html.append("<thead><tr><th class='rank-header'></th>" + "".join(f"<th>{col}</th>" for col in df.columns[1:]) + "</tr></thead><tbody>")

    for _, row in df.iterrows():
        row_class = ' class="top-rank"' if str(row['Rank']).startswith('1') else ''
        html.append(f"<tr{row_class}>")
        for col in df.columns:
            cell_class = ' class="total"' if col == 'Total' else ''
            html.append(f'<td{cell_class}>{row[col]}</td>')
        html.append("</tr>")

    html.append("</tbody></table>")
    return "".join(html)

def format_grossvp(value: Any) -> str:
    """
    Format GrossVP values with + for positive, - for negative, and = for zero.

    Args:
        value (Any): The value to format.

    Returns:
        str: Formatted GrossVP string.
    """
    try:
        num = float(value)
        if num > 0:
            return f"+{int(num)}" if num.is_integer() else f"+{num}"
        elif num < 0:
            return f"{int(num)}" if num.is_integer() else f"{num}"
        else:
            return "="
    except (ValueError, TypeError):
        return str(value)

def format_stableford(value: Any) -> str:
    """
    Format Stableford values as integers.

    Args:
        value (Any): The value to format.

    Returns:
        str: Formatted Stableford string.
    """
    try:
        num = int(round(float(value)))  # Ensure it's an integer
        return f"{num}"
    except (ValueError, TypeError):
        return str(value)

def get_champions(df: pd.DataFrame, player_column: str) -> str:
    """
    Get champions from dataframe.

    Args:
        df (pd.DataFrame): Input dataframe.
        player_column (str): Name of the player column.

    Returns:
        str: Comma-separated list of champions.
    """
    champions = df[df['Rank'] == 1][player_column].astype(str).tolist()
    return ', '.join(champions)

def display_leaderboard(leaderboard_df: pd.DataFrame, value_column: str, title: str, leader_label: str, ascending: bool) -> None:
    """
    Display a leaderboard.

    Args:
        leaderboard_df (pd.DataFrame): Input dataframe.
        value_column (str): Column to use for ranking.
        title (str): Title of the leaderboard.
        leader_label (str): Label for the leader/champion.
        ascending (bool): Whether to sort in ascending order.
    """
    leaderboard = create_leaderboard(leaderboard_df, value_column, ascending)
    player_column = get_player_column(leaderboard)
    champions = get_champions(leaderboard, player_column)

    # Identify columns to format (all columns except 'Rank' and player_column)
    columns_to_format = [col for col in leaderboard.columns if col not in ['Rank', player_column]]

    # Apply formatting based on the value_column
    if value_column == 'Stableford':
        for col in columns_to_format:
            leaderboard[col] = leaderboard[col].apply(format_stableford)
    elif value_column == 'GrossVP':
        for col in columns_to_format:
            leaderboard[col] = leaderboard[col].apply(format_grossvp)

    st.markdown(f"""
        <h3 class='leaderboard-header'>{title}</h3>
        <p>{leader_label}: {champions}</p>
        """, unsafe_allow_html=True)

    table_html = generate_table_html(leaderboard)
    st.markdown(table_html, unsafe_allow_html=True)

def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Optional: Add a manual refresh button
    if st.sidebar.button("Refresh Data"):
        st.cache_data.clear()
        st.experimental_rerun()

    try:
        with st.spinner("Loading data..."):
            # Get the file's last modification time
            file_mtime = os.path.getmtime(FILE_PATH)
            df = load_data(FILE_PATH, file_mtime)

            # Determine player column
            try:
                player_column = get_player_column(df)
            except KeyError as e:
                st.error(str(e))
                logger.error(str(e))
                st.stop()

            # Aggregate data
            round_df = aggregate_to_round_level(df)

            # Validate required columns after aggregation
            required_columns = [player_column, 'TEGNum', 'TEG', 'Round', 'Stableford', 'GrossVP', 'NetVP', 'Sc']
            missing_columns = [col for col in required_columns if col not in round_df.columns]
            if missing_columns:
                st.error(f"Missing columns in data: {', '.join(missing_columns)}")
                logger.error(f"Missing columns in data: {', '.join(missing_columns)}")
                st.stop()

        teg_order = round_df[['TEG', 'TEGNum']].drop_duplicates().sort_values('TEGNum')
        tegs = teg_order['TEG'].tolist()

        if not tegs:
            st.warning("No TEGs available in the data.")
            st.stop()

        # Move radio buttons to the sidebar
        chosen_teg = st.sidebar.radio('Select TEG', tegs, horizontal=True)

        leaderboard_df = round_df[round_df['TEG'] == chosen_teg]

        if leaderboard_df.empty:
            st.warning(f"No data available for {chosen_teg}.")
            st.stop()

        # Determine if the selected TEG is complete
        current_rounds = leaderboard_df['Round'].nunique()
        total_rounds = get_teg_rounds(chosen_teg)
        is_complete = current_rounds >= total_rounds

        # Set titles based on TEG completion
        page_header = f"{chosen_teg} Results" if is_complete else f"{chosen_teg} Scoreboard"
        leader_label = "Champion" if is_complete else "Leader"

        st.subheader(page_header)

        # Display Stableford Leaderboard
        display_leaderboard(
            leaderboard_df, 
            'Stableford', 
            "TEG Trophy Leaderboard (Best Stableford)",  # Changed "Result" to "Leaderboard"
            leader_label, 
            ascending=False
        )

        # Display GrossVP Leaderboard
        display_leaderboard(
            leaderboard_df, 
            'GrossVP', 
            "Green Jacket Leaderboard (Best Gross)",  # Changed "Result" to "Leaderboard"
            leader_label, 
            ascending=True
        )

    except FileNotFoundError as e:
        st.error(f"Error: {str(e)}")
        logger.error(f"FileNotFoundError: {str(e)}")
    except KeyError as e:
        st.error(f"Missing column in data: {str(e)}")
        logger.error(f"KeyError: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Exception: {str(e)}")

if __name__ == "__main__":
    main()

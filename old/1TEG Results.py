import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import os

# Constants
FILE_PATH = '../data/all-data.parquet'
PAGE_TITLE = "Golf Scores"
PAGE_ICON = "⛳"
MEASURES = ['Sc', 'GrossVP', 'NetVP', 'Stableford']

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        pd.DataFrame: Loaded data.
    
    Raises:
        FileNotFoundError: If the file is not found.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    #return pd.read_csv(file_path)
    return pd.read_parquet(file_path)

@st.cache_data
def aggregate_to_round_level(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate data to round level.
    
    Args:
        df (pd.DataFrame): Input dataframe.
    
    Returns:
        pd.DataFrame: Aggregated dataframe.
    """
    player_column = 'Player' if 'Player' in df.columns else 'Pl'
    group_rd = [player_column, 'TEGNum', 'TEG', 'Round']
    return df.groupby(group_rd, as_index=False)[MEASURES].sum().sort_values(by=[player_column,'TEGNum','Round'])

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
    player_column = 'Player' if 'Player' in leaderboard_df.columns else 'Pl'
    
    jacketboard_pivot = leaderboard_df.pivot_table(
        index=player_column, 
        columns='Round', 
        values=value_column, 
        aggfunc='sum', 
        fill_value=0
    ).assign(Total=lambda x: x.sum(axis=1)).sort_values('Total', ascending=ascending)

    jacketboard_pivot.columns = [f'R{col}' if isinstance(col, int) else col for col in jacketboard_pivot.columns]

    jacketboard_pivot = jacketboard_pivot.reset_index()
    jacketboard_pivot['Rank'] = jacketboard_pivot['Total'].rank(method='min', ascending=ascending).astype(int)

    duplicated_scores = jacketboard_pivot['Total'].duplicated(keep=False)
    jacketboard_pivot.loc[duplicated_scores, 'Rank'] = jacketboard_pivot.loc[duplicated_scores, 'Rank'].astype(str) + '='

    columns = ['Rank', player_column] + [col for col in jacketboard_pivot.columns if col not in ['Rank', player_column]]
    return jacketboard_pivot[columns]

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
            margin-bottom: 40px !important;
        }
        .datawrapper-table th, .datawrapper-table td {
            text-align: center !important;
            padding: 12px 8px !important;
            border: none !important;
            border-bottom: 1px solid #e0e0e0 !important;
        }
        .datawrapper-table th {
            font-weight: bold !important;
            border-bottom: 2px solid #000 !important;
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
        .datawrapper-table td:first-child {
            font-size: 12px !important;
            width: 30px !important;
            max-width: 30px !important;
        }
        .datawrapper-table th:first-child {
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
    html = ["<table class='datawrapper-table' style='min-width: 380px; max-width: 600px' >"]
    html.append("<tr><th></th>" + "".join(f"<th>{col}</th>" for col in df.columns[1:]) + "</tr>")
    
    for _, row in df.iterrows():
        row_class = ' class="top-rank"' if row['Rank'] in [1, '1='] else ''
        html.append(f"<tr{row_class}>")
        for i, value in enumerate(row):
            cell_class = ' class="total"' if df.columns[i] == 'Total' else ''
            html.append(f'<td{cell_class}>{value}</td>')
        html.append("</tr>")
    
    html.append("</table>")
    return "".join(html)

def get_champions(df: pd.DataFrame) -> str:
    """
    Get champions from dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe.
    
    Returns:
        str: Comma-separated list of champions.
    """
    return ', '.join(df[df['Rank'] == 1]['Player'].tolist())

def display_leaderboard(leaderboard_df: pd.DataFrame, value_column: str, title: str, ascending: bool) -> None:
    """
    Display a leaderboard.
    
    Args:
        leaderboard_df (pd.DataFrame): Input dataframe.
        value_column (str): Column to use for ranking.
        title (str): Title of the leaderboard.
        ascending (bool): Whether to sort in ascending order.
    """
    leaderboard = create_leaderboard(leaderboard_df, value_column, ascending)
    champions = get_champions(leaderboard)
    st.markdown(f"""
        <h3 class='leaderboard-header'>{title}</h3>
        <p>Champion: {champions}</p>
        """, unsafe_allow_html=True)
    table_html = generate_table_html(leaderboard)
    st.markdown(table_html, unsafe_allow_html=True)

def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    try:
        with st.spinner("Loading data..."):
            df = load_data(FILE_PATH)
            round_df = aggregate_to_round_level(df)

        teg_order = round_df[['TEG', 'TEGNum']].drop_duplicates().sort_values('TEGNum')
        tegs = teg_order['TEG'].tolist()
        
        chosen_teg = st.radio('Select TEG', tegs, horizontal=True)

        leaderboard_df = round_df[round_df['TEG'] == chosen_teg]

        st.subheader(f'{chosen_teg} results')

        display_leaderboard(leaderboard_df, 'Stableford', "TEG Trophy result (best Stableford)", ascending=False)
        display_leaderboard(leaderboard_df, 'GrossVP', "Green Jacket result (best gross)", ascending=True)

    except FileNotFoundError as e:
        st.error(f"Error: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
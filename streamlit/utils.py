import pandas as pd
from math import floor
import gspread
from google.oauth2.service_account import Credentials
import logging
from typing import Dict, Any

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONFIG: Dict[str, str] = {
    "ROUND_INFO_PATH": "../data/round_info.csv"
}

# Function to retrieve player name from initials
def get_player_name(initials: str) -> str:
    """
    Retrieve the player's full name based on their initials.

    Parameters:
        initials (str): The initials of the player.

    Returns:
        str: Full name of the player or 'Unknown Player' if not found.
    """
    player_dict = {
        'AB': 'Alex BAKER',
        'JB': 'Jon BAKER',
        'DM': 'David MULLIN',
        'GW': 'Gregg WILLIAMS',
        'HM': 'Henry MELLER',
        'SN': 'Stuart NEUMANN',
        'JP': 'John PATTERSON',
        # Add more player initials and names as needed
    }
    return player_dict.get(initials.upper(), 'Unknown Player')

def process_round_for_all_scores(long_df: pd.DataFrame, hc_long: pd.DataFrame) -> pd.DataFrame:
    """
    Process round data for all scores by computing various metrics.

    Parameters:
        long_df (pd.DataFrame): DataFrame containing round data.
        hc_long (pd.DataFrame): DataFrame containing handicap data.

    Returns:
        pd.DataFrame: Processed DataFrame with additional computed columns.
    """
    logger.info("Processing rounds for all scores.")
    
    # Replace 'Score' with 'Sc' if it exists
    if 'Score' in long_df.columns:
        long_df['Sc'] = long_df['Score']
        long_df.drop('Score', axis=1, inplace=True)
        logger.debug("'Score' column renamed to 'Sc'.")
    else:
        logger.warning("'Score' column not found. Skipping 'Sc' creation.")
    
    # Rename 'Par' to 'PAR'
    if 'Par' in long_df.columns:
        long_df['PAR'] = long_df['Par']
        long_df.drop('Par', axis=1, inplace=True)
        logger.debug("'Par' column renamed to 'PAR'.")
    else:
        logger.warning("'Par' column not found. Skipping 'PAR' creation.")
    
    # Create 'TEG' column
    long_df['TEG'] = 'TEG ' + long_df['TEGNum'].astype(str)
    
    # Merge handicap data
    long_df = long_df.merge(hc_long, on=['TEG', 'Pl'], how='left')
    logger.debug("Handicap data merged.")
    
    # Fill NaN values in 'HC' with 0
    long_df['HC'] = long_df['HC'].fillna(0)
    
    # Create 'HoleID'
    long_df['HoleID'] = long_df.apply(
        lambda row: f"T{int(row['TEGNum']):02}|R{int(row['Round']):02}|H{int(row['Hole']):02}", axis=1
    )
    
    # Determine 'FrontBack'
    long_df['FrontBack'] = long_df['Hole'].apply(lambda hole: 'Front' if hole < 10 else 'Back')
    
    # Map player names
    long_df['Player'] = long_df['Pl'].apply(get_player_name)
    
    # Calculate 'HCStrokes'
    long_df['HCStrokes'] = long_df.apply(
        lambda row: 1 * (row['HC'] % 18 >= row['SI']) + floor(row['HC'] / 18), axis=1
    )
    
    # Calculate 'GrossVP'
    long_df['GrossVP'] = long_df['Sc'] - long_df['PAR']
    
    # Calculate 'Net'
    long_df['Net'] = long_df['Sc'] - long_df['HCStrokes']
    
    # Calculate 'NetVP'
    long_df['NetVP'] = long_df['Net'] - long_df['PAR']
    
    # Calculate 'Stableford'
    long_df['Stableford'] = long_df['NetVP'].apply(lambda x: max(0, 2 - x))
    
    logger.info("Round processing completed.")
    return long_df

def check_hc_strokes_combinations(transformed_df: pd.DataFrame) -> None:
    """
    Check and copy unique combinations of HC, SI, and HCStrokes to the clipboard.

    Parameters:
        transformed_df (pd.DataFrame): DataFrame containing the transformed golf data.
    """
    hc_si_strokes_df = transformed_df[['HC', 'SI', 'HCStrokes']].drop_duplicates()
    hc_si_strokes_df.to_clipboard(index=False)
    logger.info("Unique combinations of HC, SI, and HCStrokes copied to clipboard.")

def add_cumulative_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cumulative scores and averages for specified measures across rounds, TEGs, and career.

    Parameters:
        df (pd.DataFrame): DataFrame containing the golf data.

    Returns:
        pd.DataFrame: DataFrame with cumulative and average scores added.
    """
    logger.info("Adding cumulative scores and averages.")
    
    # Sort data
    df = df.sort_values(by=['Pl', 'TEGNum', 'Round', 'Hole'])
    
    # Create 'Hole Order Ever'
    df['Hole Score'] = 1000 * df['TEGNum'] + 100 * df['Round'] + df['Hole']
    df['Hole Order Ever'] = df['Hole Score'].rank(method='dense').astype(int)
    df.drop(columns=['Hole Score'], inplace=True)
    
    measures = ['Sc', 'GrossVP', 'NetVP', 'Stableford']
    group_rd = ['Pl', 'TEGNum', 'Round']
    group_teg = ['Pl', 'TEGNum']
    group_career = ['Pl']
    
    for measure in measures:
        df[f'{measure} Cum Round'] = df.groupby(group_rd)[measure].cumsum()
        df[f'{measure} Cum TEG'] = df.groupby(group_teg)[measure].cumsum()
        df[f'{measure} Cum Career'] = df.groupby(group_career)[measure].cumsum()
    
    # Add counts
    df['TEG Count'] = df.groupby(group_teg).cumcount() + 1
    df['Career Count'] = df.groupby(group_career).cumcount() + 1
    
    # Add averages
    for measure in measures:
        df[f'{measure} Round Avg'] = df[f'{measure} Cum Round'] / df['Hole']
        df[f'{measure} TEG Avg'] = df[f'{measure} Cum TEG'] / df['TEG Count']
        df[f'{measure} Career Avg'] = df[f'{measure} Cum Career'] / df['Career Count']
    
    logger.info("Cumulative scores and averages added.")
    return df

def save_to_parquet(df: pd.DataFrame, output_file: str) -> None:
    """
    Save DataFrame to a Parquet file.

    Parameters:
        df (pd.DataFrame): DataFrame containing the updated golf data.
        output_file (str): Path to save the Parquet file.
    """
    df.to_parquet(output_file, index=False)
    logger.info(f"Data successfully saved to {output_file}")

def get_google_sheet(sheet_name: str, worksheet_name: str, creds_path: str) -> pd.DataFrame:
    """
    Load data from a specified Google Sheet and worksheet.

    Parameters:
        sheet_name (str): The name of the Google Sheet.
        worksheet_name (str): The name of the worksheet within the Google Sheet.
        creds_path (str): The path to the service account credentials JSON file.

    Returns:
        pd.DataFrame: DataFrame containing the data from the specified worksheet.
    """
    logger.info(f"Fetching data from Google Sheet: {sheet_name}, Worksheet: {worksheet_name}")
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    logger.info("Data fetched successfully from Google Sheets.")
    return df

def reshape_round_data(df: pd.DataFrame, id_vars: list) -> pd.DataFrame:
    """
    Reshape round data from wide to long format.

    Parameters:
        df (pd.DataFrame): Original wide-format DataFrame.
        id_vars (list): List of identifier variables.

    Returns:
        pd.DataFrame: Reshaped long-format DataFrame.
    """
    logger.info("Reshaping round data to long format.")
    player_columns = df.columns[len(id_vars):].tolist()
    long_df = pd.melt(df, id_vars=id_vars, value_vars=player_columns, var_name='Pl', value_name='Score')
    long_df['Score'] = pd.to_numeric(long_df['Score'], errors='coerce')
    reshaped_df = long_df.dropna(subset=['Score'])
    reshaped_df = reshaped_df[reshaped_df['Score'] != 0]
    logger.info("Round data reshaped successfully.")
    return reshaped_df

def load_and_prepare_handicap_data(file_path: str) -> pd.DataFrame:
    """
    Load and prepare handicap data from a CSV file.

    Parameters:
        file_path (str): Path to the handicap CSV file.

    Returns:
        pd.DataFrame: Melted and cleaned handicap DataFrame.
    """
    logger.info(f"Loading handicap data from {file_path}")
    hc_lookup = pd.read_csv(file_path)
    hc_long = pd.melt(hc_lookup, id_vars='TEG', var_name='Pl', value_name='HC')
    hc_long = hc_long.dropna(subset=['HC'])
    hc_long = hc_long[hc_long['HC'] != 0]
    logger.info("Handicap data loaded and prepared.")
    return hc_long

def summarise_existing_rd_data(existing_rows: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize existing round data.

    Parameters:
        existing_rows (pd.DataFrame): DataFrame containing existing rows.

    Returns:
        pd.DataFrame: Pivoted summary DataFrame.
    """
    logger.info("Summarizing existing round data.")
    existing_summary_df = existing_rows.groupby(['TEGNum', 'Round', 'Pl'])['Sc'].sum().reset_index()
    existing_summary_pivot = existing_summary_df.pivot(index='Pl', columns=['Round', 'TEGNum'], values='Sc')
    summary = existing_summary_pivot.fillna('-').astype(str).replace(r'\.0$', '', regex=True)
    logger.info("Existing round data summarized.")
    return summary

def add_round_info(all_data):
    # Read the round info CSV file
    round_info = pd.read_csv(CONFIG["ROUND_INFO_PATH"])

    # Merge the round info with all_data based on TEGNum and Round
    merged_data = pd.merge(
        all_data,
        round_info[['TEGNum', 'Round', 'Date', 'Course']],
        on=['TEGNum', 'Round'],
        how='left'
    )

    return merged_data

def update_all_data(csv_file: str, parquet_file: str, csv_output_file: str) -> None:
    """
    Load data from a CSV file, apply cumulative scores and averages, and save it as both a Parquet file and a CSV file.

    Parameters:
        csv_file (str): Path to the input CSV file.
        parquet_file (str): Path to the output Parquet file.
        csv_output_file (str): Path to the output CSV file for review.
    """
    logger.info(f"Updating all data from {csv_file} to {parquet_file} and {csv_output_file}")
    
    # Load the CSV file
    df = pd.read_csv(csv_file)
    logger.debug("CSV data loaded.")
    
    # Add round info
    df = add_round_info(df)
    logger.debug("Round info added.")

    # Apply cumulative score and average calculations
    df_transformed = add_cumulative_scores(df)
    logger.debug("Cumulative scores and averages applied.")
    
    # Save the transformed dataframe to a Parquet file
    save_to_parquet(df_transformed, parquet_file)
    
    # Save the transformed dataframe to a CSV file for manual review
    df_transformed.to_csv(csv_output_file, index=False)
    logger.info(f"Transformed data saved to {csv_output_file}")


def check_for_complete_and_duplicate_data(all_scores_path: str, all_data_path: str) -> Dict[str, pd.DataFrame]:
    """
    Check for complete and duplicate data in the all-scores (CSV) and all-data (Parquet) files.
    Each unique combination of TEG, Round, and Player (Pl) should have exactly 18 entries.

    Parameters:
        all_scores_path (str): Path to the all-scores CSV file.
        all_data_path (str): Path to the all-data Parquet file.

    Returns:
        Dict[str, pd.DataFrame]: Summary of incomplete and duplicate data.
    """
    logger.info("Checking for complete and duplicate data.")
    
    # Load the all-scores CSV file and the all-data Parquet file
    all_scores_df = pd.read_csv(all_scores_path)
    all_data_df = pd.read_parquet(all_data_path)
    logger.debug("All-scores and all-data files loaded.")
    
    # Group by TEG, Round, and Player and count the number of entries
    all_scores_count = all_scores_df.groupby(['TEGNum', 'Round', 'Pl']).size().reset_index(name='EntryCount')
    all_data_count = all_data_df.groupby(['TEGNum', 'Round', 'Pl']).size().reset_index(name='EntryCount')
    
    # Check for incomplete and duplicate data in all-scores.csv
    incomplete_scores = all_scores_count[all_scores_count['EntryCount'] < 18]
    duplicate_scores = all_scores_count[all_scores_count['EntryCount'] > 18]
    
    # Check for incomplete and duplicate data in all-data.parquet
    incomplete_data = all_data_count[all_data_count['EntryCount'] < 18]
    duplicate_data = all_data_count[all_data_count['EntryCount'] > 18]
    
    # Summarize the results
    summary: Dict[str, Any] = {
        'incomplete_scores': incomplete_scores,
        'duplicate_scores': duplicate_scores,
        'incomplete_data': incomplete_data,
        'duplicate_data': duplicate_data
    }
    
    # Log the summary
    if not incomplete_scores.empty:
        logger.warning("Incomplete data found in all-scores.csv.")
    else:
        logger.info("No incomplete data found in all-scores.csv.")
    
    if not duplicate_scores.empty:
        logger.warning("Duplicate data found in all-scores.csv.")
    else:
        logger.info("No duplicate data found in all-scores.csv.")
    
    if not incomplete_data.empty:
        logger.warning("Incomplete data found in all-data.parquet.")
    else:
        logger.info("No incomplete data found in all-data.parquet.")
    
    if not duplicate_data.empty:
        logger.warning("Duplicate data found in all-data.parquet.")
    else:
        logger.info("No duplicate data found in all-data.parquet.")
    
    return summary

# utilities.py

# Mapping of TEGs to their total number of rounds
TEG_ROUNDS = {
    'TEG 1': 4,
    'TEG 2': 3,
    'TEG 3': 4,
    'TEG 4': 4
    # Add more TEGs if necessary
}

def get_teg_rounds(TEG):
    """
    Function to return the number of rounds for a given TEG.
    If the TEG is not found in the dictionary, return 4 as the default value.
    
    Args:
    TEG (str): The TEG identifier (e.g., 'TEG 1', 'TEG 2', etc.)
    
    Returns:
    int: The total number of rounds for the given TEG, defaulting to 4 if not found.
    """
    return TEG_ROUNDS.get(TEG, 4)

# Generalized aggregation function with dynamic level of aggregation
def aggregate_data(data, aggregation_level, measures=['Sc', 'GrossVP', 'NetVP', 'Stableford']):
    levels = {
        'Pl': ['Pl', 'Player'],
        'TEG': ['Pl', 'TEG', 'Player', 'TEGNum'],
        'Round': ['Pl', 'TEG', 'Round', 'Player', 'TEGNum'],
        'FrontBack': ['Pl', 'TEG', 'Round', 'FrontBack', 'Player', 'TEGNum']
    }
    
    if aggregation_level not in levels:
        raise ValueError(f"Invalid aggregation level: {aggregation_level}. Choose from: {list(levels.keys())}")
    
    group_columns = levels[aggregation_level]
    return data.groupby(group_columns, as_index=False)[measures].sum().sort_values(by=group_columns)

def format_vs_par(value):
    if value > 0:
        return f"+{int(value)}"
    elif value < 0:
        return f"{int(value)}"
    else:
        return "="

import pandas as pd
from math import floor
import gspread
from google.oauth2.service_account import Credentials

# Function to retrieve player name from initials
def get_player_name(initials):
    # Placeholder logic for player name lookup (you can customize this)
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
    return player_dict.get(initials, 'Unknown Player')

# Function to process round data and add missing fields for inclusion in the all-scores file
def process_round_for_all_scores(long_df, hc_long):
    # Score becomes Sc
    long_df['Sc'] = long_df['Score']
    long_df.drop('Score', axis=1, inplace=True)

    # Par becomes PAR
    long_df['PAR'] = long_df['Par']
    long_df.drop('Par', axis=1, inplace=True)

    # TEG = 'TEG ' + TEGNum
    long_df['TEG'] = 'TEG ' + long_df['TEGNum'].astype(str)

    # Merge the handicaps with the long_df data
    long_df = long_df.merge(hc_long, on=['TEG', 'Pl'], how='left')

    # Handle NaN values by creating a new DataFrame without using inplace
    long_df['HC'] = long_df['HC'].fillna(0)

    # HoleID = combination of TEG, Round, Hole in format 'T00|R00|H00'
    long_df['HoleID'] = long_df.apply(lambda row: f"T{int(row['TEGNum']):02}|R{int(row['Round']):02}|H{int(row['Hole']):02}", axis=1)

    # FrontBack = 'Front' if Hole < 10, otherwise 'Back'
    long_df['FrontBack'] = long_df['Hole'].apply(lambda hole: 'Front' if hole < 10 else 'Back')

    # Player = get player name from initials (Pl)
    long_df['Player'] = long_df['Pl'].apply(get_player_name)

    # HCStrokes = Excel formula equivalent =1*(MOD(HC,18)>=SI)+FLOOR(HC/18,1)
    long_df['HCStrokes'] = long_df.apply(lambda row: 1 * (row['HC'] % 18 >= row['SI']) + floor(row['HC'] / 18), axis=1)

    # GrossVP = Sc - PAR
    long_df['GrossVP'] = long_df['Sc'] - long_df['PAR']

    # Net
    long_df['Net'] = long_df['Sc'] - long_df['HCStrokes']

    # NetVP = GrossVP - HCStrokes
    long_df['NetVP'] = long_df['Net'] - long_df['PAR']

    # Stableford = max(0, 2 - NetVP)
    long_df['Stableford'] = long_df['NetVP'].apply(lambda x: max(0, 2 - x))

    return long_df

# Optional function for checking combinations of HC, SI, and HCStrokes
def check_hc_strokes_combinations(transformed_df):
    # Select the relevant columns for the check
    hc_si_strokes_df = transformed_df[['HC', 'SI', 'HCStrokes']]
    
    # Drop duplicates to get unique combinations
    unique_combinations = hc_si_strokes_df.drop_duplicates()
    
    # Copy the unique combinations to clipboard
    unique_combinations.to_clipboard(index=False)
    
    print("Unique combinations of HC, SI, and HCStrokes have been copied to the clipboard.")


import pandas as pd

def add_cumulative_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cumulative scores and averages for specified measures across rounds, TEGs, and career.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the golf data.
        
    Returns:
        pd.DataFrame: DataFrame with cumulative and average scores added.
    """
    # Sort data by Player, TEGNum, Round, and Hole
    df = df.sort_values(by=['Pl', 'TEGNum', 'Round', 'Hole'])

    # Create a 'Hole Order Ever' field
    df['Hole Score'] = 1000 * df['TEGNum'] + 100 * df['Round'] + df['Hole']
    df['Hole Order Ever'] = df['Hole Score'].rank(method='dense').astype(int)
    df.drop(columns=['Hole Score'], inplace=True)

    # Measures for which cumulative and average scores will be calculated
    measures = ['Sc', 'GrossVP', 'NetVP', 'Stableford']

    # Grouping for round, TEG, and career
    group_rd = ['Pl', 'TEGNum', 'Round']
    group_teg = ['Pl', 'TEGNum']
    group_career = ['Pl']

    # Add cumulative scores for each measure
    for measure in measures:
        df[f'{measure} Cum Round'] = df.groupby(group_rd)[measure].cumsum()
        df[f'{measure} Cum TEG'] = df.groupby(group_teg)[measure].cumsum()
        df[f'{measure} Cum Career'] = df.groupby(group_career)[measure].cumsum()

    # Add counts for TEG and career
    df['TEG Count'] = df.groupby(group_teg).cumcount() + 1
    df['Career Count'] = df.groupby(group_career).cumcount() + 1

    # Add average scores for each measure
    for measure in measures:
        df[f'{measure} Round Avg'] = df[f'{measure} Cum Round'] / df['Hole']  # Round Average
        df[f'{measure} TEG Avg'] = df[f'{measure} Cum TEG'] / df['TEG Count']  # TEG Average
        df[f'{measure} Career Avg'] = df[f'{measure} Cum Career'] / df['Career Count']  # Career Average

    return df

def save_to_parquet(df: pd.DataFrame, output_file: str):
    """
    Save DataFrame to a Parquet file.

    Parameters:
        df (pd.DataFrame): DataFrame containing the updated golf data.
        output_file (str): Path to save the Parquet file.
    """
    df.to_parquet(output_file, index=False)
    print(f"Data successfully saved to {output_file}")

def get_google_sheet(sheet_name: str, worksheet_name: str, creds_path: str):
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return pd.DataFrame(sheet.get_all_records())


def reshape_round_data(df: pd.DataFrame, id_vars: list) -> pd.DataFrame:
    player_columns = df.columns[len(id_vars):].tolist()
    long_df = pd.melt(df, id_vars=id_vars, value_vars=player_columns, var_name='Pl', value_name='Score')
    long_df['Score'] = pd.to_numeric(long_df['Score'], errors='coerce')
    return long_df.dropna(subset=['Score'])[long_df['Score'] != 0]

def load_and_prepare_handicap_data(file_path: str) -> pd.DataFrame:
    hc_lookup = pd.read_csv(file_path)
    return pd.melt(hc_lookup, id_vars='TEG', var_name='Pl', value_name='HC').dropna(subset=['HC']).query('HC != 0')

def summarise_existing_rd_data(existing_rows: pd.DataFrame) -> pd.DataFrame:
    existing_summary_df = existing_rows.groupby(['TEGNum', 'Round', 'Pl'])['Sc'].sum().reset_index()
    existing_summary_pivot = existing_summary_df.pivot(index='Pl', columns=['Round', 'TEGNum'], values='Sc')
    return existing_summary_pivot.fillna('-').astype(str).replace(r'\.0$', '', regex=True)

import pandas as pd

def update_all_data(csv_file: str, parquet_file: str, csv_output_file: str):
    """
    Loads data from a CSV file, applies cumulative scores and averages, and saves it as both a Parquet file and a CSV file.

    Parameters:
    csv_file (str): Path to the input CSV file.
    parquet_file (str): Path to the output Parquet file.
    csv_output_file (str): Path to the output CSV file for review.
    """
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Apply cumulative score and average calculations
    df_transformed = add_cumulative_scores(df)

    # Save the transformed dataframe to a Parquet file
    save_to_parquet(df_transformed, parquet_file)

    # Save the transformed dataframe to a CSV file for manual review
    df_transformed.to_csv(csv_output_file, index=False)

    print(f"Data successfully updated and saved to {parquet_file} and {csv_output_file}")

import pandas as pd

def check_for_complete_and_duplicate_data(all_scores_path: str, all_data_path: str):
    """
    Checks for complete and duplicate data in the all-scores (CSV) and all-data (Parquet) files.
    Each unique combination of TEG, Round, and Player (Pl) should have exactly 18 entries.

    Parameters:
    all_scores_path (str): Path to the all-scores CSV file.
    all_data_path (str): Path to the all-data Parquet file.

    Returns:
    dict: A summary of the incomplete and duplicate data.
    """
    # Load the all-scores CSV file and the all-data Parquet file
    all_scores_df = pd.read_csv(all_scores_path)
    all_data_df = pd.read_parquet(all_data_path)

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
    summary = {
        'incomplete_scores': incomplete_scores,
        'duplicate_scores': duplicate_scores,
        'incomplete_data': incomplete_data,
        'duplicate_data': duplicate_data
    }

    # Print a summary of the results
    if not incomplete_scores.empty:
        print("Incomplete data found in all-scores.csv:")
        print(incomplete_scores)
    else:
        print("No incomplete data found in all-scores.csv.")

    if not duplicate_scores.empty:
        print("Duplicate data found in all-scores.csv:")
        print(duplicate_scores)
    else:
        print("No duplicate data found in all-scores.csv.")

    if not incomplete_data.empty:
        print("Incomplete data found in all-data.parquet:")
        print(incomplete_data)
    else:
        print("No incomplete data found in all-data.parquet.")

    if not duplicate_data.empty:
        print("Duplicate data found in all-data.parquet:")
        print(duplicate_data)
    else:
        print("No duplicate data found in all-data.parquet.")

    return summary

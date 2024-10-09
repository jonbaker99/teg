from streamlit.utils import update_all_data, check_for_complete_and_duplicate_data

# Define file paths
ALL_SCORES_PATH = '../data/all-scores.csv'
HANDICAPS_PATH = '../data/handicaps.csv'
PARQUET_FILE = '../data/all-data.parquet'
CSV_OUTPUT_FILE = '../data/all-data.csv'

# Update all data
update_all_data(ALL_SCORES_PATH, PARQUET_FILE, CSV_OUTPUT_FILE)

# Check for complete and duplicate data
check_for_complete_and_duplicate_data(ALL_SCORES_PATH, PARQUET_FILE)

print("Data update and check completed successfully.")
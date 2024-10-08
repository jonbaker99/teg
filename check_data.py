from data_utilities import check_for_complete_and_duplicate_data

# Define the paths to your files
all_scores_path = 'data/all-scores.csv'
all_data_path = 'data/all-data.parquet'

# Run the check for complete and duplicate data
check_for_complete_and_duplicate_data(all_scores_path, all_data_path)

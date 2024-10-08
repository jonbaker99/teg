from data_utilities import update_all_data

# Define the path for input CSV, output Parquet, and output CSV files
csv_file = 'data/all-scores.csv'
parquet_file = 'data/all-data.parquet'
csv_output_file = 'data/all-data.csv'  # Path to the output CSV file for review

# Call the function to update all-data and save both Parquet and CSV files
update_all_data(csv_file, parquet_file, csv_output_file)

from data_utilities import (
    process_round_for_all_scores,
    get_google_sheet,
    reshape_round_data,
    load_and_prepare_handicap_data,
    summarise_existing_rd_data,
    update_all_data
)
import pandas as pd

# Fetch and reshape Google Sheet data
CREDS_PATH = r"credentials\maps-1489139675490-41bee944be4e.json"  # Path to your service account JSON file
df = get_google_sheet("TEG Round Input", "Scores", CREDS_PATH)
id_vars = ['TEGNum', 'Round', 'Hole', 'Par', 'SI']
long_df = reshape_round_data(df, id_vars)

# Filter rounds with 18 holes
rounds_with_18_holes = long_df.groupby(['TEGNum', 'Round', 'Pl']).filter(lambda x: len(x) == 18)

# Check if there's any data after filtering
if rounds_with_18_holes.empty:
    print("No rounds with 18 holes were found. Exiting process.")
    exit()

# Show a summary of the scores by Player, Round, and TEG from the Google Sheet data
summary_df = rounds_with_18_holes.groupby(['TEGNum', 'Round', 'Pl'])['Score'].sum().reset_index()
print("Score Summary from Google Sheets (by Player, Round, TEG):")
print(summary_df.pivot(index='Pl', columns=['Round', 'TEGNum'], values='Score'))

# Load and prepare handicap data
hc_long = load_and_prepare_handicap_data('data/handicaps.csv')

# Process rounds data
transformed_rounds = process_round_for_all_scores(rounds_with_18_holes, hc_long)

# Load and handle existing data
all_scores_path = 'data/all-scores.csv'
all_scores_df = pd.read_csv(all_scores_path)
new_tegs_rounds = transformed_rounds[['TEGNum', 'Round']].drop_duplicates()
existing_rows = all_scores_df.merge(new_tegs_rounds, on=['TEGNum', 'Round'], how='inner')

update_needed = False

# Check for existing rounds in all-scores.csv
if not existing_rows.empty:
    print("Existing scores found in all-scores.csv.")
    print(summarise_existing_rd_data(existing_rows))

    # Ask user whether to overwrite the data
    overwrite_all = input("Replace all existing scores with new data? (yes/no): ").lower()
    if overwrite_all == 'yes':
        print("Replacing data.")
        update_needed = True
        # Remove existing rounds that will be replaced
        all_scores_df = all_scores_df[~all_scores_df.set_index(['TEGNum', 'Round']).index.isin(new_tegs_rounds.set_index(['TEGNum', 'Round']).index)]
        all_scores_df = pd.concat([all_scores_df, transformed_rounds], ignore_index=True)
else:
    print("No existing rounds found. Appending new data.")
    update_needed = True
    all_scores_df = pd.concat([all_scores_df, transformed_rounds], ignore_index=True)

# Save updated data if needed
if update_needed:
    all_scores_df.to_csv(all_scores_path, index=False)
    print(f"Updated {all_scores_path} saved.")
    
    # Run the update_all_data process after saving the CSV
    csv_file = 'data/all-scores.csv'
    parquet_file = 'data/all-data.parquet'
    csv_output_file = 'data/all-data.csv'  # Path to the output CSV file for review
    update_all_data(csv_file, parquet_file, csv_output_file)
else:
    print("No changes made, CSV not saved.")

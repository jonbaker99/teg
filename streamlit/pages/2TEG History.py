import streamlit as st
import pandas as pd

FILE_PATH = '../data/all-data.parquet'
all_data = pd.read_parquet(FILE_PATH)

# Function to get summary of TEGs
def get_teg_summary(df):
    # Group by 'TEGNum' and 'Player', and calculate the sum for each player in each TEG
    grouped = df.groupby(['TEGNum','Player']).agg({
        'GrossVP': 'sum',
        'Stableford': 'sum'
    }).sort_values(by="TEGNum").reset_index()

    # Initialize a list to store the results for each TEG
    results = []

    # Get unique TEG values
    for teg in df['TEGNum'].unique():
        # Filter for the current TEG
        teg_data = grouped[grouped['TEGNum'] == teg]
        
        # Get the player with the lowest sum of GrossVP
        lowest_grossvp = teg_data.loc[teg_data['GrossVP'].idxmin()]
        
        # Get the player with the highest sum of Stableford
        highest_stableford = teg_data.loc[teg_data['Stableford'].idxmax()]
        
        # Get the player with the lowest sum of Stableford
        lowest_stableford = teg_data.loc[teg_data['Stableford'].idxmin()]
        
        # Append the result for this TEG
        results.append({
            'TEGNum': teg,
            'TEG': "TEG "+ str(teg),
            'Best Gross': lowest_grossvp['Player'],
            'Best Net': highest_stableford['Player'],
            'Worst Net': lowest_stableford['Player'],
        })
    

    # st.write(results)
    # Convert results to a DataFrame
    result_df = pd.DataFrame(results).sort_values(by='TEGNum').drop(columns=['TEGNum'])
    
    # Merge with year data from all_data
    all_data['Year'] = pd.to_datetime(all_data['Date'], format='%d/%m/%Y').dt.year
    teg_yr = all_data[['TEG', 'Year']].drop_duplicates()
    teg_yr['Year'] = teg_yr['Year'].fillna(0).astype(int).astype(str)
    results_with_year = pd.merge(result_df, teg_yr, on='TEG', how='left')
    
    # Reorder and select relevant columns
    results_with_year = results_with_year[['TEG', 'Year', 'Best Net', 'Best Gross', 'Worst Net']]
    
    # Replace with correct history for specific TEG 5
    results_with_year.loc[results_with_year['TEG'] == 'TEG 5', 'Best Net'] = 'Gregg WILLIAMS'
    results_with_year.loc[results_with_year['TEG'] == 'TEG 5', 'Best Gross'] = 'Stuart NEUMANN*'
    
    return results_with_year

# Streamlit app starts here
st.title('TEG History')

# Assuming df is your DataFrame 'all_data' that you have
# You can load or prepare 'all_data' outside this snippet

# Display the summary table
teg_summary = get_teg_summary(all_data)

teg_summary.rename(columns={
    'Best Net': 'TEG Trophy',
    'Best Gross': 'Green Jacket',
    'Worst Net': 'HMM Wooden Spoon'
}, inplace=True)

#st.dataframe(teg_summary, hide_index=True)  # This will display the DataFrame in a scrollable table

st.write(teg_summary.to_html(index=False, justify='left'), unsafe_allow_html=True)

st.caption('*Green Jacket awarded in TEG 5 for best stableford round; DM had best gross score')
# teg_summary = teg_summary.reset_index(drop=True)
# st.table(teg_summary)  # This will display the DataFrame in a scrollable table

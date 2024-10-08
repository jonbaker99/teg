import pandas as pd

# Load the data from the CSV file
df = pd.read_csv(r'data/teg10-14-data.csv')
#print(df)

# Reshape the data from wide to long format
# We'll use pd.melt to unpivot the player columns
melted_df = pd.melt(df, 
                    id_vars=['TEG', 'Round', 'Hole', 'PAR', 'SI'],  # These columns remain fixed
                    value_vars=['DM', 'GW', 'JB', 'SN', 'AB', 'JP'],  # These columns will be unpivoted
                    var_name='Pl',   # This is the new column that will contain the player names (the original column headers)
                    value_name='Sc') # This is the new column that will contain the scores (the values from the original columns)

# Save the reshaped data to a new CSV file
melted_df.to_csv(r'data/teg-10-14-data-long.csv', index=False)

# Display the reshaped dataframe
print(melted_df)

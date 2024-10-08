import pandas as pd

def add_full_player_names(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Check if 'Player' field already exists
    if 'Player' not in df.columns:
        # Define the mapping of initials to full names
        player_mapping = {
            'JB': 'Jon BAKER',
            'AB': 'Alex BAKER',
            'GW': 'Gregg WILLIAMS',
            'DM': 'David MULLIN',
            'SN': 'Stuart NEUMANN',
            'JP': 'John PATTERSON',
            'HM': 'Henry MELLER'
        }
        
        # Add the 'Player' field based on the 'Pl' field
        df['Player'] = df['Pl'].map(player_mapping)
        
        # Save the updated DataFrame back to CSV
        df.to_csv(file_path, index=False)
        print(f"Added 'Player' field to {file_path}")
    else:
        print(f"'Player' field already exists in {file_path}")
    
    return df

# Usage
file_path = 'data/teg-all-data-long.csv'
updated_df = add_full_player_names(file_path)
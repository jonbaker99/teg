import pandas as pd
import numpy as np

# Data for the player scores table
player_scores = pd.DataFrame({
    'Player': ['David MULLIN', 'Jon BAKER', 'Stuart NEUMANN', 'Gregg WILLIAMS', 'Henry MELLER'],
    'R1': [36, 33, 27, 28, 18],
    'R2': [29, 37, 29, 27, 23],
    'R3': [38, 28, 33, 31, 34]
})
player_scores['Total'] = player_scores['R1'] + player_scores['R2'] + player_scores['R3']

# Data for the Stableford race line chart
np.random.seed(42)  # for reproducibility
holes = range(1, 73)
players = ['AB', 'GW', 'DM', 'JB', 'SN', 'HM', 'JP']
stableford_data = pd.DataFrame(index=holes)

for player in players:
    cumulative_scores = np.cumsum(np.random.randint(-2, 4, size=72))
    stableford_data[player] = cumulative_scores

# Adjust some values to match the image more closely
stableford_data['AB'] += 40
stableford_data['GW'] += 25
stableford_data['DM'] += 15
stableford_data['JB'] += 10
stableford_data['SN'] -= 5
stableford_data['JP'] -= 35

# Data for the average score by par bar chart
avg_score_by_par = pd.DataFrame({
    'Player': ['DM', 'JB', 'GW', 'HM', 'JP', 'SN', 'AB'],
    'Par 3': [0.9, 1.0, 1.2, 1.2, 1.2, 1.2, 1.3],
    'Par 4': [1.2, 1.5, 1.5, 1.5, 1.6, 1.6, 1.9],
    'Par 5': [0.8, 1.4, 1.5, 1.6, 1.6, 1.6, 1.7]
})

# Display the first few rows of each dataset
print("Player Scores Table:")
print(player_scores)
print("\nStableford Race Data (first 5 rows):")
print(stableford_data.head())
print("\nAverage Score by Par:")
print(avg_score_by_par)

if __name__ == "__main__":
    print("Data generated successfully.")
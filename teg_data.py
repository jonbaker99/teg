import pandas as pd

df = pd.read_csv(r'data/all-data.csv')
#print(df)

# # List the column names
# columns = df.columns

# # Convert to a list if needed
# columns_list = list(columns)
# print("\nColumn Names as a List:")
# print(columns_list)


# ADD CUMULATIVE SCORES
# NB ONLY NEEDS TO BE DONE ONCE WHEN DATA IS UPDATED (ASSUMING NEW DATA SET THEN GETS SAVED SOMEWHERE)

df = df.sort_values(by=['Pl','TEGNum', 'Round', 'Hole'])



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

round_count = df['Hole']
df['TEG Count'] = teg_count = df.groupby(group_teg).cumcount() + 1
df['Career Count'] = career_count = df.groupby(group_career).cumcount() + 1

for measure in measures:
    df[f'{measure} Round Avg'] = df[f'{measure} Cum Round'] / round_count # ROUND
    df[f'{measure} TEG Avg'] = df[f'{measure} Cum TEG'] / teg_count # TEG
    df[f'{measure} Career Avg'] = df[f'{measure} Cum Career'] / career_count # CAREER


# Display the result
#print(df)
#df.to_clipboard(index=False)
print('cumulative data added')



# TEG_LEVEL DATA

#teg_df = df.groupby(['Pl', 'TEG', 'TEGNum'], as_index=False)[['Sc', 'Stableford', 'GrossVP', 'NetVP']].sum().sort_values(by=['Pl','TEGNum'])  #original approach


measures = ['Sc', 'GrossVP', 'NetVP', 'Stableford']
group_teg = ['Pl', 'TEGNum', 'TEG']
teg_df = df.groupby(group_teg, as_index=False)[measures].sum().sort_values(by=['Pl','TEGNum'])
#teg_df.to_clipboard(index=False)
print('teg level data created')

# ROUND LEVEL DATA
group_rd = ['Pl', 'TEGNum', 'Round']
round_df = df.groupby(group_rd, as_index=False)[measures].sum().sort_values(by=['Pl','TEGNum','Round'])
#round_df.to_clipboard(index=False)
print('round data created')



# LEADERBOARD (STABLEFORD)

chosen_teg = 'TEG 16'

leaderboard_df = round_df[round_df['TEG'] == chosen_teg]
leaderboard_pivot = leaderboard_df.pivot_table(index='Pl', columns='Round', values='Stableford', aggfunc='sum', fill_value=0)
# print(leaderboard_pivot)
# print()
leaderboard_pivot['Total'] = leaderboard_pivot.sum(axis=1)
leaderboard_pivot = leaderboard_pivot.sort_values(by='Total', ascending=False).reset_index()
leaderboard_pivot['Rank'] = leaderboard_pivot['Total'].rank(method='min', ascending=False).astype(int).astype(str)
duplicated_scores = leaderboard_pivot['Total'].duplicated(keep=False)
leaderboard_pivot.loc[duplicated_scores, 'Rank'] = leaderboard_pivot['Rank'].astype(str) + '='
trophy_champ = leaderboard_pivot[leaderboard_pivot['Rank'].isin(['1', '1='])]['Pl'].tolist()
# print(leaderboard_pivot)
# print()

leaderboard_pivot = leaderboard_pivot[['Rank'] + [col for col in leaderboard_pivot.columns if col != 'Rank']]

print(f'\nTROPHY TABLE | {chosen_teg}\n=================')
print(leaderboard_pivot.to_string(index=False))
print(trophy_champ)
leaderboard_pivot.to_clipboard(index=False)

# LEADERBOARD (JACKET)

jacketboard_pivot = leaderboard_df.pivot_table(index='Pl', columns='Round', values='GrossVP', aggfunc='sum', fill_value=0)
# print(leaderboard_pivot)
# print()
jacketboard_pivot['Total'] = jacketboard_pivot.sum(axis=1)
jacketboard_pivot = jacketboard_pivot.sort_values(by='Total', ascending=True).reset_index()
jacketboard_pivot['Rank'] = jacketboard_pivot['Total'].rank(method='min', ascending=True).astype(int).astype(str)
duplicated_scores = jacketboard_pivot['Total'].duplicated(keep=False)
jacketboard_pivot.loc[duplicated_scores, 'Rank'] = jacketboard_pivot['Rank'].astype(str) + '='
# print(leaderboard_pivot)
# print()

jacketboard_pivot = jacketboard_pivot[['Rank'] + [col for col in jacketboard_pivot.columns if col != 'Rank']]

print(f'\nJACKET TABLE | {chosen_teg}\n=================')
print(jacketboard_pivot.to_string(index=False))

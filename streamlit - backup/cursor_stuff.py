import pandas as pd
import altair as alt
from utils import load_all_data, aggregate_data, get_teg_rounds

all_data = load_all_data()


#create a dataframe with the unique tegs and the number of unique rounds for each teg
teg_rounds = all_data.groupby('TEG')['Round'].nunique().reset_index()
# add a column called 'Rounds_in_TEG' to teg_rounds with the value of get_teg_rounds for each teg
teg_rounds['Rounds_in_TEG'] = teg_rounds['TEG'].apply(get_teg_rounds)
#print(teg_rounds)

#identify the TEGs in teg_rounds where Rounds_in_TEG is not equal to Round
incomplete_tegs = teg_rounds[teg_rounds['Rounds_in_TEG'] != teg_rounds['Round']]
print(incomplete_tegs)

# remove the incomplete TEGs from all_data
all_data = all_data[~all_data['TEG'].isin(incomplete_tegs['TEG'])]

# print the unique values of TEGNum in all_data in ascending order
print(sorted(all_data['TEGNum'].unique()))

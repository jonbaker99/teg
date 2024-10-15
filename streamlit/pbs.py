import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import altair as alt
from utils import load_all_data, get_teg_rounds

all_data = load_all_data()

# filter out TEG == TEG 50
#all_data = all_data[all_data['TEG'] != 'TEG 50']

#call get_teg_rounds() for each TEG in all_data
#create df with TEG and ROUNDS
teg_rounds = pd.DataFrame({'TEG': list(all_data['TEG'].unique()), 'ROUNDS': [get_teg_rounds(teg) for teg in all_data['TEG'].unique()]})
# print('\nTEG ROUNDS:')
# print(teg_rounds)

# get teg rounds for each TEG in all_data
teg_rounds_in_data = all_data.groupby('TEG')['Round'].nunique().reset_index()
# print('\nTEG ROUNDS IN DATA:')
# print(teg_rounds_in_data)

#exclude TEGS where ROUNDS in teg_rounds_in_data != ROUNDS in teg_rounds
all_data = all_data[~all_data['TEG'].isin(teg_rounds_in_data[teg_rounds_in_data['Round'] != teg_rounds['ROUNDS']]['TEG'])]

# print unique TEGs in all_data
# print('\nUNIQUE TEGS IN DATA:')
# print(all_data['TEG'].unique())

#=====CREATING PERSONAL BESTS========


# Aggregate Sc, GrossVP, NetVP and Stableford by TEG and Player
teg_data = all_data.groupby(['TEG', 'Player'])[['Sc', 'GrossVP', 'NetVP', 'Stableford']].sum().reset_index()

# print('\nTEG DATA:')
# print(teg_data)

# identify lowest Sc, GrossVP, NetVP and highest Stableford for each Player from teg_data 
personal_bests = teg_data.groupby('Player').agg({
    'Sc': 'min',
    'GrossVP': 'min',
    'NetVP': 'min',
    'Stableford': 'max'
}).reset_index()
print('\nPERSONAL BESTS:')
print(personal_bests)

# convert personal_bests to long format
#personal_bests_long = pd.melt(personal_bests, id_vars=['Player'], value_vars=['Best_Sc', 'Best_GrossVP', 'Best_NetVP', 'Best_Stableford'], var_name='Stat', value_name='Value')

# ======= TRY AN ALTERNATIVE APPROACH =======   

# filter teg_data for the lowest Sc, GrossVP, NetVP and highest Stableford for each Player
lowest_sc = teg_data[teg_data.groupby('Player')['Sc'].idxmin()]
#highest_stableford = teg_data[teg_data.groupby('Player')['Stableford'].idxmax()]

print('\nLOWEST SC:') 
print(lowest_sc)

# print('\nHIGHEST STABLEFORD:')
# print(highest_stableford)

# print('\nPERSONAL BESTS LONG:')
# print(personal_bests_long)


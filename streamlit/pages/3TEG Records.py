from utils import get_ranked_teg_data, get_best, get_ranked_round_data
import streamlit as st
import pandas as pd

st.set_page_config(page_title="TEG Records", page_icon="⛳")
st.title("TEG Records")


def format_best_teg_record(ranked_teg_df, measure):
    # Get the best record(s)
    best_records = get_best(ranked_teg_df, measure_to_use=measure, top_n=1)
    
    # Format the header based on the measure
    if measure == 'Sc':
        header = f"Best Score: {int(best_records[measure].iloc[0])}"
    elif measure == 'GrossVP':
        header = f"Best Gross: {int(best_records[measure].iloc[0]):+}"
    elif measure == 'NetVP':
        header = f"Best Net: {int(best_records[measure].iloc[0]):+}"
    elif measure == 'Stableford':
        header = f"Best Stableford: {int(best_records[measure].iloc[0])}"
    
    # Format player info
    if len(best_records) == 1:
        player_info = f"| **{best_records['Player'].iloc[0]}** | {best_records['TEG'].iloc[0]} ({best_records['Year'].iloc[0]})"
        return f"{header} {player_info}"
    else:
        player_infos = [f"* **{row['Player']}** | {row['TEG']} ({row['Year']})" for _, row in best_records.iterrows()]
        return f"{header}\n" + "\n".join(player_infos)
    
def format_best_round_record(ranked_round_df, measure):
    # Get the best record(s)
    best_records = get_best(ranked_round_df, measure_to_use=measure, top_n=1)
    
    # Format the header based on the measure
    if measure == 'Sc':
        header = f"Best Score: {int(best_records[measure].iloc[0])}"
    elif measure == 'GrossVP':
        header = f"Best Gross: {int(best_records[measure].iloc[0]):+}"
    elif measure == 'NetVP':
        header = f"Best Net: {int(best_records[measure].iloc[0]):+}"
    elif measure == 'Stableford':
        header = f"Best Stableford: {int(best_records[measure].iloc[0])}"
    
    # Format player info
    if len(best_records) == 1:
        player_info = f"| **{best_records['Player'].iloc[0]}** | {best_records['Course'].iloc[0]} | {best_records['TEG'].iloc[0]}, R{best_records['Round'].iloc[0]} | {best_records['Date'].iloc[0]}"
        return f"{header} {player_info}"
    else:
        player_infos = [f"* **{row['Player']}** | {row['Course']} | {row['TEG']}, {row['Round']} | ({row['Date']})" for _, row in best_records.iterrows()]
        return f"{header}\n" + "\n".join(player_infos)


measures = ['GrossVP', 'NetVP', 'Stableford']
tegs_ranked = get_ranked_teg_data()
rounds_ranked = get_ranked_round_data()

# col1, col2, = st.columns(2)
'---'

# with col1:
st.subheader('Best TEGs')
for measure in measures:
    st.markdown(format_best_teg_record(tegs_ranked, measure))

'---'

# with col2:
st.subheader('Best Rounds')
for measure in measures:
    st.markdown(format_best_round_record(rounds_ranked, measure))

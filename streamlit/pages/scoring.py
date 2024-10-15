from utils import score_type_stats, load_all_data, apply_score_types, max_scoretype_per_round
import streamlit as st
import pandas as pd, altair as alt
import numpy as np

st.set_page_config(page_title="TEG Scoring")
st.title("Scoring")

'---'
st.subheader("Career Eagles, Birdies, Pars and TBPs")

# Calculate the stats
scoring_stats = score_type_stats()
# st.write("Columns in the DataFrame:", scoring_stats.columns)

fields = ['Eagles', 'Holes_per_Eagle']

def make_scoring_chart_progress_column(df, fields):
    df = scoring_stats[['Player'] + fields].sort_values(by=fields, ascending=[False, True])
    df_native = df.astype(object)

    # Handle potential infinity values
    max_values = []
    for field in fields:
        max_val = df[field].replace([np.inf, -np.inf], np.nan).max()
        if np.isnan(max_val):
            max_val = 1  # or any other appropriate default value
        max_values.append(int(max_val))

    output_df = st.dataframe(
        df_native,
        column_config={
            fields[0]: st.column_config.ProgressColumn(
                fields[0].replace("_", " "),
                help="Number of " + fields[0].replace("_", " "),
                format="%f",
                min_value=0,
                max_value=max_values[0]*1.1
            ),
            fields[1]: st.column_config.ProgressColumn(
                fields[1].replace("_", " "),
                help=fields[1].replace("_", " "),
                format="%.1f",
                min_value=0,
                max_value=max_values[1]*1.1
            ),
        },
        hide_index=True,
        use_container_width=True,
    )

    return output_df

chart_fields_all = [
    ['Eagles', 'Holes_per_Eagle'],
    ['Birdies', 'Holes_per_Birdie'],
    ['Pars_or_Better', 'Holes_per_Par_or_Better'],
    ['TBPs', 'Holes_per_TBP']
]

cnt_fields = len(chart_fields_all)

for i in range(cnt_fields):
    chart_fields = chart_fields_all[i]
    section_title = chart_fields[0].replace("_", " ")
    st.markdown(f"**Career {section_title}**")
    #st.caption(f'Number & frequency of career {section_title}')
    make_scoring_chart_progress_column(scoring_stats, chart_fields)

'---'

st.subheader('Most of each type of score in a single round')
max_by_round = max_scoretype_per_round()
st.write(max_by_round.to_html(index=False, justify='left'), unsafe_allow_html=True)
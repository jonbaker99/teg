from utils import score_type_stats, load_all_data, apply_score_types
import streamlit as st
import pandas as pd, altair as alt
import numpy as np

# Calculate the stats
scoring_stats = score_type_stats()
# st.write("Columns in the DataFrame:", scoring_stats.columns)



st.subheader('Numbers & frequency of score types')

# Display the dataframe in Streamlit
# st.dataframe(scoring_stats)

# def make_score_chart(score_df,field='Birdies', sort_desc = True):
#     df = score_df[['Player',field]]
#     chart = alt.Chart(df).mark_bar().encode(
#     x=alt.X('Player', sort='-y' if sort_desc else 'y'),  # Sort x-axis based on y values
#     y=field)
#     return chart

# '---'



# def make_horizontal_bar_chart(df, field, sort_desc=True, format_decimal=False):
#     # Define the formatting for the text
#     text_format = '.1f' if format_decimal else 'd'

#     # Handle potential Infinity values
#     df[field] = df[field].replace([np.inf, -np.inf], np.nan)
    
#     # Calculate the maximum value for the x-axis, excluding NaN
#     max_value = df[field].max()
    
#     # If max_value is NaN (all values were Infinity), set a default
#     if np.isnan(max_value):
#         max_value = 1  # or any other appropriate default value

#     base = alt.Chart(df).encode(
#         y=alt.Y('Player:N', 
#                 sort='-x' if sort_desc else 'x', 
#                 axis=alt.Axis(title=None, labelLimit=200)),
#         x=alt.X(f'{field}:Q', 
#                 axis=alt.Axis(title=None, labels=False),
#                 scale=alt.Scale(domain=[0, max_value]))
#     ).properties(
#         #title=field,
#         height=len(df) * 45,
#         #width=400
#     )

#     bars = base.mark_bar()

#     text = base.mark_text(
#         align='right',
#         baseline='middle',
#         dx=-5,
#         color='white'
#     ).encode(
#         text=alt.Text(f'{field}:Q', format=text_format)
#     )
    
#     chart = (bars + text).configure_view(strokeWidth=0).configure_axis(
#         grid=False,
#         labelColor='black',
#         labelFontSize=14
#     )

#     return chart


# # Create two columns
# col1, col2 = st.columns(2)

# fields = ['Eagles', 'Birdies', 'Pars_or_Better', 'TBPs'] 

# with col1:
#     for i, field in enumerate(fields):
#         # Add title and horizontal line
#         st.markdown(f"**{field}**")
#         st.markdown("<hr style='height:2px;border-width:0;color:gray;background-color:gray;margin-top:-15px;margin-bottom:10px'>", unsafe_allow_html=True)
        
#         # Create and display the chart
#         chart = make_horizontal_bar_chart(scoring_stats, field, sort_desc=True, format_decimal=False)
#         st.altair_chart(chart, use_container_width=True)

# fields = ['Holes_per_Eagle', 'Holes_per_Birdie', 'Holes_per_Par_or_Better', 'Holes_per_TBP']
# with col2:
#     for i, field in enumerate(fields):
#         # Add title and horizontal line
#         st.markdown(f"**{field}**")
#         st.markdown("<hr style='height:2px;border-width:0;color:gray;background-color:gray;margin-top:-15px;margin-bottom:10px'>", unsafe_allow_html=True)
        
#         # Create and display the chart
#         chart = make_horizontal_bar_chart(scoring_stats, field, sort_desc=False, format_decimal=True)
#         st.altair_chart(chart, use_container_width=True)

'---'

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


from streamlit_extras.colored_header import colored_header


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
    st.markdown(f"**{section_title}**")
    st.caption(f'Number & frequency of career {section_title}')
    #colored_header(section_title,f'Number & frequency of career {section_title}',"red-70")
    make_scoring_chart_progress_column(scoring_stats, chart_fields)

# items_in_cols = 4

# from math import ceil
# num_cols = ceil(cnt_fields / items_in_cols)

# cols = st.columns(num_cols)


# for i in range(cnt_fields):
#     col_index = i // items_in_cols
#     with cols[col_index]:
#         chart_fields = chart_fields_all[i]
#         st.markdown(f"**{chart_fields[0]}**")
#         make_scoring_chart_progress_column(scoring_stats, chart_fields)



'---'

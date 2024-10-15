from utils import score_type_stats, load_all_data, apply_score_types
import streamlit as st
import pandas as pd, altair as alt

# Calculate the stats
scoring_stats = score_type_stats()
st.write("Columns in the DataFrame:", scoring_stats.columns)



st.subheader('Numbers & frequency of score types')

# Display the dataframe in Streamlit
st.dataframe(scoring_stats)

def make_score_chart(score_df,field='Birdies', sort_desc = True):
    df = score_df[['Player',field]]
    chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Player', sort='-y' if sort_desc else 'y'),  # Sort x-axis based on y values
    y=field)
    return chart

# st.altair_chart(make_score_chart(scoring_stats,'Eagles'), use_container_width=True)
# st.altair_chart(make_score_chart(scoring_stats,'Birdies'), use_container_width=True)
# st.altair_chart(make_score_chart(scoring_stats,'Pars_or_Better'), use_container_width=True)
# st.altair_chart(make_score_chart(scoring_stats,'TBPs'), use_container_width=True)

# st.write('TWO COLUMNS x TWO ROWS')


# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Eagles")
#     chart = make_score_chart(scoring_stats, 'Eagles')
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

#     st.subheader("Birdies")
#     chart = make_score_chart(scoring_stats, 'Birdies')
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

#     st.subheader("Pars or Better")
#     chart = make_score_chart(scoring_stats, 'Pars_or_Better')
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

#     st.subheader("TBPs")
#     chart = make_score_chart(scoring_stats, 'TBPs')
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

# with col2:

#     st.subheader("Holes_per_Eagle")
#     chart = make_score_chart(scoring_stats, 'Holes_per_Eagle',sort_desc=False)
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

#     st.subheader("Holes_per_Birdie")
#     chart = make_score_chart(scoring_stats, 'Holes_per_Birdie',sort_desc=False)
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

#     st.subheader("Holes_per_Par_or_Better")
#     chart = make_score_chart(scoring_stats, 'Holes_per_Par_or_Better',sort_desc=False)
#     if chart:
#         st.altair_chart(chart, use_container_width=True)

#     st.subheader("Holes_per_TBP")
#     chart = make_score_chart(scoring_stats, 'Holes_per_TBP',sort_desc=False)
#     if chart:
#         st.altair_chart(chart, use_container_width=True)



'---'

def make_horizontal_bar_chart(df, field, sort_desc=True, format_decimal=False):

    # Define the formatting for the text
    if format_decimal:
        text_format = '.1f'
    else:
        text_format = 'd'


    base = alt.Chart(df).encode(
        y=alt.Y('Player:N', sort='-x' if sort_desc else 'x', axis=alt.Axis(title=None)),
        x=alt.X(f'{field}:Q', axis=alt.Axis(title=field))
    ).properties(
        title=field,
        height=len(df) * 50  # Adjust this multiplier to change bar height
    )

    #bars = base.mark_bar(color='#5bc0de')
    bars = base.mark_bar()

    text = base.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Slight offset to position text to the right of the bar
    ).encode(
        text=alt.Text(f'{field}:Q', format=text_format)
    )
    
    return (bars + text).configure_view(strokeWidth=0).configure_axis(grid=False)

# Create two columns
col1, col2 = st.columns(2)

# Fields to display
#fields = ['Eagles', 'Birdies', 'Pars_or_Better', 'TBPs', 'Holes_per_Eagle', 'Holes_per_Birdie', 'Holes_per_Par_or_Better','Holes_per_TBP']
# # Create charts in columns
# for i, field in enumerate(fields):
#     with col1 if i < 4 else col2:
#         chart = make_horizontal_bar_chart(scoring_stats, field)
#         st.altair_chart(chart, use_container_width=True)

fields = ['Eagles', 'Birdies', 'Pars_or_Better', 'TBPs'] 

with col1:
    for i, field in enumerate(fields):
        chart = make_horizontal_bar_chart(scoring_stats, field,sort_desc=True,format_decimal=False)
        st.altair_chart(chart, use_container_width=True)


fields = ['Holes_per_Eagle', 'Holes_per_Birdie', 'Holes_per_Par_or_Better','Holes_per_TBP']
with col2:
    for i, field in enumerate(fields):
        chart = make_horizontal_bar_chart(scoring_stats, field,sort_desc=False,format_decimal=True)
        st.altair_chart(chart, use_container_width=True)


'---'

import streamlit as st
import altair as alt
import pandas as pd

def reshape_data(df):
    selected_columns = ['Player', 'Eagles', 'Birdies', 'Pars_or_Better', 'TBPs']
    df_selected = df[selected_columns]
    return df_selected.melt(id_vars=['Player'], var_name='Measure', value_name='Value')

def create_faceted_chart(df):
    data = reshape_data(df)
    
    color_scale = alt.Scale(domain=['Eagles', 'Birdies', 'Pars_or_Better', 'TBPs'],
                            range=['#8B0000', '#FF0000', '#ADD8E6', '#000000'])
    
    chart_height = len(df.Player.unique()) * 25

    base = alt.Chart(data).encode(
        y=alt.Y('Player:N', sort=alt.EncodingSortField(field='Value', op='sum', order='descending'), title=None),
        x=alt.X('Value:Q', axis=None),
        color=alt.Color('Measure:N', scale=color_scale, legend=None)
    ).properties(
        width=150,
        height=chart_height
    )

    bars = base.mark_bar()

    # Adjust text color based on measure for visibility
    text_color = alt.condition(
        alt.datum.Measure == 'Pars_or_Better',
        alt.value('black'),  # Use black text for light blue bars
        alt.value('white')   # Use white text for other bars
    )

    text = base.mark_text(
        align='left',   # Align to the left edge of the bar
        baseline='middle',
        dx=-15,           # Small offset from the left edge
    ).encode(
        text=alt.Text('Value:Q', format='d'),
        color=text_color
    )

    final_chart = (bars + text).facet(
        column=alt.Column('Measure:N', title=None, sort=['Eagles', 'Birdies', 'Pars_or_Better', 'TBPs']),
        spacing=5
    ).resolve_scale(
        x='independent'
    ).properties(
        title='Golf Statistics by Player'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False
    )

    return final_chart

# Create and display the chart
try:
    chart = create_faceted_chart(scoring_stats)
    st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.write("Debug info:")
    st.write(f"DataFrame shape: {scoring_stats.shape}")
    st.write(f"DataFrame columns: {scoring_stats.columns}")
    st.write(scoring_stats.head())

'---'

import streamlit as st
import pandas as pd
import altair as alt

# Assuming your DataFrame is already loaded and named 'scoring_stats'
# If not, you would load it here, e.g.:
# scoring_stats = pd.read_csv('your_data_file.csv')

st.title('Golf Statistics Visualization')

# Function to create a faceted chart for a given measure
def create_faceted_chart(df, measure, count_col, rate_col):
    base = alt.Chart(df).encode(
        y=alt.Y('Player:N', 
                sort=alt.SortField(field=count_col, order='descending'),
                title=None,
                axis=alt.Axis(labelFontSize=14, labelColor='black', labelLimit=200))
    ).properties(
        height=alt.Step(40),  # Reduced from 30 to make bars less wide
        width=alt.Step(5)  # This sets a maximum width for each bar
    )

    bar1 = base.mark_bar().encode(
        x=alt.X(f'{count_col}:Q', title='', axis=alt.Axis(labels=False, ticks=False, domain=False)),
        color=alt.value('steelblue')
    )

    bar2 = base.mark_bar().encode(
        x=alt.X(f'{rate_col}:Q', title='', axis=alt.Axis(labels=False, ticks=False, domain=False)),
        color=alt.value('orange'),
        y=alt.Y('Player:N', sort=alt.SortField(field=count_col, order='descending'), axis=None)
    )

    text1 = bar1.mark_text(align='left', dx=3).encode(
        text=f'{count_col}:Q'
    )

    text2 = bar2.mark_text(align='left', dx=3).encode(
        text=f'{rate_col}:Q'
    )

    chart1 = (bar1 + text1).properties(title=f'{measure} Count')
    chart2 = (bar2 + text2).properties(title=f'Holes per {measure}')

    chart = alt.hconcat(chart1, chart2).resolve_scale(
        x='independent'
    ).properties(
        title=f'{measure} Statistics'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False
    ).configure_concat(
        spacing=20  # Add some space between the two charts
    )

    return chart

# Create charts for each measure
measures = [
    ('Eagle', 'Eagles', 'Holes_per_Eagle'),
    ('Birdie', 'Birdies', 'Holes_per_Birdie'),
    ('Par or Better', 'Pars_or_Better', 'Holes_per_Par_or_Better'),
    ('TBP', 'TBPs', 'Holes_per_TBP')
]

for measure, count_col, rate_col in measures:
    st.subheader(f'{measure} Statistics')
    chart = create_faceted_chart(scoring_stats, measure, count_col, rate_col)
    st.altair_chart(chart, use_container_width=True)

# Add some explanatory text
st.markdown("""
This visualization shows golf statistics for various players:
- The blue bars represent the count of each statistic (Eagles, Birdies, Pars or Better, TBPs).
- The orange bars represent the number of holes per occurrence of each statistic.
- Players are sorted by the count of each statistic in descending order.
""")
'---'


st.markdown("""
# To do
- Bar charts - number of each thing
- Bar charts - holes per
- Stacked bar score mix
- Most in a round
""")
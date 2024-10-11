import streamlit as st
import pandas as pd
import altair as alt
from utils import load_all_data, get_teg_winners

# === LOAD DATA & INITIAL PROCESSING === #

# Load the data
all_data = load_all_data()

# Filter out TEGNum 50 and remove the 'Year' column
all_data = all_data[all_data['TEGNum'] != 50]
winners = get_teg_winners(all_data).drop(columns=['Year'])

# Remove asterisks from player names
winner_df = winners.replace(r'\*', '', regex=True)

# Melt the DataFrame to have players and competitions in long format
melted_winners = pd.melt(winner_df, id_vars=['TEG'], value_vars=['TEG Trophy', 'Green Jacket', 'HMM Wooden Spoon'],
                         var_name='Competition', value_name='Player')

# Group by player and competition, then count the occurrences
player_wins = melted_winners.groupby(['Player', 'Competition']).size().unstack(fill_value=0).sort_values(by='TEG Trophy', ascending=False)

# Reorder and rename the columns
player_wins = player_wins[['TEG Trophy', 'Green Jacket', 'HMM Wooden Spoon']]
player_wins.columns = ['Trophy', 'Jacket', 'Spoon']

# === DISPLAY TABLE === #
st.title("Player Wins Summary")

# Reset index and display the table
player_wins = player_wins.reset_index().rename(columns={'index': 'Player'})
st.write(player_wins.to_html(index=False, justify='left'), unsafe_allow_html=True)

# === CALCULATE NUMBER OF DOUBLES === #

# Find players who won both the Trophy and Jacket in the same TEG
same_player_both = winner_df[winner_df['TEG Trophy'] == winner_df['Green Jacket']]

# Count the number of "doubles" for each player
player_doubles = same_player_both['TEG Trophy'].value_counts().reset_index()
player_doubles.columns = ['Player', 'Doubles']
player_doubles = player_doubles.sort_values(by='Doubles', ascending=False)

# Display the number of times players have won both the Trophy and Jacket
st.write(f"Number of times a player has won both the Trophy and Jacket in a single TEG: {same_player_both.shape[0]}")

# Display the doubles table
st.write(player_doubles.to_html(index=False, justify='left'), unsafe_allow_html=True)

# === CREATE CHARTS === #

# Sort the data for each competition
trophy_sorted = player_wins.sort_values(by='Trophy', ascending=False).reset_index()
jacket_sorted = player_wins.sort_values(by='Jacket', ascending=False).reset_index()
spoon_sorted = player_wins.sort_values(by='Spoon', ascending=False).reset_index()

# Extract the player order from the horizontal bar charts for use in vertical charts
player_order_trophy = trophy_sorted['Player'].tolist()
player_order_jacket = jacket_sorted['Player'].tolist()
player_order_spoon = spoon_sorted['Player'].tolist()

# Find the maximum number of wins across all competitions to set the x-axis range
max_wins = max(trophy_sorted['Trophy'].max(), jacket_sorted['Jacket'].max(), spoon_sorted['Spoon'].max())

# === HORIZONTAL BAR CHARTS === #

# Function to create a customized Altair horizontal bar chart
def create_bar_chart(df, x_col, y_col, title):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_col, title=None, axis=alt.Axis(grid=False, labels=False, domain=False), scale=alt.Scale(domain=(0, max_wins))),
        y=alt.Y(y_col, sort='-x', title=None),
        color=alt.value('steelblue')
    ).properties(
        title=title,
        width=350,
        height=300
    )
    
    # Add text labels
    text = chart.mark_text(align='left', baseline='middle', dx=3).encode(text=x_col)
    
    return chart + text

# === VERTICAL COLUMN CHARTS === #

# Function to create a customized Altair vertical bar chart with explicit sorting
def create_vertical_bar_chart(df, y_col, x_col, title, player_order):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(x_col, title=None, axis=alt.Axis(grid=False, labels=True, domain=False), sort=player_order),  # Sort by player order
        y=alt.Y(y_col, title=None, axis=alt.Axis(grid=False, labels=False)),  # Remove y-axis labels and grid
        color=alt.value('steelblue')
    ).properties(
        title=title,
        width=250,
        height=300
    )
    
    # Add text labels on top of bars
    text = chart.mark_text(align='center', baseline='bottom', dy=-3).encode(text=y_col)
    
    return chart + text

# === DISPLAY HORIZONTAL BAR CHARTS === #
st.subheader("Player Wins Bar Charts")

# 3-Column layout for Trophy, Jacket, Spoon (Horizontal Bars)
col1, col2, col3 = st.columns(3)

with col1:
    trophy_chart = create_bar_chart(trophy_sorted, 'Trophy', 'Player', 'TEG Trophy Wins')
    st.altair_chart(trophy_chart, use_container_width=True)

with col2:
    jacket_chart = create_bar_chart(jacket_sorted, 'Jacket', 'Player', 'Green Jacket Wins')
    st.altair_chart(jacket_chart, use_container_width=True)

with col3:
    spoon_chart = create_bar_chart(spoon_sorted, 'Spoon', 'Player', 'Wooden Spoon Wins')
    st.altair_chart(spoon_chart, use_container_width=True)

# === DISPLAY VERTICAL COLUMN CHARTS (SORTED BY WINS DESCENDING) === #
st.subheader("Player Wins Vertical Column Charts")

col1, col2, col3 = st.columns(3)

with col1:
    trophy_column_chart = create_vertical_bar_chart(trophy_sorted, 'Trophy', 'Player', 'TEG Trophy Wins', player_order_trophy)
    st.altair_chart(trophy_column_chart, use_container_width=True)

with col2:
    jacket_column_chart = create_vertical_bar_chart(jacket_sorted, 'Jacket', 'Player', 'Green Jacket Wins', player_order_jacket)
    st.altair_chart(jacket_column_chart, use_container_width=True)

with col3:
    spoon_column_chart = create_vertical_bar_chart(spoon_sorted, 'Spoon', 'Player', 'Wooden Spoon Wins', player_order_spoon)
    st.altair_chart(spoon_column_chart, use_container_width=True)

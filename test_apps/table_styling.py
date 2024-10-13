import streamlit as st
import pandas as pd

# Sample DataFrame
data = {
    'Player': ['Alice', 'Bob', 'Charlie'],
    'Score': [85, 92, 88],
    'Rank': [1, 2, 3]
}

df = pd.DataFrame(data)

# Table 1: Grey background with Roboto or Arial font
styled_df_1 = (df.style
               .set_properties(**{'background-color': 'lightgrey', 'color': 'black', 'font-family': 'Roboto, Arial, sans-serif'})
               .set_table_styles([{
                   'selector': 'thead th',
                   'props': [('background-color', 'darkgrey'), ('color', 'white')]
               }]))

# Table 2: Pale yellow (FT) background with serif font
styled_df_2 = (df.style
               .set_properties(**{'background-color': '#FFF2CC', 'color': 'black', 'font-family': 'Georgia, serif'})
               .set_table_styles([{
                   'selector': 'thead th',
                   'props': [('background-color', '#F5C000'), ('color', 'black')]
               }]))

# Streamlit Page Layout
st.title("Styled Tables Example")

st.subheader("Table 1: Grey Background with Roboto/Arial Font")
st.write(styled_df_1.to_html(), unsafe_allow_html=True)

st.subheader("Table 2: Pale Yellow (FT) Background with Serif Font")
st.write(styled_df_2.to_html(), unsafe_allow_html=True)

'---'

import streamlit as st
import pandas as pd

# Sample DataFrame with Rank column
data = {
    'Rank': [1, 2, 3, 4, 5],
    'Player': ['David MULLIN', 'Jon BAKER', 'Stuart NEUMANN', 'Henry MELLER', 'Gregg WILLIAMS'],
    'R1': ['+17', '+18', '+26', '+29', '+20'],
    'R2': ['+17', '+21', '+21', '+17', '+32'],
    'R3': ['+29', '+23', '+22', '+37', '+35'],
    'R4': ['+22', '+27', '+28', '+35', '+41'],
    'Total': ['+85', '+89', '+97', '+118', '+128']
}

df = pd.DataFrame(data)

# Define a function to apply grey background for the row where Rank == 1
def highlight_rank(row):
    return ['background-color: lightgrey' if row['Rank'] == 1 else '' for _ in row]

# Styler for the table based on the new requirements
styled_df = (df.style
             # Apply grey shading to row where Rank = 1
             .apply(highlight_rank, axis=1)
             # Set font family, remove vertical borders, and align text
             .set_properties(**{
                 'font-family': 'Roboto, Arial, sans-serif',
                 'color': '#333333',
                 'border': 'none',  # No vertical borders
                 'text-align': 'left'
             })
             # Set custom styling for the header and ensure the Player header is left-aligned
             .set_table_styles([
                 {'selector': 'thead th:first-child::after',  # Change header text for the first column (Rank)
                  'props': [('content', '"R"')]},  # Set 'R' as the content for the first column header
                 {'selector': 'thead th:nth-child(2)',
                  'props': [('text-align', 'left'),  # Left align the Player column header
                            ('border-bottom', '2px solid black')]},
                 {'selector': 'thead th',
                  'props': [('background-color', 'white'),  # No shading for the header
                            ('color', 'black'),
                            ('font-weight', 'bold'),
                            ('border-bottom', '2px solid black'),
                            ('text-align', 'center')]},
                 {'selector': 'tbody td:last-child',
                  'props': [('font-weight', 'bold'),
                            ('text-align', 'right')]}  # Right align the Total column
             ])
             # Align Rank column (Rank) to the center
             .set_properties(subset=['Rank'], **{'text-align': 'center'}))

# Display the styled DataFrame in Streamlit without the index
st.title("Styled Table Example with Custom Formatting")
st.write(styled_df.to_html(index=False), unsafe_allow_html=True)

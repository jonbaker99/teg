import streamlit as st
import pandas as pd
import numpy as np

# # Create a sample DataFrame
# df = pd.DataFrame({
#     'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
#     'Date': pd.date_range(start='2023-01-01', periods=5),
#     'Score': [95.5, 82.3, 88.7, 90.1, 79.8],
#     'Grade': ['A', 'B', 'B+', 'A-', 'C+'],
#     'Pass': [True, True, True, True, False],
#     'Department': ['HR', 'IT', 'Finance', 'Marketing', 'Operations']
# })

# def style_dataframe(df):
#     def add_stars(val):
#         if val == 'A':
#             return f'★ {val}'
#         elif val in ['B', 'B+', 'A-']:
#             return f'☆ {val}'
#         else:
#             return val

#     return (df.style
#         .hide(axis="index")
#         .format({
#             'Date': lambda x: x.strftime('%Y-%m-%d'),
#             'Score': '{:.1f}',
#             'Grade': add_stars
#         })
#         .set_properties(subset=['Name', 'Department'], **{'font-weight': 'bold'})
#         .set_properties(subset=['Score'], **{'background-color': '#e6f3ff'})
#         .background_gradient(subset=['Score'], cmap='YlOrRd')
#         .bar(subset=['Score'], color='#5fba7d', vmin=70, vmax=100)
#         .applymap(lambda x: 'color: green' if x else 'color: red', subset=['Pass'])
#         .highlight_max(subset=['Score'], color='yellow')
#         .set_table_styles([
#             {'selector': 'th', 'props': [('background-color', '#f4f4f4'), 
#                                         ('color', '#333'), 
#                                         ('font-weight', 'bold'),
#                                         ('border', '1px solid #ddd'),
#                                         ('font-family', '"Times New Roman", Times, serif')]},
#             {'selector': 'td', 'props': [('padding', '8px'),
#                                         ('border', '1px solid #ddd')]},
#             {'selector': '', 'props': [('border-collapse', 'collapse')]},
#             {'selector': 'caption', 'props': [('caption-side', 'bottom'), 
#                                               ('font-style', 'italic'),
#                                               ('font-family', 'Georgia, serif')]},
#             {'selector': 'td:nth-child(1)', 'props': [('font-family', 'Arial, sans-serif')]},  # Name column
#             {'selector': 'td:nth-child(2)', 'props': [('font-family', '"Courier New", Courier, monospace')]},  # Date column
#             {'selector': 'td:nth-child(3)', 'props': [('font-family', '"Trebuchet MS", sans-serif')]},  # Score column
#             {'selector': 'td:nth-child(4)', 'props': [('font-family', 'Verdana, sans-serif')]},  # Grade column
#             {'selector': 'td:nth-child(5)', 'props': [('font-family', '"Lucida Console", Monaco, monospace')]},  # Pass column
#             {'selector': 'td:nth-child(6)', 'props': [('font-family', '"Palatino Linotype", "Book Antiqua", Palatino, serif')]},  # Department column
#         ])
#         .set_caption("Student Performance Report")
#         .apply(lambda x: [f'data-toggle="tooltip" title="Score: {x["Score"]:.1f}, Pass: {x["Pass"]}"'] * len(x), axis=1)
#     )

# st.title("Comprehensive Pandas Styler Example with Mixed Fonts - USES CSS")

# # Display the styled dataframe
# styled_df = style_dataframe(df)
# st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# # Add CSS for tooltips and additional font styling
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Roboto&family=Merriweather&display=swap');

# [data-toggle="tooltip"] {
#   position: relative;
#   cursor: pointer;
# }

# [data-toggle="tooltip"]:hover::before {
#   content: attr(title);
#   position: absolute;
#   bottom: 100%;
#   left: 50%;
#   transform: translateX(-50%);
#   padding: 5px;
#   background-color: #333;
#   color: white;
#   border-radius: 3px;
#   white-space: nowrap;
#   z-index: 1;
#   font-family: 'Roboto', sans-serif;
# }

# table {
#   font-family: 'Merriweather', serif;
# }
# </style>
# """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import numpy as np

# Create a sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Date': pd.date_range(start='2023-01-01', periods=5),
    'Score': [95.5, 82.3, 88.7, 90.1, 79.8],
    'Grade': ['A', 'B', 'B+', 'A-', 'C+'],
    'Pass': [True, True, True, True, False],
    'Department': ['HR', 'IT', 'Finance', 'Marketing', 'Operations']
})

def style_dataframe_core_styler(df):
    return (df.style
        # 1. Hide index
        .hide(axis="index")
        
        # 2. Format specific columns
        .format({
            'Date': lambda x: x.strftime('%Y-%m-%d'),
            'Score': '{:.1f}',
            'Grade': lambda x: f'Grade: {x}'
        })
        
        # 3. Set properties for specific columns
        .set_properties(subset=['Name', 'Department'], **{'font-weight': 'bold'})
        .set_properties(subset=['Score'], **{'background-color': 'lightblue'})
        
        # 4. Apply color gradient
        .background_gradient(subset=['Score'], cmap='YlOrRd')
        
        # 5. Add data bars
        .bar(subset=['Score'], color='lightgreen', vmin=70, vmax=100)
        
        # 6. Highlight specific values
        .highlight_max(subset=['Score'], color='yellow')
        .highlight_min(subset=['Score'], color='lightgray')
        
        # 7. Apply styles based on data values
        .applymap(lambda x: 'color: green' if x else 'color: red', subset=['Pass'])
        
        # 8. Apply custom formatting function
        .applymap(lambda x: f'color: {"red" if x < 85 else "black"}', subset=['Score'])
        
        # 9. Add a caption
        .set_caption("Student Performance Report")
    )

st.title("Pandas Styler Core Formatting Examples")

# Display the styled dataframe
styled_df = style_dataframe_core_styler(df)
st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)
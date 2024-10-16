import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Handicaps")

def format_change(val):
    if val > 0:
        return f"+{val}"
    elif val < 0:
        return str(val)
    else:
        return "-"

def format_value(val):
    if pd.isna(val) or val == 0:
        return "-"
    return str(int(val))


st.title("Handicaps")

# Current handicaps data
current_handicaps = pd.DataFrame({
    'Handicap': ['Gregg WILLIAMS', 'Dave MULLIN', 'Jon BAKER', 'John PATTERSON', 'Stuart NEUMANN', 'Alex BAKER'],
    #'TEG 16': [16, 20, 19, 26, 29, 30],
    'TEG 17': [16, 21, 22, 26, 27, 34],
    'Change': [0, 1, 3, 0, -2, 3]
})

# Format the "Change" column
current_handicaps_formatted = current_handicaps.copy()
current_handicaps_formatted['Change'] = current_handicaps_formatted['Change'].apply(format_change)

tab1, tab2 = st.tabs(["TEG 17 Handicaps", "Handicap History"])

with tab1:
    st.write(current_handicaps_formatted.to_html(index=False, justify='left'), unsafe_allow_html=True)

    '---'

    # st.write(current_handicaps)

    # # Create a container for metrics
    # metric_container = st.container()

    # with metric_container:
        
    #     # Create six columns
    #     col1,col2,col3,col4,col5,col6 = st.columns(6)

    #     with col1:
    #         st.metric(label='Gregg WILLIAMS',value=16,delta=0,delta_color='inverse')

    #     with col2:
    #         st.metric(label='David MULLIN',value=21,delta=1,delta_color='inverse')

    # Function to insert Unicode Line Separator
    
    
    def format_name(name):
        return '  \n'.join(name.split(' '))  # Double space + newline for Markdown line break

    current_handicaps['Handicap_formatted'] = current_handicaps['Handicap'].apply(format_name)


    # Title
    st.title("Golf Handicaps Summary")

    # Create a container for custom metrics
    custom_metric_container = st.container()

    with custom_metric_container:
        # Create six columns
        cols = st.columns(6)
        
        # Iterate through the columns and DataFrame rows simultaneously
        for col, (_, row) in zip(cols, current_handicaps.iterrows()):
            with col:
                # Display the Handicap name with a line break using Markdown
                #st.markdown(f"**{format_name(row['Handicap'])}**")
                
                # Display the TEG 17 value and Change using st.metric
                st.metric(
                    #label="TEG 17",
                    label = row['Handicap_formatted'],
                    value=row['TEG 17'],
                    delta=row['Change'],
                    delta_color='off'
                )


    # Optional: Add some spacing or additional information
    st.markdown("---")
    st.write("**Note:** The 'Change' indicates the difference in handicap from the previous period.")




with tab2:
    try:
        historic_handicaps = pd.read_csv("../data/handicaps.csv")
        
        # Apply formatting to all columns except the first one (assuming the first column is names or dates)
        for col in historic_handicaps.columns[1:]:
            historic_handicaps[col] = historic_handicaps[col].apply(format_value)
        
        # Display historic handicaps without index, non-sortable, and left-aligned headers
        st.write(historic_handicaps.to_html(index=False, justify='left'), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Error: The file '../data/handicaps.csv' was not found.")
    except pd.errors.EmptyDataError:
        st.warning("The file '../data/handicaps.csv' is empty.")
    except Exception as e:
        st.error(f"An error occurred while reading the CSV file: {str(e)}")
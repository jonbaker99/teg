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

def handicaps_page():
    st.title("Handicaps")

    # Current handicaps data
    current_handicaps = pd.DataFrame({
        'Handicap': ['Gregg WILLIAMS', 'Dave MULLIN', 'Jon BAKER', 'John PATTERSON', 'Stuart NEUMANN', 'Alex BAKER'],
        #'TEG 16': [16, 20, 19, 26, 29, 30],
        'TEG 17': [16, 21, 22, 26, 27, 34],
        'Change': [0, 1, 3, 0, -2, 3]
    })

    # Format the "Change" column
    current_handicaps['Change'] = current_handicaps['Change'].apply(format_change)

    # Display current handicaps table without index, non-sortable, and left-aligned headers
    st.write(current_handicaps.to_html(index=False, justify='left'), unsafe_allow_html=True)

    # Collapsible section for historic handicaps
    with st.expander("Historic Handicaps"):
        # Read historic handicaps from CSV
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

if __name__ == "__main__":
    handicaps_page()
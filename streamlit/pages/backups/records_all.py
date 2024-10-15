import streamlit as st
import pandas as pd
from typing import Dict, Tuple, List
from utils import get_complete_teg_data, get_round_data

# Constants
METRICS: Dict[str, str] = {
    'Gross': 'GrossVP',
    'Net': 'NetVP',
    'Stableford': 'Stableford'
}

@st.cache_data
def get_aggregated_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch and cache the aggregated TEG and Round data."""
    return get_complete_teg_data(), get_round_data()

def format_score(value: float, column: str) -> str:
    """Format score values based on the column type."""
    if column in ['GrossVP', 'NetVP']:
        return f"+{int(value):.0f}" if value > 0 else f"{int(value):.0f}"
    return f"{int(value):.0f}"

def get_metric_values(df: pd.DataFrame, column: str, aggregation: str) -> pd.DataFrame:
    """Get the best or worst metric values."""
    if column == 'Stableford':
        idx = df[column].idxmax() if aggregation == 'best' else df[column].idxmin()
        sort_ascending = False if aggregation == 'best' else True
    else:
        idx = df[column].idxmin() if aggregation == 'best' else df[column].idxmax()
        sort_ascending = True if aggregation == 'best' else False
    
    return df[df[column] == df.loc[idx, column]].sort_values(by=column, ascending=sort_ascending)

def prepare_output_dataframe(metric_values: pd.DataFrame, column: str, metric_name: str) -> pd.DataFrame:
    """Prepare the output DataFrame with formatted columns."""
    if 'Round' in metric_values.columns:
        metric_values['Round_Display'] = metric_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)
        selected_columns = ['Player', column, 'Round_Display', 'Course', 'Date']
        rename_dict = {column: 'Score', 'Round_Display': 'Round'}
    else:
        selected_columns = ['Player', column, 'TEG', 'Year']
        rename_dict = {column: 'Score'}
    
    output = metric_values[selected_columns].rename(columns=rename_dict)
    output['Measure'] = metric_name
    output['Score'] = output['Score'].apply(lambda x: format_score(x, column))
    
    return output[['Measure'] + [col for col in output.columns if col != 'Measure']]

def display_metric_overall(df: pd.DataFrame, metric_name: str, column: str, aggregation: str = 'best') -> pd.DataFrame:
    """Display the best or worst metric across all players for a specific score type."""
    try:
        metric_values = get_metric_values(df, column, aggregation)
        return prepare_output_dataframe(metric_values, column, metric_name)
    except Exception as e:
        st.error(f"Error processing {metric_name}: {str(e)}")
        return pd.DataFrame()

def combine_metrics(data: pd.DataFrame, aggregation_type: str) -> pd.DataFrame:
    """Combine metrics for best or worst performances."""
    return pd.concat([display_metric_overall(data, metric_name, column, aggregation_type) 
                      for metric_name, column in METRICS.items()], 
                     ignore_index=True)

def display_table(df: pd.DataFrame, title: str) -> None:
    """Display a formatted table in Streamlit."""
    st.subheader(title)
    st.write(df.to_html(index=False, classes=['table', 'table-striped', 'table-hover'], escape=False), unsafe_allow_html=True)

def show_combined_metrics() -> None:
    """Display combined best and worst TEGs and Rounds tables."""
    try:
        teg_data, round_data = get_aggregated_data()

        tables = [
            ("Best TEGs", combine_metrics(teg_data, 'best')),
            ("Best Rounds", combine_metrics(round_data, 'best')),
            ("Worst TEGs", combine_metrics(teg_data, 'worst')),
            ("Worst Rounds", combine_metrics(round_data, 'worst'))
        ]

        for title, df in tables:
            display_table(df, title)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main() -> None:
    st.set_page_config(page_title="TEG Records", page_icon="⛳")
    st.title("TEG Records")

    # # Add a refresh button
    # if st.button("Refresh Data"):
    #     st.cache_data.clear()
    #     st.experimental_rerun()

    show_combined_metrics()

if __name__ == "__main__":
    main()
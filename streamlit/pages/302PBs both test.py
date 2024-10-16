import streamlit as st
import pandas as pd
from utils import get_complete_teg_data, get_round_data

def display_metric(df, metric_name, column, group_by=['Player'], aggregation='best'):
    if aggregation not in ['best', 'worst']:
        st.error("Invalid aggregation type. Choose 'best' or 'worst'.")
        return

    try:
        if column == 'Stableford':
            idx = df.groupby(group_by)[column].idxmax() if aggregation == 'best' else df.groupby(group_by)[column].idxmin()
            sort_ascending = False if aggregation == 'best' else True
        else:
            idx = df.groupby(group_by)[column].idxmin() if aggregation == 'best' else df.groupby(group_by)[column].idxmax()
            sort_ascending = True if aggregation == 'best' else False

        metric_values = df.loc[idx]
        
        display_title = f"Personal {aggregation.capitalize()} " + ("Round" if 'Round' in df.columns else "TEG") + f": {metric_name}"

        if 'Round' in df.columns:
            metric_values['Round_Display'] = metric_values.apply(lambda x: f"{x['TEG']}|R{x['Round']}", axis=1)
            selected_columns = ['Player', column, 'Round_Display', 'Course', 'Date']
            rename_dict = {column: 'Score', 'Round_Display': 'Round'}
        else:
            selected_columns = ['Player', column, 'TEG', 'Year']
            rename_dict = {column: 'Score'}

        output = metric_values[selected_columns].rename(columns=rename_dict).sort_values(by='Score', ascending=sort_ascending).reset_index(drop=True)

        output['Score'] = output['Score'].apply(lambda x: f"+{int(x):.0f}" if x > 0 else f"{int(x):.0f}" if column in ['GrossVP', 'NetVP'] else f"{int(x):.0f}")

        if 'Year' in output.columns:
            output['Year'] = output['Year'].astype(int)

        #output = output.sort_values(by='Score', ascending=sort_ascending).reset_index(drop=True)

        st.subheader(display_title)
        st.write(output.to_html(index=False, justify='left'), unsafe_allow_html=True)

    except KeyError as e:
        st.error(f"KeyError encountered while processing {metric_name}: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred while processing {metric_name}: {e}")

def show_teg_metrics():
    try:
        teg_data = get_complete_teg_data()
        df_merged = teg_data

        metrics = {
            'Gross': 'GrossVP',
            'Net': 'NetVP',
            'Stableford': 'Stableford'
        }

        required_columns = ['Player', 'Sc', 'GrossVP', 'NetVP', 'Stableford', 'TEG', 'Year']
        missing_columns = [col for col in required_columns if col not in df_merged.columns]
        if missing_columns:
            st.error(f"Missing columns in TEG data: {missing_columns}")
            return

        for metric_name, column in metrics.items():
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='best')
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='worst')

    except Exception as e:
        st.error(f"An unexpected error occurred in TEG Metrics: {e}")

def show_round_metrics():
    try:
        round_data = get_round_data()
        df_merged = round_data

        metrics = {
            'Gross': 'GrossVP',
            'Net': 'NetVP',
            'Stableford': 'Stableford'
        }

        required_columns = ['Player', 'Sc', 'GrossVP', 'NetVP', 'Stableford', 'TEG', 'Round', 'Course', 'Date']
        missing_columns = [col for col in required_columns if col not in df_merged.columns]
        if missing_columns:
            st.error(f"Missing columns in Round data: {missing_columns}")
            return

        for metric_name, column in metrics.items():
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='best')
            display_metric(df=df_merged, metric_name=metric_name, column=column, group_by=['Player'], aggregation='worst')

    except Exception as e:
        st.error(f"An unexpected error occurred in Round Metrics: {e}")

def main():
    st.title("Personal Bests (& Worsts)")

    tab1, tab2 = st.tabs(["By TEG", "By Round"])

    with tab1:
        show_teg_metrics()

    with tab2:
        show_round_metrics()

if __name__ == "__main__":
    main()
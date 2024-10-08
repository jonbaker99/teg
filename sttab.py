import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

@st.cache_data
def aggregate_to_round_level(df):
    measures = ['Sc', 'GrossVP', 'NetVP', 'Stableford']
    player_column = 'Player' if 'Player' in df.columns else 'Pl'
    group_rd = [player_column, 'TEGNum', 'TEG', 'Round']
    return df.groupby(group_rd, as_index=False)[measures].sum().sort_values(by=[player_column,'TEGNum','Round'])

def create_leaderboard(leaderboard_df, value_column, ascending=True):
    player_column = 'Player' if 'Player' in leaderboard_df.columns else 'Pl'
    
    jacketboard_pivot = leaderboard_df.pivot_table(
        index=player_column, 
        columns='Round', 
        values=value_column, 
        aggfunc='sum', 
        fill_value=0
    ).assign(Total=lambda x: x.sum(axis=1)).sort_values('Total', ascending=ascending)

    jacketboard_pivot.columns = [f'R{col}' if isinstance(col, int) else col for col in jacketboard_pivot.columns]

    jacketboard_pivot = jacketboard_pivot.reset_index()
    jacketboard_pivot['Rank'] = jacketboard_pivot['Total'].rank(method='min', ascending=ascending).astype(int)

    duplicated_scores = jacketboard_pivot['Total'].duplicated(keep=False)
    jacketboard_pivot.loc[duplicated_scores, 'Rank'] = jacketboard_pivot.loc[duplicated_scores, 'Rank'].astype(str) + '='

    columns = ['Rank', player_column] + [col for col in jacketboard_pivot.columns if col not in ['Rank', player_column]]
    jacketboard_pivot = jacketboard_pivot[columns]

    return jacketboard_pivot

def get_custom_css():
    return """
    <style>
        .datawrapper-table {
            font-family: Arial, sans-serif !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            width: 100% !important;
            font-size: 14px !important;
            margin-bottom: 40px !important;  /* Increased bottom margin */
        }
        .datawrapper-table th, .datawrapper-table td {
            text-align: center !important;
            padding: 12px 8px !important;
            border: none !important;
            border-bottom: 1px solid #e0e0e0 !important;
        }
        .datawrapper-table th {
            font-weight: bold !important;
            border-bottom: 2px solid #000 !important;
        }
        .datawrapper-table tr:hover {
            background-color: #f5f5f5 !important;
        }
        .datawrapper-table .total {
            font-weight: bold !important;
        }
        .datawrapper-table td:nth-child(2),
        .datawrapper-table th:nth-child(2) {
            text-align: left !important;
        }
        .datawrapper-table td:first-child {
            font-size: 12px !important;
            width: 30px !important;
            max-width: 30px !important;
        }
        .datawrapper-table th:first-child {
            width: 30px !important;
            max-width: 30px !important;
        }
        .datawrapper-table .top-rank {
            background-color: #f7f7f7 !important;
        }
        .leaderboard-header {
            font-size: 18px !important;  /* Smaller font for headers */
            margin-top: 30px !important;  /* Space above header */
            margin-bottom: 10px !important;  /* Space below header */
        }
        .divider {
            border-top: 1px solid #e0e0e0;
            margin: 40px 0;  /* Space above and below divider */
        }
    </style>
    """

def generate_table_html(df):
    html = ["<table class='datawrapper-table'>"]
    html.append("<tr><th></th>" + "".join(f"<th>{col}</th>" for col in df.columns[1:]) + "</tr>")
    
    for _, row in df.iterrows():
        row_class = ' class="top-rank"' if row['Rank'] == 1 or row['Rank'] == '1=' else ''
        html.append(f"<tr{row_class}>")
        for i, value in enumerate(row):
            if df.columns[i] == 'Total':
                html.append(f'<td class="total">{value}</td>')
            else:
                html.append(f'<td>{value}</td>')
        html.append("</tr>")
    
    html.append("</table>")
    return "".join(html)

def get_champions(df):
    return ', '.join(df[df['Rank'] == 1]['Player'].tolist())

def main():
    st.set_page_config(page_title="Golf Scores", page_icon="⛳")
    
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    df = load_data(r'data/teg-all-data-long.csv')
    round_df = aggregate_to_round_level(df)

    teg_order = round_df[['TEG', 'TEGNum']].drop_duplicates().sort_values('TEGNum')
    tegs = teg_order['TEG'].tolist()
    chosen_teg = st.selectbox('Select TEG', tegs)

    leaderboard_df = round_df[round_df['TEG'] == chosen_teg]

    st.subheader(f'Leaderboard for {chosen_teg}')

    # Stableford Leaderboard
    stableford_leaderboard = create_leaderboard(leaderboard_df, 'Stableford', ascending=False)
    stableford_champions = get_champions(stableford_leaderboard)
    st.markdown(f"<h3 class='leaderboard-header'>TEG Trophy result (best Stableford)<br>Champion: {stableford_champions}</h3>", unsafe_allow_html=True)
    table_html = generate_table_html(stableford_leaderboard)
    st.markdown(table_html, unsafe_allow_html=True)

    # GrossVP Leaderboard
    grossvp_leaderboard = create_leaderboard(leaderboard_df, 'GrossVP', ascending=True)
    grossvp_champions = get_champions(grossvp_leaderboard)
    st.markdown(f"<h3 class='leaderboard-header'>Green Jacket result (best gross)<br>Champion: {grossvp_champions}</h3>", unsafe_allow_html=True)
    table_html = generate_table_html(grossvp_leaderboard)
    st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
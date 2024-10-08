import streamlit as st
import pandas as pd

def get_custom_css():
    return """
    <style>
        .datawrapper-table {
            font-family: Arial, sans-serif !important;
            border-collapse: separate !important;
            border-spacing: 0 !important;
            width: 100% !important;
            font-size: 14px !important;
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
    </style>
    """

def prepare_data(df):
    df = df.sort_values('Total', ascending=False)
    df['Rank'] = df['Total'].rank(method='min', ascending=False).astype(int)
    return df[['Rank', 'Player', 'R1', 'R2', 'R3', 'R4', 'Total']]

def generate_table_html(df):
    html = ["<table class='datawrapper-table'>"]
    html.append("<tr><th></th>" + "".join(f"<th>{col}</th>" for col in df.columns[1:]) + "</tr>")
    
    for _, row in df.iterrows():
        row_class = ' class="top-rank"' if row['Rank'] == 1 else ''
        html.append(f"<tr{row_class}>")
        for i, value in enumerate(row):
            if df.columns[i] == 'Total':
                html.append(f'<td class="total">{value}</td>')
            else:
                html.append(f'<td>{value}</td>')
        html.append("</tr>")
    
    html.append("</table>")
    return "".join(html)

def main():
    st.set_page_config(page_title="Golf Scores", page_icon="⛳")
    
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Sample data
    data = {
        'Player': ['Stuart Neumann', 'Gregg Williams', 'David Mullin', 'Jon Baker', 'Alex Baker'],
        'R1': [39, 34, 33, 34, 29],
        'R2': [35, 30, 34, 32, 32],
        'R3': [39, 37, 30, 33, 33],
        'R4': [43, 42, 45, 32, 33],
        'Total': [156, 143, 142, 131, 127]
    }
    df = pd.DataFrame(data)

    df = prepare_data(df)

    tegs = ['TEG1', 'TEG2', 'TEG3']
    selected_teg = st.selectbox('Select TEG', tegs)

    st.subheader(f'Data for {selected_teg}')

    table_html = generate_table_html(df)
    st.markdown(table_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
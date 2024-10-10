import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
from golf_data import player_scores, stableford_data, avg_score_by_par


# Assume we have the data from the previous example
# player_scores, stableford_data, avg_score_by_par

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Golf Tournament Dashboard'),
    
    html.H2('Player Scores'),
    dash_table.DataTable(
        id='player-scores-table',
        columns=[{"name": i, "id": i} for i in player_scores.columns],
        data=player_scores.to_dict('records'),
    ),
    
    html.H2('Stableford Race'),
    dcc.Graph(id='stableford-race-chart'),
    
    html.H2('Average Score by Par'),
    dcc.Graph(id='avg-score-by-par-chart')
])

@app.callback(
    Output('stableford-race-chart', 'figure'),
    Output('avg-score-by-par-chart', 'figure'),
    Input('player-scores-table', 'data')
)
def update_charts(data):
    # Line Chart
    fig_line = px.line(stableford_data, x=stableford_data.index, y=stableford_data.columns,
                       labels={'index': 'Hole number', 'value': 'Stableford Points'},
                       title='Stableford Race')
    
    # Bar Chart
    fig_bar = px.bar(avg_score_by_par.melt(id_vars=['Player'], var_name='Par', value_name='Score'),
                     x='Player', y='Score', color='Par', barmode='group',
                     labels={'Score': 'Avg. Score over Par'},
                     title='Average Score by Par')
    
    return fig_line, fig_bar

if __name__ == '__main__':
    app.run_server(debug=True)
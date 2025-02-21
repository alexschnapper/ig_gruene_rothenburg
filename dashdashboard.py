import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash App initialisieren
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Instagram Data Dashboard'),

    html.Div(children='''
        Analyse der Instagram-Daten.
    '''),

    dcc.Graph(
        id='posts-per-month',
        figure=fig_posts
    ),

    dcc.Graph(
        id='impressions-per-month',
        figure=fig_impressions
    ),

    dcc.Graph(
        id='reach-per-month',
        figure=fig_reach
    ),

    dcc.Graph(
        id='engagement-per-month',
        figure=fig_engagement
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
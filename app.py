import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Daten laden
df = pd.read_csv('data/instagram_data.csv')
posts_per_month = pd.read_csv('data/posts_per_month.csv', index_col=0)
impressions_per_month = pd.read_csv('data/impressions_per_month.csv', index_col=0)
reach_per_month = pd.read_csv('data/reach_per_month.csv', index_col=0)
engagement_per_month = pd.read_csv('data/engagement_per_month.csv', index_col=0)

# Daten analysieren
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['year_month'] = df['timestamp'].dt.to_period('M')

# Anzahl der Beiträge pro Monat
fig_posts = px.bar(posts_per_month, x=posts_per_month.index, y=posts_per_month.values, title='Posts per Month')

# Impressions pro Monat
fig_impressions = px.line(impressions_per_month, x=impressions_per_month.index, y=impressions_per_month.values, title='Impressions per Month')

# Reach pro Monat
fig_reach = px.line(reach_per_month, x=reach_per_month.index, y=reach_per_month.values, title='Reach per Month')

# Engagement pro Monat
fig_engagement = px.line(engagement_per_month, x=engagement_per_month.index, y=engagement_per_month.values, title='Engagement per Month')

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
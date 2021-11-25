import plotly.graph_objects as go  # or plotly.express as px
import dash
from dash import dcc
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import json
import plotly.express as px
import numpy as np
from urllib.request import urlopen
class DataViz():
    def __init__(self, df_full_json):
        self.df_full_json = df_full_json
    def read_csv(self):
        self.df_full_json = pd.read_csv(
            '../lung_pollution/data/covid_pollution_json_rifqi.csv')
        return self.df_full_json

    def fig(self, *args, **kwargs):
        app = dash.Dash()
        with urlopen('https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/1_sehr_hoch.geo.json') as response:
            counties = json.load(response)
        fig = px.choropleth_mapbox(self.df_full_json,
                           geojson=counties,
                           locations='county_new',
                           featureidkey="properties.NAME_3",
                           color='cases_per_100k',
                           color_continuous_scale="Viridis",
                           range_color=(0, 15000),
                           mapbox_style="carto-positron",
                           zoom=4.5, center = {"lat":  51.312801, "lon":  9.481544},
                           opacity=0.5,
                           labels={'cases':'cases per 100k'}
                          )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.Div([html.H1("Lung Pollution", className='display-3'),
                              html.P(
                                  'Our project is done, Dorien can buy us drinks',
                                  className='lead',
                              ),
                              html.P('', className='font-italic'),
                ]), width=10),
            ], className= 'mb-4 mt-2'),

            dbc.Row([
                dbc.Col(html.Div(dcc.Graph(figure=fig)),
            width=5),
            dbc.Col(html.Div([html.H1("Lung Pollution", className='display-3'),
                              html.P(
                                  'Our project is done, Dorien can buy us drinks',
                                  className='lead',
                              ),
                              html.P('', className='font-italic'),
                ]), width=10)
            ])
            ], fluid=True)
        if __name__ == '__main__':
            app.run_server(host='0.0.0.0', port=8089,
                   debug=True, use_reloader=False)
        return fig

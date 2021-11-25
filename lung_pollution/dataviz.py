import plotly.graph_objects as go  # or plotly.express as px
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import json
import plotly.express as px
import numpy as np
from urllib.request import urlopen

class DataViz():

    def __init__(self, file_name='lung_pollution/data/covid_pollution_final-rifqi.csv'):
        #self.file_name = '../lung_pollution/data/covid_pollution_json_rifqi.csv'
        self.file_name = file_name

    def load_data(self):
        self.df = pd.read_csv(self.file_name)
        return self.df

    def fig_map(self, *args, **kwargs):
        url = 'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/1_sehr_hoch.geo.json'
        with urlopen(url) as response:
            counties = json.load(response)
        fig = px.choropleth_mapbox(
                           self.df,
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

        app = dash.Dash()
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

        return app

if __name__ == '__main__':
    viz = DataViz()
    viz.load_data()
    #print(data)
    app = viz.fig_map()
    app.run_server(host='127.0.0.1', port=8070, debug=True, use_reloader=False)

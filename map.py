#import plotly.graph_objects as go  # or plotly.express as px
import dash
#import dash_core_components as dcc
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
#import dash_html_components as html
import pandas as pd
import json
import plotly.express as px
import numpy as np
from urllib.request import urlopen
from dash.dependencies import Output, Input
from flask_caching import Cache
#import os
import base64
#from google.cloud import storage

#################################################################################
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    #prevent_initial_callbacks=True,
    meta_tags=[{
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }])

cache = Cache(
    app.server,
    config={
        #'CACHE_TYPE': 'redis',
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': 'cache-directory'
    })

TIMEOUT = 3600

server = app.server

app.config.suppress_callback_exceptions = True

####################################################################################
with urlopen(
        'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/4_niedrig.geo.json'
) as response:
    counties = json.load(response)

import pandas as pd

df = pd.read_csv("./lung_pollution/data/covid_pollution_complete.csv")

###############################################################################

app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    html.H1(
                        "Air Pollution & CoViD-19 in Germany",
                        #className='display-3',
                        style={'textAlign': 'left'}),
                    html.P('Impact of air pollution on CoViD-19',
                           className='lead',
                           style={'textAlign': 'left'}),
                    html.P('', className='font-italic'),
                ]),
                width=10),
        ],
        className='mb-4 mt-2'),
    dbc.Row([
        dbc.Col(html.Div([
            html.P("Pollutants:"),
            dcc.RadioItems(id='pollutant',
                           options=[{
                               'label': 'NO annualMean',
                               'value': 'NO_annualMean'
                           }, {
                               'label': 'NO2 annualMean',
                               'value': 'NO2_annualMean'
                           },
                           {
                               'label': 'O3 annualMean',
                               'value': 'O3_annualMean'
                           }, {
                               'label': 'PM2.5 annualMean',
                               'value': 'PM2_5_annualMean'
                           }
                            ],
                           value='NO_annualMean',
                           labelStyle={'display': 'inline-block'},
                           inputStyle={"margin-left": "20px"}),
            dcc.Graph(id="choropleth_pollutant")
        ]),
                width=6),
        dbc.Col(html.Div([
            html.P("CoViD-19:"),
            dcc.RadioItems(id='covid',
                           options=[{
                               'label': 'Cases per 100k',
                               'value': 'cases_per_100k'
                           }, {
                               'label': 'Deaths per 100k',
                               'value': 'deaths_per_100k'
                           }],
                           value='cases_per_100k',
                           labelStyle={'display': 'inline-block'},
                           inputStyle={"margin-left": "20px"}),
            dcc.Graph(id="choropleth_covid")
        ]),
                width=6),
    ]),
])

###############################################################################

@app.callback(Output("choropleth_pollutant", "figure"),
              [Input("pollutant", "value")])
#@cache.memoize(timeout=TIMEOUT)
def make_map_pollutant(pollutants):
    fig_pollutant = px.choropleth_mapbox(
        df,
        geojson=counties,
        locations='county_new',
        featureidkey="properties.NAME_3",
        color=pollutants,
        color_continuous_scale="ylorrd",  #Emrld
        #range_color=(0, np.max(df["cases_per_100k"])),
        #animation_frame='year',
        mapbox_style="carto-positron",
        zoom=3.8,
        center={
            "lat": 51.312801,
            "lon": 9.481544
        },
        opacity=0.5,
        #labels={'cases_per_100k': 'cases per 100k'}
    )
    fig_pollutant.update_layout(margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    },)
    return fig_pollutant


###covid
@app.callback(Output("choropleth_covid", "figure"), [Input("covid", "value")])
#@cache.memoize(timeout=TIMEOUT)
def make_map_covid(covids):

    if covids == 'cases_per_100k':
        color_scale = "greys"
    elif covids == 'deaths_per_100k':
        color_scale = "amp"

    fig_covid = px.choropleth_mapbox(
        df,
        geojson=counties,
        locations='county_new',
        featureidkey="properties.NAME_3",
        color=covids,
        color_continuous_scale=color_scale,
        #range_color=(0, np.max(df["cases_per_100k"])),
        #animation_frame='year',
        mapbox_style="carto-positron",
        zoom=4.3,
        center={
            "lat": 51.312801,
            "lon": 9.481544
        },
        opacity=0.5,
        #labels={'cases_per_100k': 'cases per 100k'}
    )
    fig_covid.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_covid


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8010, debug=True)

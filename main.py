import plotly.graph_objects as go  # or plotly.express as px
import dash
import dash_core_components as dcc
#from dash import dcc
import dash_bootstrap_components as dbc
#from dash import html
import dash_html_components as html
import pandas as pd
import json
import plotly.express as px
import numpy as np
from urllib.request import urlopen
from dash.dependencies import Output, Input
#from memoized_property import memoized_property
from flask_caching import Cache
#import os
import base64
# import matplotlib as mpl
# import matplotlib.pyplot as plt

# from matplotlib.cm import ScalarMappable
# from matplotlib.lines import Line2D
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# from textwrap import wrap

################################################################################

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],
                #prevent_initial_callbacks=True,
                meta_tags=[{
                    'name': 'viewport',
                    'content': 'width=device-width, initial-scale=1.0'
                }])

cache = Cache(app.server,
              config={
                  #'CACHE_TYPE': 'redis',
                  'CACHE_TYPE': 'filesystem',
                  'CACHE_DIR': 'cache-directory'
              })

TIMEOUT = 3600

server = app.server

app.config.suppress_callback_exceptions = True

############################### DATASETS #######################################

@cache.memoize(timeout=TIMEOUT)
def load_data():
    df1 = pd.read_csv("./lung_pollution/data/covid_pollution_final-rifqi.csv")
    df = df1[[
        'county_new', 'county', 'year', 'NO2_annualMean', 'NO_annualMean',
        'O3_annualMean', 'PM10_annualMean', 'PM2_5_annualMean',
        'cases_per_100k', 'deaths_per_100k', 'fully_vaccinated',
        'Population_density'
    ]]
    return df

df=load_data()

@cache.memoize(timeout=TIMEOUT)
def load_geojson():
    with urlopen(
            'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/4_niedrig.geo.json'
    ) as response:
        counties = json.load(response)
    return counties

counties = load_geojson()


############################### IMAGES, GLOBAL VARIABLES #######################

image_filename = 'introduction.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename_2 = 'model-overview.png'  # replace with your own image
encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())

image_filename_3 = 'feature-permutation.png'  # replace with your own image
encoded_image_3 = base64.b64encode(open(image_filename_3, 'rb').read())

image_filename_4 = 'gauge.png'  # replace with your own image
encoded_image_4 = base64.b64encode(open(image_filename_4, 'rb').read())

pollutants = [
    'NO_annualMean', 'NO2_annualMean', 'O3_annualMean', 'PM2_5_annualMean'
]
covids = ['cases_per_100k', 'deaths_per_100k']

################################ SIDEBAR SETTING ###############################

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H1("NAVIGATIONS", className="lead"),
        html.Hr(),
        html.P("Go to", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Lung Pollution", href="/", active="exact"),
                dbc.NavLink("Air Pollution & CoViD-19 in Germany",
                            href="/page-1",
                            active="exact"),
                dbc.NavLink(
                    "CoViD-19 Predictor", href="/page-2", active="exact"),
                dbc.NavLink(
                    "Under the Hood", href="/page-3", active="exact"),
            ],
            vertical=False,
            pills=True,
        ),
        html.Hr(),
        html.P("Who are we?", className="lead"),
        html.P("Sara Iside Broggini", className="lead-1"),
        html.P("Ana Luiza Curi Christianini", className="lead-1"),
        html.P("Rifqi Farhan", className="lead-1"),
        html.P("Dorien Roosen", className="lead-1"),
    ],
    style=SIDEBAR_STYLE,
)
#################################################################################


content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")],
              prevent_initial_call=True)
#@cache.memoize(timeout=TIMEOUT)
def render_page_content(pathname):
    if pathname == "/":
        return [dbc.Col([
            html.H1('Lung Pollution', style={'textAlign': 'left'}),
            html.P("Welcome to our Data Science Project ", className="lead"),
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                     width=1024, height=550)

            ],width=12)
        ]

    elif pathname == "/page-1":
        return [
            dbc.Container(
                [
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H1("Air Pollution & CoViD-19 in Germany",
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
                            dcc.RadioItems(
                                id='pollutant',
                                options=[{
                                    'value': x,
                                    'label': x
                                } for x in pollutants],
                                value=pollutants[0],
                                labelStyle={'display': 'inline-block'},
                                inputStyle={"margin-left": "20px"}),
                            dcc.Graph(id="choropleth_pollutant")]),
                        width=6),

                        dbc.Col(html.Div([
                            html.P("CoViD-19:"),
                            dcc.RadioItems(
                                id='covid',
                                options=[{
                                    'value': x,
                                    'label': x
                                } for x in covids],
                                value=covids[0],
                                labelStyle={'display': 'inline-block'},
                                inputStyle={"margin-left": "20px"}),
                            dcc.Graph(id="choropleth_covid")]),
                        width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([], width=3),
                        dbc.Col([
                            html.H2("", style={'textAlign': 'center'}),
                            dcc.Dropdown(id='county-searchbox',
                                         multi=False,
                                         value='Berlin',
                                         options=[{
                                             'label': x,
                                             'value': x
                                         } for x in sorted(
                                             df["county_new"].unique())]),
                        ],
                                width=3),
                        dbc.Col([], width=3),
                    ],
                            className='mb-3 mt-2'),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id='graph_no2')), width=4),
                        dbc.Col(html.Div(dcc.Graph(id='graph_no')), width=4),
                        dbc.Col(html.Div(dcc.Graph(id='graph_o3')), width=4),
                        #dbc.Col(html.Div(dcc.Graph(figure=graph_pm10)), width=2),
                        #dbc.Col(html.Div(dcc.Graph(figure=graph_pm25)), width=2),
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(dcc.Graph(id='graph_pm10')), width=4),
                        dbc.Col(html.Div(dcc.Graph(id='graph_pm25')), width=4),
                        #dbc.Col([], width=3),
                        #dbc.Col(html.Div(dcc.Graph(id='graph_o3')), width=4),
                        #dbc.Col(html.Div(dcc.Graph(figure=graph_pm10)), width=2),
                        #dbc.Col(html.Div(dcc.Graph(figure=graph_pm10)), width=2),
                    ]),
                ],
                fluid=True)
        ]

    elif pathname == "/page-2":
        return [
            dbc.Row([
                dbc.Col([
                    html.H1('CoViD-19 Predictor', style={'textAlign': 'left'}),
                    html.P("It's time to make a prediction!",
                           className="lead"),
                ],
                        width=12),
                dbc.Col([
                    html.I("Input: NO"),
                    html.Br(),
                    dcc.Input(id='input1',
                              placeholder='Enter a value...',
                              type='number',
                              value='',
                              style={'marginRight': '10px'})
                ],
                        width=3),
                dbc.Col([
                    html.I("Input: NO2"),
                    html.Br(),
                    dcc.Input(id='input2',
                              placeholder='Enter a value...',
                              type='number',
                              value='',
                              style={'marginRight': '10px'})
                ],
                        width=3),
                dbc.Col([
                    html.I("Input: O3"),
                    html.Br(),
                    dcc.Input(id='input3',
                              placeholder='Enter a value...',
                              type='number',
                              value='',
                              style={'marginRight': '10px'})
                ],
                        width=3),
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        html.H1(' ', style={'textAlign': 'left'}),
                        #html.P(" ", className="lead"),
                    ],
                    width=12),
            ]),
            dbc.Row([
                dbc.Col([
                    html.I("Input: PM2.5"),
                    html.Br(),
                    dcc.Input(id='input4',
                              placeholder='Enter a value...',
                              type='number',
                              value='',
                              style={'marginRight': '10px'})
                ],
                        width=3),
                dbc.Col([
                    html.I("Input: Population Density"),
                    html.Br(),
                    dcc.Input(id='input5',
                              placeholder='Enter a value...',
                              type='number',
                              value='',
                              style={'marginRight': '10px'})
                ],
                        width=3),
                dbc.Col([
                    html.I("Input: Vaccination Rate"),
                    html.Br(),
                    dcc.Input(id='input6',
                              placeholder='Enter a value...',
                              type='number',
                              value='',
                              style={'marginRight': '10px'})
                ],
                        width=3),
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        html.H1(' ', style={'textAlign': 'left'}),
                        #html.P(" ", className="lead"),
                    ],
                    width=12),
            ]),
            dbc.Row([
                dbc.Col([], width=3),
                dbc.Col(
                    [
                        #html.Div(dcc.Input(id='input-on-submit', type='text')),
                        html.Br(),
                        html.Button('Predict', id='submit-val', n_clicks=0),
                        # html.Div(id='container-button-basic',
                        #          children='Press Predict'),
                        html.Br(),
                    ],
                    width=3),
                #dbc.Col([], width=3),
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        html.P('Output: CoViD-19 Cases',
                               style={'textAlign': 'centre'},
                               className="lead"),
                        #html.P("Feature Permutation ", className="lead"),
                        html.Img(src='data:image/png;base64,{}'.format(
                            encoded_image_4.decode()),
                                 width=615,
                                 height=308)
                    ],
                    width=6),
                dbc.Col(
                    [
                        #html.H1('Under the Hood', style={'textAlign': 'left'}),
                        html.P("Relative Importance of CoViD-19 Modulators ",
                               className="lead"),
                        html.Img(src='data:image/png;base64,{}'.format(
                            encoded_image_3.decode()),
                                 width=450,
                                 height=350)
                    ],
                    width=4)
                #dbc.Col(html.Div(dcc.Graph(id='graph_no')), width=4),
                #dbc.Col(html.Div(dcc.Graph(id='graph_o3')), width=4),
                #dbc.Col(html.Div(dcc.Graph(figure=graph_pm10)), width=2),
                #dbc.Col(html.Div(dcc.Graph(figure=graph_pm25)), width=2),
            ]),
        ]

    elif pathname == "/page-3":
        return [
            dbc.Col([
                html.H1('Under the Hood', style={'textAlign': 'left'}),
                html.P("Model Overview ", className="lead"),
                html.Img(src='data:image/png;base64,{}'.format(
                    encoded_image_2.decode()),
                         width=1024,
                         height=550)
            ],
                    width=12)
        ]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron([
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised..."),
    ])

######pollutant
@app.callback(
    Output("choropleth_pollutant", "figure"),
    [Input("pollutant", "value")])
@cache.memoize(timeout=TIMEOUT)
def make_map_pollutant(pollutants):
    fig_pollutant = px.choropleth_mapbox(df,
                                    geojson=counties,
                                    locations='county_new',
                                    featureidkey="properties.NAME_3",
                                    color=pollutants,
                                    color_continuous_scale="Emrld",
                                    #range_color=(0, np.max(df["cases_per_100k"])),
                                    animation_frame='year',
                                    mapbox_style="carto-positron",
                                    zoom=3.5,
                                    center={
                                        "lat": 51.312801,
                                        "lon": 9.481544
                                    },
                                    opacity=0.5,
                                    #labels={'cases_per_100k': 'cases per 100k'}
                                    )
    fig_pollutant.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_pollutant

###covid
@app.callback(Output("choropleth_covid", "figure"),
              [Input("covid", "value")])
@cache.memoize(timeout=TIMEOUT)
def make_map_covid(covids):
    fig_covid = px.choropleth_mapbox(
        df,
        geojson=counties,
        locations='county_new',
        featureidkey="properties.NAME_3",
        color=covids,
        color_continuous_scale="greys",
        #range_color=(0, np.max(df["cases_per_100k"])),
        #animation_frame='year',
        mapbox_style="carto-positron",
        zoom=3.5,
        center={
            "lat": 51.312801,
            "lon": 9.481544
        },
        opacity=0.5,
        #labels={'cases_per_100k': 'cases per 100k'}
    )
    fig_covid.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_covid


@app.callback([
    Output(component_id='graph_no2', component_property='figure'),
    Output(component_id='graph_no', component_property='figure'),
    Output(component_id='graph_o3', component_property='figure'),
    Output(component_id='graph_pm10', component_property='figure'),
    Output(component_id='graph_pm25', component_property='figure'),
], [Input(component_id='county-searchbox', component_property='value')])
#@cache.memoize(timeout=TIMEOUT)
def update_graph(county_selected):
    #dff = df.copy()
    dff = df[df["county_new"] == county_selected]

    height = 280
    width = 350

    template = 'plotly'

    # Graph for pollutant 1 (NO2)
    graph_no2 = px.area(dff,
                        x='year',
                        y='NO2_annualMean',
                        title='NO2 (annual mean) [µg/cm3]',
                        template=template,
                        height=height,
                        width=width,
                        range_y=[
                            df['NO2_annualMean'].min(),
                            1.1 * df['NO2_annualMean'].max()
                        ]).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                                         paper_bgcolor='rgba(0,0,0,0)',
                                         plot_bgcolor='rgba(0,0,0,0)',
                                         yaxis=dict(title=None,
                                                    showgrid=True,
                                                    showticklabels=True),
                                         xaxis=dict(title=None,
                                                    showgrid=False,
                                                    showticklabels=True))

    graph_no2.update_yaxes(
        showline=False,
        linewidth=0.25,
        matches=None,  #autoscale y axis
        linecolor='gray',
        gridcolor='gray')

    # Graph for pollutant 2 (NO)
    graph_no = px.area(dff,
                       x='year',
                       y='NO_annualMean',
                       title='NO (annual mean) [µg/cm3]',
                       template=template,
                       height=height,
                       width=width,
                       range_y=[
                           df['NO_annualMean'].min(),
                           1.1 * df['NO_annualMean'].max()
                       ]).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        yaxis=dict(title=None,
                                                   showgrid=True,
                                                   showticklabels=True),
                                        xaxis=dict(title=None,
                                                   showgrid=False,
                                                   showticklabels=True))
    graph_no.update_yaxes(showline=False,
                          linewidth=0.25,
                          matches=None,
                          linecolor='gray',
                          gridcolor='gray')

    # Graph for pollutant 3 (O3)
    graph_o3 = px.area(dff,
                       x='year',
                       y='O3_annualMean',
                       title='O3 (annual mean) [µg/cm3]',
                       template=template,
                       height=height,
                       width=width,
                       range_y=[
                           df['O3_annualMean'].min(),
                           1.1 * df['O3_annualMean'].max()
                       ]).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(0,0,0,0)',
                                        yaxis=dict(title=None,
                                                   showgrid=True,
                                                   showticklabels=True),
                                        xaxis=dict(title=None,
                                                   showgrid=False,
                                                   showticklabels=True))
    graph_o3.update_yaxes(showline=False,
                          linewidth=0.25,
                          matches=None,
                          linecolor='gray',
                          gridcolor='gray')

    # Graph for pollutant 4 (PM10)
    graph_pm10 = px.area(dff,
                         x='year',
                         y='PM10_annualMean',
                         title='PM10 (annual mean) [µg/cm3]',
                         template=template,
                         height=height,
                         width=width,
                         range_y=[
                             df['PM10_annualMean'].min(),
                             1.1 * df['PM10_annualMean'].max()
                         ]).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                                          paper_bgcolor='rgba(0,0,0,0)',
                                          plot_bgcolor='rgba(0,0,0,0)',
                                          yaxis=dict(title=None,
                                                     showgrid=True,
                                                     showticklabels=True),
                                          xaxis=dict(title=None,
                                                     showgrid=False,
                                                     showticklabels=True))
    graph_pm10.update_yaxes(showline=False,
                            linewidth=0.25,
                            matches=None,
                            linecolor='gray',
                            gridcolor='gray')

    # Graph for pollutant 5 (PM2.5)
    graph_pm25 = px.area(dff,
                         x='year',
                         y='PM2_5_annualMean',
                         title='PM2.5 (annual mean) [µg/cm3]',
                         template=template,
                         height=height,
                         width=width,
                         range_y=[
                             df['PM2_5_annualMean'].min(),
                             1.1 * df['PM2_5_annualMean'].max()
                         ]).update_layout(margin=dict(t=50, r=0, l=0, b=50),
                                          paper_bgcolor='rgba(0,0,0,0)',
                                          plot_bgcolor='rgba(0,0,0,0)',
                                          yaxis=dict(title=None,
                                                     showgrid=True,
                                                     showticklabels=True),
                                          xaxis=dict(title=None,
                                                     showgrid=False,
                                                     showticklabels=True))
    graph_pm25.update_yaxes(showline=False,
                            linewidth=0.25,
                            matches=None,
                            linecolor='gray',
                            gridcolor='gray')

    return [graph_no2, graph_no, graph_o3, graph_pm10, graph_pm25]


# if __name__ == '__main__':
#     app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

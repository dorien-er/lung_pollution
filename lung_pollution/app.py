import plotly.graph_objects as go  # or plotly.express as px
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
import requests
import dash_extensions as de
import time
import viz

viz = viz.Viz()

################################################################################

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

TIMEOUT = 60

server = app.server

app.config.suppress_callback_exceptions = True

############################### DATASETS #######################################


@cache.memoize(timeout=TIMEOUT)
def load_data():
    df = pd.read_csv("./lung_pollution/data/covid_pollution_complete.csv")
    # df = df[[
    #     'county_new', 'year', 'NO2_annualMean', 'NO_annualMean',
    #     'O3_annualMean', 'PM10_annualMean', 'PM2_5_annualMean',
    #     'cases_per_100k', 'deaths_per_100k', 'fully_vaccinated',
    #     'Population_density'
    # ]]
    return df


#df = load_data()


@cache.memoize(timeout=TIMEOUT)
def load_data_google_bucket():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    ### GCP Storage - - - - - - - - - - - - - - - - - - - - - -
    BUCKET_NAME = 'lungpollution-2021-predictonline'
    ##### Data  - - - - - - - - - - - - - - - - - - - - - - - -
    BUCKET_TRAIN_DATA_PATH = 'data/covid_pollution_complete.csv'

    df = pd.read_csv(
        f"gs://{BUCKET_NAME}/{BUCKET_TRAIN_DATA_PATH}",  #nrows=1000
    )
    # df = df[[
    #     'county_new', 'year', 'NO2_annualMean', 'NO_annualMean',
    #     'O3_annualMean', 'PM10_annualMean', 'PM2_5_annualMean',
    #     'cases_per_100k', 'deaths_per_100k', 'fully_vaccinated',
    #     'Population_density'
    # ]]
    return df


df = load_data_google_bucket()

@cache.memoize(timeout=TIMEOUT)
def load_geojson():
    with urlopen(
            'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/4_niedrig.geo.json'
    ) as response:
        counties = json.load(response)
    return counties


counties = load_geojson()

############################### IMAGES, GLOBAL VARIABLES #######################

image_filename = 'data/images/intro.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename_2 = 'data/images/under-the-hood.png'  # replace with your own image
encoded_image_2 = base64.b64encode(open(image_filename_2, 'rb').read())

image_filename_3 = 'data/images/kde.png'  # replace with your own image
encoded_image_3 = base64.b64encode(open(image_filename_3, 'rb').read())

#image_filename_4 = 'data/images/gauge.png'  # replace with your own image
#encoded_image_4 = base64.b64encode(open(image_filename_4, 'rb').read())

# -------------------------- LOTTIE GIFs LOADING FUNCTIONS ---------------------------- #
# Lotties: Emil at https://github.com/thedirtyfew/dash-extensions
url1 = "https://assets7.lottiefiles.com/private_files/lf30_kcwpiswk.json"
url2 = "https://assets10.lottiefiles.com/packages/lf20_wt7bupjp.json"
url3 = "https://assets1.lottiefiles.com/packages/lf20_i7y3y8fi.json"
url4 = "https://assets3.lottiefiles.com/packages/lf20_5szujujo.json"
url5 = "https://assets10.lottiefiles.com/packages/lf20_9gmlwgi8.json"
url6 = "https://assets8.lottiefiles.com/packages/lf20_EyJRUV.json"
url404 = "https://assets9.lottiefiles.com/packages/lf20_hqstn5mm.json"

options_lottie = dict(loop=True,
               autoplay=True,
               rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# pollutants = [
#     'NO_annualMean', 'NO2_annualMean', 'O3_annualMean', 'PM2_5_annualMean'
# ]
# covids = ['cases_per_100k', 'deaths_per_100k']

#token = open('./lung_pollution/data/.mapbox_token').read()

################################ SIDEBAR SETTING ###############################

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#D9F6FC",  #BFEAF2
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
                    "Behind the Scenes", href="/page-3", active="exact"),
            ],
            vertical=False,
            pills=True,
        ),
        # dbc.Nav(
        #     [
        #         html.Hr(),
        #         html.P("Who are we?", className="lead"),
        #         dbc.NavLink("Sara Iside Broggini", url="https://www.linkedin.com/in/sara-iside-broggini/", active="exact"),
        #         dbc.NavLink("Ana Luiza Curi Christianini",
        #                     href="/page-1",
        #                     active="exact"),
        #         dbc.NavLink("Rifqi Farhan", href="/page-2", active="exact"),
        #         dbc.NavLink(
        #             "Dorien Roosen", href="/page-3", active="exact"),
        #     ],
        #     vertical=False,
        #     pills=True,
        # ),
        html.Hr(),
        html.P("Who are we?", className="lead"),
        #html.P("Sara Iside Broggini", className="lead-1"),
        html.A("Sara Iside Broggini",
               href='https://www.linkedin.com/in/sara-iside-broggini/',
               target="_blank",
               style={
                   "color": "black",
                   "text-decoration": "none"
               }),
        html.Br(),
        html.Br(),
        html.
        A("Ana Luiza Curi Christianini",
          href=
          'https://www.linkedin.com/in/ana-luiza-curi-christianini-92666b29/',
          target="_blank",
          style={
              "color": "black",
              "text-decoration": "none"
          }),
        html.Br(),
        html.Br(),
        html.A("Rifqi Farhan",
               href='https://www.linkedin.com/in/rifqi-farhan/',
               target="_blank",
               style={
                   "color": "black",
                   "text-decoration": "none"
               }),
        html.Br(),
        html.Br(),
        html.A("Dorien Roosen",
               href='https://www.linkedin.com/in/dorien-roosen/',
               target="_blank",
               style={
                   "color": "black",
                   "text-decoration": "none"
               }),
        #html.P("Ana Luiza Curi Christianini", className="lead-1"),
        #html.P("Rifqi Farhan", className="lead-1"),
        #html.P("Dorien Roosen", className="lead-1"),
        de.Lottie(options=options_lottie, width="80%", height="80%", url=url5),
    ],
    style=SIDEBAR_STYLE,
)
#################################################################################

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

#design layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")],
              prevent_initial_call=True)
#@cache.memoize(timeout=TIMEOUT)
def render_page_content(pathname):
    if pathname == "/":
        return [
            dbc.Row([
                dbc.Col([
                    html.H1('Lung Pollution', style={'textAlign': 'left'}),
                    html.P("Welcome to our Data Science Project ",
                           className="lead"),
                ],
                        width=4),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Img(src='data:image/png;base64,{}'.format( #loading images, connected to top
                        encoded_image.decode()),
                             width=1024,
                             height=585),
                ],
                        width=8),
            ])
        ]

    elif pathname == "/page-1":
        return [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div([
                                    html.H1(
                                        "Air Pollution & CoViD-19 in Germany",
                                        #className='display-3',
                                        style={'textAlign': 'left'}),
                                    html.P(
                                        'Impact of air pollution on CoViD-19',
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
                                    'label': 'NO',
                                    'value': 'NO_totMean'
                                }, {
                                    'label': 'NO2',
                                    'value': 'NO2_totMean'
                                }, {
                                    'label': 'O3',
                                    'value': 'O3_totMean'
                                }, {
                                    'label': 'PM2.5',
                                    'value': 'PM2_5_totMean'
                                }],
                                value='PM2_5_totMean',
                                labelStyle={'display': 'inline-block'},
                                inputStyle={"margin-left": "20px"}),
                            dcc.Graph(id="choropleth_pollutant", #placeholder with an id (copy)
                                      config={
        'displayModeBar': False
        })
                        ]),
                                width=6),
                        dbc.Col(html.Div([
                            html.P("CoViD-19 (since the pandemic started):"),
                            dcc.RadioItems(
                                id='covid',
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
                            dcc.Graph(id="choropleth_covid", config={
        'displayModeBar': False
        })
                        ]),
                                width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([], width=4),
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
                                width=4),
                        dbc.Col([], width=4),
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

    elif pathname == "/page-3":
        return [
            dbc.Col([
                html.H1('Behind the Scenes', style={'textAlign': 'left'}),
                html.Br(),
                html.Img(src='data:image/png;base64,{}'.format(
                    encoded_image_2.decode()),
                         width=1200,
                         height=672)
            ],
                    width=12)
        ]

    elif pathname == "/page-2":
        return [
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H1('CoViD-19 Predictor',
                                style={'textAlign': 'left'}),
                        html.P("It's time to make a prediction!",
                               className="lead"),
                    ],
                            width=12),
                ]),
                dbc.Row([
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        de.Lottie(options=options_lottie,
                                                  width="32%",
                                                  height="32%",
                                                  url=url1)),
                                    html.Br(),
                                    dbc.CardBody([
                                        html.
                                        I("PM2.5 [µg/cm3] (Target in 2030: 5)"
                                          ),
                                        html.Br(),
                                        dcc.Input(
                                            id='input1',
                                            placeholder='Enter a value...',
                                            type='number',
                                            value='16.65255207',
                                            style={'marginRight': '10px'}),
                                        html.Br(),
                                        html.Br(),
                                        html.I(
                                            "O3 [µg/cm3] Target in 2030: 40"),
                                        html.Br(),
                                        dcc.Input(
                                            id='input2',
                                            placeholder='Enter a value...',
                                            type='number',
                                            value='49.340399',
                                            style={'marginRight': '10px'}),
                                        html.Br(),
                                        html.Br(),
                                        html.
                                        I("NO2 [µg/cm3] (Target in 2030: 10)"),
                                        html.Br(),
                                        dcc.Input(
                                            id='input3',
                                            placeholder='Enter a value...',
                                            type='number',
                                            value='20.026733',
                                            style={'marginRight': '10px'}),
                                        html.Br(),
                                        html.Br(),
                                        html.
                                        I("NO [µg/cm3] (Target in 2030: 10)"),
                                        html.Br(),
                                        dcc.Input(
                                            id='input4',
                                            placeholder='Enter a value...',
                                            type='number',
                                            value='20.7315438',
                                            style={'marginRight': '10px'}),
                                        html.Br(),
                                        html.Br(),
                                    ],
                                                 style={'textAlign': 'center'
                                                        }),
                                ],
                                color=
                                "success",  # https://bootswatch.com/default/ for more card colors
                                inverse=
                                True,  # change color of text (black or white)
                                outline=
                                False,  # True = remove the block colors from the background and header
                                className="mt-3"),
                            dbc.Card(
                                [
                                    dbc.CardBody([
                                        html.I("Vaccination Rate"),
                                        html.Br(),
                                        dcc.Input(
                                            id='input6',
                                            placeholder='Enter a value...',
                                            type='number',
                                            value='0.688',
                                            style={'marginRight': '10px'}),
                                        html.Br(),
                                    ],
                                                 style={'textAlign': 'center'
                                                        }),
                                ],
                                color=
                                "info",  # https://bootswatch.com/default/ for more card colors
                                inverse=
                                True,  # change color of text (black or white)
                                outline=
                                False,  # True = remove the block colors from the background and header
                                className="mt-3"),
                            dbc.Card(
                                [
                                    dbc.CardBody([
                                        html.I(
                                            "Population Density [people/km2]"),
                                        html.Br(),
                                        dcc.Input(
                                            id='input5',
                                            placeholder='Enter a value...',
                                            type='number',
                                            value='290.00534',
                                            style={'marginRight': '10px'}),
                                        html.Br(),
                                    ],
                                                 style={'textAlign': 'center'
                                                        }),
                                ],
                                color=
                                "#f79952",  # https://bootswatch.com/default/ for more card colors
                                inverse=
                                True,  # change color of text (black or white)
                                outline=
                                False,  # True = remove the block colors from the background and header
                                className="mt-3"),
                        ],
                        width=4),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        de.Lottie(options=options_lottie,
                                                  width="20%",
                                                  height="5%",
                                                  url=url2)),
                                    dbc.CardBody(
                                        [
                                            html.I("Number of cases per 100k"),
                                            # html.Br(),
                                            # html.H1(' ',
                                            #         style={'textAlign': 'left'}),
                                            # html.Div(id="number-out",
                                            #          style={'fontSize': 60}),
                                            dcc.Graph(id="num_cases",
                                                      config={
                                                          'displayModeBar':
                                                          False
                                                      })
                                        ],
                                        style={
                                            'textAlign': 'center',
                                        }),
                                ],
                                color=
                                "#296073",  # https://bootswatch.com/default/ for more card colors
                                inverse=
                                True,  # change color of text (black or white)
                                outline=
                                False,  # True = remove the block colors from the background and header
                                className="mt-3"),
                            #html.H1('Under the Hood', style={'textAlign': 'left'}),
                            html.Br(),
                            html.Img(src='data:image/png;base64,{}'.format(
                                encoded_image_3.decode()),
                                     width=660,
                                     height=320),
                            html.P("Different Scenarios of CoViD-19 Cases",
                                   className="lead",
                                   style={'textAlign': 'center'}),
                        ],
                        width=6),
                ]),
                dbc.Row([
                    dbc.Col([], width=3),
                ]),
            ])
        ]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Row([
        dbc.Col([
            de.Lottie(options=options_lottie,
                      width="100%",
                      height="100%",
                      url=url404)
        ], width=12)
    ])

########################### Inputs ###########################################
@app.callback(
    #Output("number-out", "children"),
    Output("num_cases", "figure"),
    Input("input1", "value"),
    Input("input2", "value"),
    Input("input3", "value"),
    Input("input4", "value"),
    Input("input5", "value"),
    Input("input6", "value"),)
def number_render(PM2_5, O3, NO2, NO, density, vax):
    if NO == None or NO2 == None or O3 == None or PM2_5 == None or density == None or vax == None:
        time.sleep(10)

    else:
        NO =float(NO)
        NO2 = float(NO2)
        O3 = float(O3)
        PM2_5 = float(PM2_5)
        density = float(density)
        vax = float(vax)
        url = 'https://lung-pollution-mkutgm5w2a-ew.a.run.app/predict'

        params = dict(NO=NO, NO2=NO2, PM2_5=PM2_5, O3=O3, vax=vax, density=density)

        response = requests.get(url, params=params)

        prediction = response.json()

        pred = int(prediction['prediction'])

    fig = go.Figure(
        go.Indicator(mode="number+delta",
                     value=pred,
                     number={
                         'prefix': "",
                         "font": {
                             "size": 50
                         }
                     },
                     delta={
                         'position': "bottom",
                         'reference': 5803,
                         'increasing': {
                             "color": "red"
                         },
                         'decreasing': {
                             "color": "#4CCF3E"
                         },
                     },
                     domain={
                         "x": [0, 1],
                         "y": [0, 1]
                     }))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "white"},
        height=100,
    )
    return fig

####### pollution and covid visualizations
###pollution map germany
@app.callback(Output("choropleth_pollutant", "figure"),
              [Input("pollutant", "value")])
#@cache.memoize(timeout=TIMEOUT)
def make_map_pollutant(pollutants):
    fig_pollutant = viz.pollutant_map(pollutants)
    return fig_pollutant

###covid map germany
@app.callback(Output("choropleth_covid", "figure"), [Input("covid", "value")])
#@cache.memoize(timeout=TIMEOUT)
def make_map_covid(covids):
    fig_covid = viz.covid_map(covids)
    return fig_covid

###pollution per county
@app.callback([
    Output(component_id='graph_no2', component_property='figure'),
    Output(component_id='graph_no', component_property='figure'),
    Output(component_id='graph_o3', component_property='figure'),
    Output(component_id='graph_pm10', component_property='figure'),
    Output(component_id='graph_pm25', component_property='figure'),
], [Input(component_id='county-searchbox', component_property='value')])
#@cache.memoize(timeout=TIMEOUT)
def county_pollutant(county_selected):
    pollutant_county_fig = viz.update_graph(county_selected)
    return pollutant_county_fig

# if __name__ == '__main__':
#     app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8070, debug=True)

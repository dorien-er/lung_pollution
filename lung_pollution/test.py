# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8080/ in your web browser.

import dash                                     # pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import requests
import pandas as pd
from pandas.io.json import json_normalize
import json


import folium
import geopandas as gpd
#import pandas_datareader.data as web
#from scripts import get_card_content

import numpy as np
import plotly.graph_objects as go

from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import calendar
import datetime
from plotly.subplots import make_subplots
#from wordcloud import WordCloud          # pip install wordcloud

# Lottie by Emil - https://github.com/thedirtyfew/dash-extensions
url_coonections = "https://assets9.lottiefiles.com/packages/lf20_svy4ivvy.json"
url_companies = "https://assets1.lottiefiles.com/packages/lf20_wvpdxivl.json"
url_msg_in = "https://assets1.lottiefiles.com/packages/lf20_ZXgMbf.json"
url_msg_out = "https://assets9.lottiefiles.com/packages/lf20_yvrh9cry.json"
url_reactions = "https://assets5.lottiefiles.com/private_files/lf30_y94njU.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

# -------------------------- PYTHON FUNCTIONS ---------------------------- #

def load_data(data_file=None):
        '''0.0.1  Create a function to load the dataset which was extracted from the Data Warehouse'''
        return pd.read_csv(data_file)

def load__class_data(data_file=None):
        '''0.0.1  Create a function to load the dataset which was extracted from the Data Warehouse'''
        return pd.read_csv(data_file)

def load_world_lon_lat_data():
    url = 'https://gist.githubusercontent.com/erdem/8c7d26765831d0f9a8c62f02782ae00d/raw/248037cd701af0a4957cce340dabb0fd04e38f4c/countries.json'
    d = pd.read_json(url)
    d = d[['latlng', 'name']]
    d.rename(columns = {'name':'Country'}, inplace = True)

    return d

def get_df_country_metrics(dfObj=None, country=None, theme=None):
        '''0.0.3  Create a function which takes the dataset, a country, and a theme and returns only the data for that
        specific input and writes the metrics/features into columns (from long to wide format)'''
        dfObj = dfObj[ (dfObj['Country'] == country) & (df['Theme'] == theme) ]
        dfObj = dfObj.pivot_table(index='Year',
                    columns='Metric',
                    values='Value')#.reset_index(drop=True)
        dfObj.columns = [str(col) for col in dfObj.columns]
        #dfObj.style.highlight_null('red')
        #st.dataframe(dfObj.style.applymap(lambda cell: 'color:red' if pd.isnull(cell) else ''))
        #print(dfObj.style.applymap(lambda cell: 'color:red' if pd.isnull(cell) else ''))
        return dfObj

def plot_bar(dfObj=None, theme=None, sumcheck_var=None):
    '''Function to plot stacked bar charts, which are used to see if individual metrics components
    add up to the total amount provided. The total amount is overlaid with a line graph. For example,
    the sum of female and male injured persons should equal the total amount of injured persons.'''
    #print(f"features: {dfObj.columns}")
    sumcheck_dict = sumcheck_var
    flag = 0
    sub_list = sumcheck_dict.get(theme)
    #print(f"Sublist for theme {theme}: {sub_list}")


    if sub_list is not None:
        fig = make_subplots(rows=1, cols=len(sumcheck_dict.get(theme)), start_cell="bottom-left")
        for i in range(len(sub_list)):
            sub_list2 = sub_list[i]
            test_list = dfObj.columns
            #print(f"Testlist: {test_list}")
            #print(f"Sublist: {sub_list2}")

            if (set(sub_list2).issubset(set(test_list))):
                flag = 1
                data = []
                for j in range(len(sumcheck_dict.get(theme)[i])-1):
                    #print(f"subplot col {j}")
                    #print(sumcheck_dict.get(theme)[i][j])
                    data.append(go.Bar(name = sumcheck_dict.get(theme)[i][j], x=dfObj.index, y=dfObj[sumcheck_dict.get(theme)[i][j]]))

                    #for name in range(len(sumcheck_dict.get(theme))):
                    #st.write(data)
                    fig.add_trace(go.Bar(name = sumcheck_dict.get(theme)[i][j], x=dfObj.index, y=dfObj[sumcheck_dict.get(theme)[i][j]]),
                                    row=1, col=i+1)
                    # Change the bar mode
                    fig.update_layout(barmode='stack')
                    fig.add_trace(go.Scatter(
                        x = dfObj.index,
                        y = dfObj[sumcheck_dict.get(theme)[i][-1]],
                        name = sumcheck_dict.get(theme)[i][-1],
                        connectgaps=True),
                        row=1,
                        col=i+1
                        )
        return fig
    else:
    #print("Nothing to plot. I continue to next subplot.")
    #st.plotly_chart(fig, use_container_width=True)
        print("")
    # printing result
    if (flag) :
        print("")
    else :
        print("")

def get_a_countrys_latest_MetricData(dfObj=None, country='France', metric='Road Network Density'):
    dfObj = dfObj[ (dfObj['Country'] == country) & (df['Metric'] == metric) ]
    latest_year = np.max(dfObj["Year"])
    dfObj = dfObj[dfObj["Year"].isin([latest_year])].reset_index(drop=True)
    metric = dfObj['Metric'][0]
    value = np.around(dfObj['Value'][0], decimals=2, out=None)
    unit = dfObj['Unit'][0]
    return metric, latest_year, value, unit


def update_text_paved_network_ratio(country_slctd='France', metric='Paved Network Ratio'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    #print(dfObj)
    start_year = dfObj["Year"][0]
    end_year = np.max(dfObj["Year"])

    earliest_value = dfObj["Value"][0]
    latest_value = dfObj["Value"][len(dfObj.index)-1]
    diff_value = latest_value - earliest_value
    if diff_value > 0:
        trend = 'an increase'
    else:
        trend = 'a decrease'

    #print(dfObj["Value"][len(dfObj.index)-1])
    return f"Between {start_year} and {end_year}, {country_slctd} shows {trend} of {diff_value} % in its {metric}."




# -------------------------- LOAD DATA ----------------------------
df_class = load_data(data_file='./data/CLASS.csv')
#print(df_class.sample(n=10))

df = load_data(data_file='./data/WRS Data 2000-2019.csv')
#print(df.sample(n=10))
#print(f"<<<<<< Shape: {df.shape}")

df = df.merge(df_class, how='left', on='Country')
#print(df.sample(n=10))
#print(f"<<<<<< Shape: {df.shape}")
#print(f"------------- Shape: {df.shape}")
#print(f"- - - - -  {df.columns}")
#print(df["Region"].unique())

#['world', 'usa', 'europe', 'asia', 'africa', 'north america', 'south america']
rename_dict = {'Sub-Saharan Africa': 'africa',
               'Middle East & North Africa': 'asia',
               'Latin America & Caribbean': 'south america',
               'North America': 'north america',
               'South Asia': 'asia',
               'Europe & Central Asia': 'world',
               'East Asia & Pacific': 'world'}
df.replace({"Region": rename_dict}, inplace=True)
print(df["Region"].unique())

geo_df = load_world_lon_lat_data()
df = df.merge(geo_df, how='left', on='Country')
print(df.sample())
print(df.columns)

# -------------------------- CARD CONTENT
card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

card_content_road_network_left = [
    dbc.CardHeader(id='header_value_left', children='000'),
    dbc.CardBody(
        [
            html.H5(id="body_value_left", children="000"),
            dcc.Graph(id='graph-left', figure={}, config={'displayModeBar':False}),
        ]
    ),
]

card_content_road_network_middle = [
    dbc.CardHeader(id='header_value_middle', children='000'),
    dbc.CardBody(
        [
            html.H5(id="body_value_middle", children="000"),
            dcc.Graph(id='graph-middle', figure={}, config={'displayModeBar':False}),
        ]
    ),
]

card_content_road_network_right = [
    dbc.CardHeader(id='header_value_right', children='000'),
    dbc.CardBody([
        dbc.Row([
            html.H5(id="body_value_right", children="000"),
        ]),
        dbc.Col([
            dcc.Graph(id='graph-right', figure={}, config={'displayModeBar':False}),
        ], width=12),
    ]),
]

card_content_road_network = [
    dbc.CardHeader(id='test', children=''),
    dbc.CardBody(
        [
            html.H5("Analysis", className="card-title"),
            html.P(
                '''Since 2008, Turkey shows a constant and very high degree of paved network ratio.
                More than 92% of Turkey's road network is paved, according to the data provided.''',
                className="card-text",
            ),
            html.P(
                '''In 2019, slightly more than 92.17 % was paved, which in an increase of 3927 km in total numbers compared to 2018.''',
                className="card-text",
            ),
        ]
    ),
]

card_content_road_network_detail = [
    dbc.CardHeader(id='test_detailed', children=''),
    dbc.CardBody(
        [
            html.H5("Analysis", className="card-title"),
            html.P(
                '''Until 2013, the total road network in Turkey was slightly increasing, with an average value around 360,000 km.
                Since then, the total road network has declined, but is still constant. The average after 2013 is in the range of 245,000 km.''',
                className="card-text",
            ),
            html.P(
                '''The reason for this decline might be due to changes in the measurement of that metric. If we look at the individual
                contributions, e.g. the length of main or national roads, and secondary or regional roads, we ca see that those
                values have been from the year 2000 till 2019 constant in the case of main or national roads. Here, the average value is
                in the the range of 31,000 km. If we look at the evolution of the length of the secondary or regional road network length,
                we see that it was was slightly increasing over time, from around 30,000 km in 2000 to approximately 34,000 km in 2019.''',
                className="card-text",
            ),
        ]
    ),
]
# -------------------------- DASH ---------------------------- #

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.config.suppress_callback_exceptions = True




# -------------------------- PROJECT DASHBOARD ---------------------------- #

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Jumbotron([html.H1("IRF Data Warehouse Country Explorer", className="display-3"),
                        html.P(
                            "The easy way to see a countries' development over time for several indicators, its comparison to different countries, or income groups, in an interactive App.",
                            className="lead",
                        ),
                        html.P("", className="font-italic"),
                ]), width=10),
    ], className='mb-4 mt-2'),

    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col([
            html.H2("", style={'textAlign':'center'}),
            dcc.Dropdown(id='my-country-searchbox', multi=False, value='Turkey', options=[{'label': x, 'value':x} for x in sorted(df["Country"].unique())]),
        ], width=4),
        dbc.Col([], width=3),
    ], className='mb-3 mt-2'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Road Network Density 2019'),
                    html.H2(id='content-connections', children="000"),
                    html.H6(id='content-connections_unit', children='unit')
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="70%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Persons Killed Rate 2019'),
                    html.H2(id='content-companies', children="000"),
                    html.H6(id='content-companies_unit', children='unit')
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="42%", height="15%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Total Vehicles in Use Rate by Population 2019'),
                    html.H2(id='content-msg-in', children="000"),
                    html.H6(id='content-msg-in_unit', children='unit')
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="37%", height="40%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Total Vehicles in Use Rate by Network 2019'),
                    html.H2(id='content-msg-out', children="000"),
                    html.H6(id='content-msg-out_unit', children='unit')
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="40%", height="40%", url=url_reactions)),
                dbc.CardBody([
                    html.H6('Motorway Highway Ratio 2019'),
                    html.H2(id='content-reactions', children="000"),
                    html.H6(id='content-reactions_unit', children='unit')
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ], className='mb-2 mt-2'),

    dbc.Row([
        dbc.Col([], width=2),
        dbc.Col([
            dcc.Graph(id='my-map_folium', figure={}),
            dcc.Dropdown(id='my-map-searchbox', multi=False, value='Road Network Density', options=[{'label': x, 'value':x} for x in sorted(['Road Network Density', 'Persons Killed Rate', 'Total Vehicles In Use Rate by Population', 'Total Vehicles In Use Rate by Network', 'Motorway Highway Ratio'])]),
        ], width=6),
        dbc.Col([], width=2)
    ], className='mb-3 mt-2'),







   dbc.Row([
       dbc.Col([
            dbc.Jumbotron([
                html.H1("Road Network", className="display-3"),
                dbc.Row([
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Card(
                                        [

                                            dbc.CardHeader([html.H6("Global Paved Network Distribution")]),
                                            dbc.CardBody([
                                                dcc.Graph(id='my-map-small', figure={}, config={'displayModeBar':False})
                                            ])

                                        ], color="light", inverse=False), width=2),



                                    dbc.Col(dbc.Card(
                                        [
                                                dbc.CardHeader([html.H6("Paved Network 2019"), html.P("% of total roads")]),
                                                dbc.CardBody([

                                                    html.H2(id='content-paved-network', children="000"),
                                                    html.P(id='detailed-paved-network', children='100')

                                                ], style={'textAlign':'left'})

                                        ], color="light", inverse=False
                                        ),
                                    width=2),
                                    dbc.Col(dbc.Card(
                                        [
                                                dbc.CardHeader([html.H6("Paved Network 2019"), html.P("% of total roads")]),
                                                dbc.CardBody(
                                                    dcc.Graph(id='yearly-line-chart', figure={}, config={'displayModeBar':False}                                                                               )
                                                )
                                        ], color="light", inverse=False
                                        ),
                                    width=2),
                                    dbc.Col(dbc.Card(card_content_road_network, color="light", inverse=False), width=6),
                                ],
                                className="mb-4",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Card(card_content_road_network_left, color="light", inverse=False), width=2),
                                    dbc.Col(dbc.Card(card_content_road_network_middle, color="light", inverse=False), width=2),
                                    dbc.Col(dbc.Card(card_content_road_network_right, color="light", inverse=False), width=2),
                                    dbc.Col(dbc.Card(card_content_road_network_detail, color="light", inverse=False), width=6),
                                ]
                            ),
                        ]
                    ),
                ], className='mb-3 mt-2'),
            ]),
        ], width=12),
    ], className='mb-3 mt-3', no_gutters=True), #justify  Horizontal:start,center,end,between,around),

        dbc.Row([
            dbc.Col([
                dbc.Jumbotron([
                    html.H1("Road Accidents", className="display-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardImg(
                                    src=None,#"/assets/blue_dot.png",
                                    top=True,
                                    style={"width": "2rem"},
                                    className="ml-3 mt-3"),
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.P("Injury accidents per 100,000 population", className="ml-3")
                                        ], width={'size':10, 'offset':1}),

                                        dbc.Col([
                                            dcc.Graph(id='yearly-bar_final', figure={},
                                                    config={'displayModeBar':False},
                                                    )
                                        ], width={'size':10,'offset':1}),


                                    ]),
                                ])
                            ], style={"width": "24rem"},
                            className="mt-3"
                            ),
                        ], width=2),
                        dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(
                                        src=None,#"/assets/blue_dot.png",
                                        top=True,
                                        style={"width": "2rem"},
                                        className="ml-3 mt-3"),
                                    dbc.CardBody([
                                        dbc.Row([
                                            dbc.Col([
                                                html.P("Persons Killed in Road Accidents", className="ml-3")
                                            ], width={'size':10, 'offset':1}),

                                            dbc.Col([
                                                #dcc.Graph(id='yearly-donut_final_1', figure={},
                                                #        config={'displayModeBar':False},
                                                #        )
                                            ], width={'size':10,'offset':1}),


                                        ]),
                                ]),
                                dcc.Graph(id='yearly-donut_final_1', figure={},
                                                    config={'displayModeBar':False},
                                                    )
                            ], style={"width": "24rem"},
                            className="mt-3"
                            ),
                        ], width=2),
                        dbc.Col([
                            html.P(
                                update_text_paved_network_ratio(country_slctd='Turkey', metric='Paved Network Ratio'),
                                className="lead",
                            ),
                        ], width=4),
                    ]),

                ])
            ])
        ], no_gutters=False), #justify  Horizontal:start,center,end,between,around),),

        dbc.Row([
            dbc.Col([
                dbc.Jumbotron([
                    html.H1("Vehicles In Use", className="display-3"),

                    dbc.Col([
                        html.P(
                            update_text_paved_network_ratio(country_slctd='Turkey', metric='Paved Network Ratio'),
                            className="lead",
                        ),
                    ]),
                    dcc.Graph(id='yearly-heatmap_final_1', figure={},
                                                    config={'displayModeBar':False},
                    ),
                    html.H1(children='Hello Dash'),
                    html.Div(children='''
                        Dash: A web application framework for Python.
                    '''
                    ),
                ])
            ])
        ], no_gutters=False), #justify  Horizontal:start,center,end,between,around),),





        html.Div([
        dcc.Markdown('''
            #### Dash and Markdown
            Dash supports [Markdown](http://commonmark.org/help).
            Markdown is a simple way to write and format text.
            It includes a syntax for things like **bold text** and *italics*,
            [links](http://commonmark.org/help), inline `code` snippets, lists,
            quotes, and more.
            ''')
    ]),

], fluid=True)



# Updating the 5 number cards
@app.callback(
    Output('content-connections','children'),
    Output('content-connections_unit','children'),
    Output('content-companies','children'),
    Output('content-companies_unit','children'),
    Output('content-msg-in','children'),
    Output('content-msg-in_unit','children'),
    Output('content-msg-out','children'),
    Output('content-msg-out_unit','children'),
    Output('content-reactions','children'),
    Output('content-reactions_unit','children'),
    Input('my-country-searchbox','value'),
)
def update_small_cards(country_slctd):

    # Road Network Density
    (metric, latest_year, conctns_num, unit_rnd) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Road Network Density')
    print(f"Road Network Density: {conctns_num}")

    # Persons Killed Rate
    (metric, latest_year, compns_num, unit_pkr) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Persons Killed Rate')
    print(f"Persons Killed Rate: {compns_num}")

    # TOTAL VEHICLES IN USE BY POPULATION
    (metric, latest_year, in_num, unit_tvp) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Total Vehicles In Use Rate by Population')
    print(f"Total Vehicles in Use Rate by Population: {in_num}")

    # TOTAL VEHICLES IN USE BY NETWORK
    (metric, latest_year, out_num, unit_tvn) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Total Vehicles In Use Rate by Network')
    print(f"Total Vehicles in Use Rate by Network: {out_num}")

    # Motorway Highway Ratio
    (metric, latest_year, reactns_num, unit_mhr) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Motorway Highway Ratio')
    print(f"Motorway Highway Ratio: {reactns_num}")

    return conctns_num, unit_rnd, compns_num, unit_pkr, in_num, unit_tvp, out_num, unit_tvn, reactns_num, unit_mhr


# Updating the 5 number cards
@app.callback(
    Output('content-paved-network','children'),
    Output('detailed-paved-network', 'children'),
    Input('my-country-searchbox','value'),
)
def update_road_network_cards(country_slctd):
    print(f"You selected: {country_slctd}")
    X = df[df["Country"].isin([country_slctd]) & df["Year"].isin([2018, 2019]) & df["Metric"].isin(['Paved Network Ratio', 'Total Paved Road Network'])]
    print(X.tail())
    X = X[['Country', 'Year', 'Metric', 'Value', 'Unit']]
    print("Matrix X:")
    print(X.tail())
    X_red = X[X["Metric"].isin(['Total Paved Road Network'])]
    print("Matrix X_red:")
    print(X_red.tail())
    total_change_km_paved_roads_2018_2019 = X_red[["Value"]].diff(1).reset_index(drop=True)
    total_change_km_paved_roads_2018_2019 = total_change_km_paved_roads_2018_2019["Value"][1]
    print(total_change_km_paved_roads_2018_2019)

    # Paved Road Network
    (metric, latest_year, conctns_num, unit_rnd) = get_a_countrys_latest_MetricData(dfObj=df, country=country_slctd, metric='Paved Network Ratio')
    if conctns_num > 0:
        trend='more'
    else:
        trend='less'
    conctns_num = f"{conctns_num}%"
    total_change_km_paved_roads_2018_2019 = f"{total_change_km_paved_roads_2018_2019} km {trend} compared to 2018"
    return conctns_num, total_change_km_paved_roads_2018_2019

@app.callback(
    Output('header_value_left', 'children'),
    Output('header_value_middle', 'children'),
    Output('header_value_right', 'children'),
    Output('body_value_left', 'children'),
    Output('body_value_middle', 'children'),
    Output('body_value_right', 'children'),
    Input('my-country-searchbox','value')
)
def update_road_network_cards2(country_slctd):
    X = df[df["Country"].isin([country_slctd]) & df["Year"].isin([2019]) & df["Metric"].isin(['Total Road Network', 'Main or National Roads', 'Secondary or Regional Roads'])]
    X = X[['Country', 'Year', 'Metric', 'Value', 'Unit']]
    left_body = X[X['Metric'].isin(['Total Road Network'])]['Value']
    middle_body = X[X['Metric'].isin(['Main or National Roads'])]['Value']
    right_body = X[X['Metric'].isin(['Secondary or Regional Roads'])]['Value']
    left_header = X[X['Metric'].isin(['Total Road Network'])]['Metric']
    middle_header = X[X['Metric'].isin(['Main or National Roads'])]['Metric']
    right_header = X[X['Metric'].isin(['Secondary or Regional Roads'])]['Metric']
    return left_header, middle_header, right_header, left_body, middle_body, right_body

@app.callback(
    Output('graph-left', 'figure'),
    Output('graph-middle', 'figure'),
    Output('graph-right', 'figure'),
    Input('my-country-searchbox','value')
)
def update_road_network_small_graphs(country_slctd):
    X = df[df["Country"].isin([country_slctd]) & df["Metric"].isin(['Total Road Network', 'Main or National Roads', 'Secondary or Regional Roads'])]
    X = X[['Country', 'Year', 'Metric', 'Value', 'Unit']]

    fig_left = px.bar(X[X["Metric"].isin(["Total Road Network"])], x='Year', y='Value',
                      template='seaborn', height=120,
                      range_y=[X['Value'].min(), 1.1*X['Value'].max()]).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                                paper_bgcolor='rgba(0,0,0,0)',
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                yaxis=dict(
                                                    title=None,
                                                    showgrid=True,
                                                    showticklabels=True
                                                    ),
                                                xaxis=dict(
                                                    title=None,
                                                    showgrid=False,
                                                    showticklabels=True
                                                    )
                                                )
    fig_left.update_yaxes(showline=False, linewidth=0.25, linecolor='gray', gridcolor='gray')


    fig_middle = px.bar(X[X["Metric"].isin(["Main or National Roads"])], x='Year', y='Value',
                      template='seaborn', height=120,).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                                paper_bgcolor='rgba(0,0,0,0)',
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                yaxis=dict(
                                                    title=None,
                                                    showgrid=True,
                                                    showticklabels=True
                                                    ),
                                                xaxis=dict(
                                                    title=None,
                                                    showgrid=False,
                                                    showticklabels=True
                                                    )
                                                )
    fig_middle.update_yaxes(showline=False, linewidth=0.25, linecolor='gray', gridcolor='gray')

    fig_right = px.bar(X[X["Metric"].isin(["Secondary or Regional Roads"])], x='Year', y='Value',
                    template='seaborn', height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                                title=None,
                                                showgrid=True,
                                                showticklabels=True
                                                ),
                                            xaxis=dict(
                                                title=None,
                                                showgrid=False,
                                                showticklabels=True
                                                )
                                            )
    fig_right.update_yaxes(showline=False, linewidth=0.25, linecolor='gray', gridcolor='gray')

    return fig_left, fig_middle, fig_right









# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(country_slctd):
    #dff = get_df_country_metrics(dfObj=df, country=country_slctd, theme='Road Traffic')
    dff = df[df['Country'].isin([country_slctd]) & df['Metric'].isin(['Passenger Car Traffic'])]
    figln = px.line(dff, x='Year', y='Value', template='seaborn')
    return figln

@app.callback(
    Output('yearly-line-chart', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd):
    print(country_slctd)
    dff = df[df['Country'].isin([country_slctd]) & df['Metric'].isin(['Paved Network Ratio'])]
    #figln2 = px.line(dff, x='Year', y='Value', template='seaborn')
    res = dff[["Country", "Year", "Metric", "Value", "Unit"]]
    print(res.head())
    fig = px.area(dff, x='Year', y='Value',
                    #title='% paved of total roads',
                    #color='Metric',
                    #range_y=[dff['Value'].min(), 1.1*dff['Value'].max()],
                    range_y=[0, 100],
                    height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                                paper_bgcolor='rgba(0,0,0,0)',
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                yaxis=dict(
                                                    title=None,
                                                    showgrid=True,
                                                    showticklabels=True
                                                    ),
                                                xaxis=dict(
                                                    title=None,
                                                    showgrid=False,
                                                    showticklabels=True
                                                    )
                                                )
    fig.update_yaxes(showline=False, linewidth=0.25, linecolor='gray', gridcolor='gray')
    #fig.update_traces(fill='tozeroy',line={'color':'blue'})
    fig.update_traces(line={'color': 'rgb(77,166,255)'})
    return fig

# Chloropleth Map - small
@app.callback(
    Output('my-map-small', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_small_map(country_slctd):
    metric_ = "Paved Network Ratio"
    dfObj = df[df["Year"].isin([2019]) & df["Metric"].isin([metric_])]
    print(f"<< Country Map Data Selection")
    print(dfObj.head())
    print(f">> Country Map Data Selection")
    coordinates_ = df[df["Country"].isin([country_slctd])].reset_index(drop=True)
    latitude = coordinates_.iloc[0]["latlng"][0]
    longitude = coordinates_.iloc[0]["latlng"][1]
    print(f"Lat: {latitude}")
    print(f"Lon: {longitude}")

    fig = px.choropleth(data_frame = dfObj,
              locations='Country',
              color='Value',
              template = 'ggplot2',
              range_color=[0, np.max(dfObj["Value"])],
              #color_continuous_scale='world',
              #animation_frame='Year',
              locationmode='country names',
              center = {'lat': latitude, 'lon': longitude},
              basemap_visible=False,
              #scope='world',
              height=50,
              width=100,
              #title=f'Global {dfObj["Metric"].unique()[0]} Distribution',
              hover_name = 'Country',
              #labels={‘vax_per_cap’:’Vaxes % of Population’,
               #       ‘week’:’Week’,
               #       ‘state_codes’:’State Code’}
               )

    fig.update_layout(coloraxis_showscale=False)

    return fig

# Chloropleth Map - multiple
@app.callback(
    Output('my-map_folium', 'figure'),
    Input('my-country-searchbox', 'value'),
    Input('my-map-searchbox','value'),
)
def update_map(country_slctd, metric_slctd):
    #print(df.columns)
    #dfObj = df[df["Metric"].isin(['Population', 'Persons Killed Rate']) & df["Year"].isin([2019])]

    #print(dfObj.head())

    #base choropleth map from https://plot.ly/python/mapbox-county-choropleth/
    df1 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                    dtype={"fips": str})
    print(f"SHAPE DF: {df.shape}")
    print(df1.head())
    #generate another feature to map
    df1['unemp2']=24-df1.unemp
    print(f"SHAPE MAP DF: {df1.shape}")
    #print(df.head)
    data=[]
    data.append(go.Choroplethmapbox(geojson='https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json',
                                        locations=df1.fips,
                                        z=df1.unemp,
                                        colorbar=dict(title='Unemployment Year 1'),
                                        colorscale="OrRd"
                                        ))
    data.append(go.Choroplethmapbox(geojson='https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json',
                                        locations=df1.fips,
                                        z=df1.unemp2,
                                        colorbar=dict(title='Unemployment Year 2'),
                                        colorscale="OrRd"
                                        ))
    data[0]['visible']=False
    layout=go.Layout(mapbox_style="carto-positron",
                    mapbox_zoom=3, mapbox_center = {"lat": 37.0902, "lon": -95.7129})
    #dropdown code from https://plot.ly/~empet/15237/choroplethmapbox-with-dropdown-menu/#/
    layout.update(updatemenus=list([
            dict(
                x=-0.05,
                y=1,
                yanchor='top',
                buttons=list([
                    dict(
                        args=['visible', [True, False]],
                        label='Year: 1',
                        method='restyle'
                    ),
                    dict(
                        args=['visible', [False, True]],
                        label='Year: 2',
                        method='restyle')]))]))
    # layout.update(margin={"r":0,"t":0,"l":0,"b":0})
    figo = go.Figure(data=data,layout=layout)


    #-----
    metric = metric_slctd #'Persons Killed Rate'
    data2 = df[df["Metric"].isin([metric])].sort_values(by=['Year', 'Country'])
    print(data2.head())
    gig = px.choropleth(data_frame = data2,
              locations='Country',
              color='Value',
              template = 'ggplot2',
              range_color=[0, np.max(data2["Value"])],
              #color_continuous_scale='world',
              animation_frame='Year',
              locationmode='country names',
              basemap_visible=False,
              scope='world',
              height=600,
              width=1500,
              title=f'Global {data2["Metric"].unique()[0]} Distribution',
              hover_name = 'Country',
              #labels={‘vax_per_cap’:’Vaxes % of Population’,
               #       ‘week’:’Week’,
               #       ‘state_codes’:’State Code’}
               )
    #-----

    return gig


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-mult-countries', 'value')
)
def update_graph(country_slctd):
    dff = df[df['Country'].isin(country_slctd) & df['Metric'].isin(['Passenger Car Traffic'])]
    figln2 = px.line(dff, x='Year', y='Value', color='Country', template='seaborn')
    return figln2


# Connected Scatterplots # Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-mult-countries', 'value')
)
def update_graph(country_slctd):
    dfObj = df[df['Country'].isin(country_slctd)]
    dfObj = dfObj.pivot_table(index=['Country', 'Year'],
                columns=['Metric'],
                values='Value').reset_index(drop=False)
    fighist = px.line(dfObj, x='GDP Growth', y='Population', color="Country", text="Year", template='seaborn')
    fighist.update_traces(textposition="bottom right")
    #dff = dff[dff['Year']=='2019']
    #fighist = px.histogram(dff, x='Metric', y='Close')
    return fighist




# Line Graph for Cards for Road Accidents ---------------------------------------------------------------
theme_metrics = df[df["Theme"].isin(['Road Accidents'])]['Metric'].unique()

for i, metric in zip(range(59), theme_metrics):

#    @app.callback(
#    Output(f'yearly-{metric}', 'figure'),
#    Input('my-country-searchbox', 'value')
#    )

    def update_graph(country_slctd='Finland', metric=metric):
        dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
        fig = px.line(dfObj, x='Year', y='Value',
                    range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                    height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                                paper_bgcolor='rgba(0,0,0,0)',
                                                plot_bgcolor='rgba(0,0,0,0)',
                                                yaxis=dict(
                                                title=None,
                                                showgrid=False,
                                                showticklabels=False
                                                ),
                                                xaxis=dict(
                                                title=None,
                                                showgrid=False,
                                                showticklabels=False
                                                ))

        year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
        year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

        if year_end >= year_start:
            return fig.update_traces(fill='tozeroy',line={'color':'green'})
        elif year_end < year_start:
            return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
Output(f'yearly-{metric}', 'figure'),
Input('my-country-searchbox', 'value')
)
#####################################################################################
# Line Graph for Cards---------------------------------------------------------------
@app.callback(
    Output('yearly-line_final', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='France', metric='Paved Network Ratio'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title='% paved of total roads',
                                               showgrid=False,
                                               showticklabels=True
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})


@app.callback(
    Output('yearly-bar_final', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='France', metric='Injury Accident Rate'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.bar(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ))
    return fig


@app.callback(
    Output('yearly-donut_final_1', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='France', metric=['Male Persons Killed', 'Female Persons Killed']):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin(metric)) & (df['Year'].isin([2019])) ].reset_index(drop=True)
    #print(dfObj)
    labels = dfObj["Metric"].unique()
    #print(labels)
    values = dfObj["Value"]
    #print(values)
    fig = px.pie(labels,
                 values = values,
                 names = labels,
                 hole = 0.4,
                 height=120
                ).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ))
    fig.update_traces(hoverinfo='label+percent',
                   textinfo='percent', textfont_size=10)

    fig.add_annotation(x= 0.5, y = 0.5,
                    #text = f'{dfObj["Year"].unique}',
                    text = '2019',
                    font = dict(size=10,family='Verdana',
                                color='black'),
                    showarrow = False)
    fig.update_layout(showlegend=True)

    return fig

@app.callback(
    Output('yearly-heatmap_final_1', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='France', metric=['Passenger Cars In Use', 'Buses and Motor Coaches In Use', 'Vans and Pickups In Use', 'Lorries and Road Tractors In Use', 'Motorcycles and Mopeds In Use']):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin(metric))].reset_index(drop=True)

    dfObj = dfObj[["Year", "Metric", "Value"]]
    #print(dfObj)
    import seaborn as sns
    flights = sns.load_dataset("flights")
    #print(flights)
    flights = flights.pivot("month", "year", "passengers")
    #fig, ax = sns.heatmap(dfObj, annot=True, fmt="d", cmap="YlGnBu", linewidths=.6)

    fig = go.Figure(data=go.Heatmap(
        z=dfObj["Value"],
        x=dfObj["Year"],
        y=dfObj["Metric"],
        colorscale='bluyl')).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             height=150,
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=True
                                            ))


    return fig

@app.callback(
    Output('yearly-line', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Main or National Roads'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line2', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Motorway Highway Ratio'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line3', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Motorways / Highways'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line4', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Other Roads'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line5', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Paved Network Ratio'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line6', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Road Network Density'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line7', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Secondary or Regional Roads'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line8', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Total Paved Road Network'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

@app.callback(
    Output('yearly-line9', 'figure'),
    Input('my-country-searchbox', 'value')
)
def update_graph(country_slctd='Finland', metric='Total Road Network'):
    dfObj = df[(df['Country'].isin([country_slctd])) & (df['Metric'].isin([metric]))].reset_index(drop=True)
    fig = px.line(dfObj, x='Year', y='Value',
                   range_y=[dfObj['Value'].min(), 1.1*dfObj['Value'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                            paper_bgcolor='rgba(0,0,0,0)',
                                            plot_bgcolor='rgba(0,0,0,0)',
                                            yaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ),
                                            xaxis=dict(
                                               title=None,
                                               showgrid=False,
                                               showticklabels=False
                                            ))

    year_start = dfObj[dfObj['Year'] == dfObj['Year'].min()]['Value'].values[0]
    year_end = dfObj[dfObj['Year'] == dfObj['Year'].max()]['Value'].values[0]

    if year_end >= year_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif year_end < year_start:
        return fig.update_traces(fill='tozeroy', line={'color': 'red'})

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8030, debug=True, use_reloader=True)

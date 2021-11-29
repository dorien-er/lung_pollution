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

############################ LOAD CSV & JSON ##################################

df = pd.read_csv("./lung_pollution/data/covid_pollution_final-rifqi.csv")
#df['id'] = df['id'].astype('string')

# with urlopen(
#         'https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/1_sehr_hoch.geo.json'
# ) as response:
#     counties = json.load(response)

with open("./lung_pollution/data/1_sehr_hoch.geo.json") as response:
    counties = json.load(response)

############################# MAPS ############################################

fig_cases = px.choropleth_mapbox(df,
                                 geojson=counties,
                                 locations='county_new',
                                 featureidkey="properties.NAME_3",
                                 color='cases_per_100k',
                                 color_continuous_scale="Burgyl",
                                 range_color=(0, np.max(df["cases_per_100k"])),
                                 animation_frame='year',
                                 mapbox_style="carto-positron",
                                 zoom=3.5,
                                 center={
                                     "lat": 51.312801,
                                     "lon": 9.481544
                                 },
                                 opacity=0.5,
                                 labels={'cases_per_100k': 'cases per 100k'})
fig_cases.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig_deaths = px.choropleth_mapbox(
    df,
    geojson=counties,
    locations='county_new',
    featureidkey="properties.NAME_3",
    color='deaths_per_100k',
    color_continuous_scale="gray",
    #reversescale=True,    # CHECK IT FOR PX
    range_color=(0, np.max(df["deaths_per_100k"])),
    animation_frame='year',
    mapbox_style="carto-positron",
    zoom=3.5,
    center={
        "lat": 51.312801,
        "lon": 9.481544
    },
    opacity=0.5,
    labels={'deaths_per_100k': 'deaths per 100k'})
fig_deaths.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

###############################################################################

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{
                    'name': 'viewport',
                    'content': 'width=device-width, initial-scale=1.0'
                }])
server = app.server

app.config.suppress_callback_exceptions = True

############################## LAYOUT SETTINGS ################################

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Div([
                html.H1("Lung Pollution",
                        className='display-3',
                        style={'textAlign': 'center'}),
                html.P(
                    'How is climate change affecting our respiratory health?',
                    className='lead',
                    style={'textAlign': 'center'}),
                html.P('', className='font-italic'),
            ]),
                    width=10),
        ],
                className='mb-4 mt-2'),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(figure=fig_cases)), width=5),
            dbc.Col(html.Div(dcc.Graph(figure=fig_deaths)), width=5),
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
                             } for x in sorted(df["county_new"].unique())]),
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
            dbc.Col([], width=2),
            dbc.Col(html.Div(dcc.Graph(id='graph_pm10')), width=4),
            dbc.Col(html.Div(dcc.Graph(id='graph_pm25')), width=4),
            dbc.Col([], width=2),
            #dbc.Col(html.Div(dcc.Graph(id='graph_o3')), width=4),
            #dbc.Col(html.Div(dcc.Graph(figure=graph_pm10)), width=2),
            #dbc.Col(html.Div(dcc.Graph(figure=graph_pm10)), width=2),
        ]),
    ],
    fluid=True)

############################### CALLBACKS ###################################
@app.callback([
    Output(component_id='graph_no2', component_property='figure'),
    Output(component_id='graph_no', component_property='figure'),
    Output(component_id='graph_o3', component_property='figure'),
    Output(component_id='graph_pm10', component_property='figure'),
    Output(component_id='graph_pm25', component_property='figure'),
], [Input(component_id='county-searchbox', component_property='value')])

def update_graph(county_selected):
    #print(county_selected)
    #print(type(county_selected))

    dff = df.copy()
    dff = dff[dff["county_new"] == county_selected]

    #print(dff)

    # Graph for pollutant 1 (NO2)
    graph_no2 = px.area(dff,
                        x='year',
                        y='NO2_annualMean',
                        title='NO2 (annual mean)',
                        template='seaborn',
                        height=280,
                        width=400,
                        range_y=[
                            df['NO2_annualMean'].min(),
                            1.1 * df['NO2_annualMean'].max()
                        ]).update_layout(margin=dict(t=50, r=0, l=0, b=20),
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
                       title='NO (annual mean)',
                       template='seaborn',
                       height=280,
                       width=400,
                       range_y=[
                           df['NO_annualMean'].min(),
                           1.1 * df['NO_annualMean'].max()
                       ]).update_layout(margin=dict(t=50, r=0, l=0, b=20),
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
                       title='O3 (annual mean)',
                       template='seaborn',
                       height=280,
                       width=400,
                       range_y=[
                           df['O3_annualMean'].min(),
                           1.1 * df['O3_annualMean'].max()
                       ]).update_layout(margin=dict(t=50, r=0, l=0, b=20),
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
                         title='PM10 (annual mean)',
                         template='seaborn',
                         height=280,
                         width=400,
                         range_y=[
                             df['PM10_annualMean'].min(),
                             1.1 * df['PM10_annualMean'].max()
                         ]).update_layout(margin=dict(t=50, r=0, l=0, b=20),
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
                         title='PM2.5 (annual mean)',
                         template='seaborn',
                         height=280,
                         width=400,
                         range_y=[
                             df['PM2_5_annualMean'].min(),
                             1.1 * df['PM2_5_annualMean'].max()
                         ]).update_layout(margin=dict(t=50, r=0, l=0, b=20),
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


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8040, debug=True,
                   use_reloader=True)  # Turn off reloader if inside Jupyter

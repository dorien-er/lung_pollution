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
        pass



if __name__ == '__main__':
    viz = DataViz()
    viz.load_data()
    #print(data)
    app = viz.fig_map()
    app.run_server(host='0.0.0.0', port=8070, debug=True, use_reloader=False)

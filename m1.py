import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import time
from dash.dependencies import Input, Output, State

external_stylesheets = [
    dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Modal(
        [
            dbc.ModalHeader("END OF COMPLEX OPERATIONS"),
            dbc.ModalBody("Finally!"),
        ],
        id='end-modal',
        is_open=False,
    ),
    html.Div(id='page-content'),
])

index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
])

page_1_layout = html.Div([
    html.H1('Page 1'),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{
            'label': i,
            'value': i
        } for i in ['LA', 'NYC', 'MTL']],
    ),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


# Complex stuff that takes some time to complete and in the end shows an alert
@app.callback(Output("end-modal",
                     "is_open"), [Input('page-1-dropdown', 'value')],
              [State("end-modal", "is_open")])
def page_1_complex_calculation(value, is_open):
    # time consuming operations represented with some sleep time
    time.sleep(5)
    return True


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(id='page-2-radios',
                   options=[{
                       'label': i,
                       'value': i
                   } for i in ['Orange', 'Blue', 'Red']],
                   value='Orange'),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

page_3_layout = html.Div(['Some more stufff!!!!'])


@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):

    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8040, debug=True, use_reloader=False)

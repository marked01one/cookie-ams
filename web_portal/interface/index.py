from ast import Div
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(className="container", children=[
  html.H1("Asset Management System"),
  html.Div([
    "Input: ",
    dcc.Input(id='my-input', value='intial value', type='text')
  ]),
  html.Br(),
  html.Div(id='my-output')
])


@callback(Output('my-output', 'children'), Input('my-input', 'value'))
def update_output_div(input):
  return f'Output: {input}'


if __name__ == '__main__':
  app.run_server()
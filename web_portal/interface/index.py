from ast import Div
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from services.http_service import ManufacturerService

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
manufacturer = ManufacturerService()

app.layout = html.Div(className="container", children=[
  html.H1("Asset Management System", id='button'),
  html.Ul(id='output-container')
])

@callback(Output('output-container', 'children'), Input("button", "n_clicks"))
def update_output_div(n_clicks):
  
  return [html.Li(m['manufacturer_name'])
    for m in manufacturer.get_manufacturers()['content']
  ]


if __name__ == '__main__':
  app.run_server()
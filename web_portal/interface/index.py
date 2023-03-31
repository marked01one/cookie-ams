from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
from services.http_service import ManufacturerService, TransformerService

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
manufacturer = ManufacturerService()
transformer = TransformerService()

app.layout = html.Div(className="container", children=[
  html.H1("Asset Management System", id='on_init'),
  html.Table(className='table', children=[
    html.Thead(id='table_columns'),
    html.Tbody(id='table_data')
  ])
])

@callback([Output('table_columns', 'children'), Output('table_data', 'children')], Input("on_init", "n_clicks"))
def update_output_div(n_clicks):
  response_body = transformer.get_transformers({})['content']['results']
  columns = list(response_body[0].keys())
  # Create the table head columns
  table_columns = [html.Th(col.upper(), scope="col") for col in columns[1:]]
  # Create the table body, i.e. the data
  table_data = [
    html.Tr([
      html.Td(children=obj[key]) for key in columns[1:]
    ]) 
    for obj in response_body
  ]
  return table_columns, table_data


if __name__ == '__main__':
  app.run_server()
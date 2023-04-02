import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

from services.http_service import ManufacturerService, TransformerService

dash.register_page(__name__, path='/logs')

manufacturer = ManufacturerService()
transformer = TransformerService()

layout = html.Div(children=[
  html.H1("Transformers", className="ms-5", style={'marginTop': 15, 'marginBottom': 0}, id='on_init'),
  html.Hr(className="ms-5"),
  html.P("Annual Transformers Distribution", style={"fontSize": 32, 'marginLeft': 24, 'paddingLeft': 24}),
  dcc.Graph(id="output-graph", className='ms-5'),
  html.Hr(className="ms-5"),
  html.P("Transformer Logs", style={"fontSize": 32, 'marginLeft': 24, 'paddingLeft': 24}),
  html.Table(className='table mx-5 pe-5 border-dark', children=[
    html.Thead(id='table_columns', className="bg-dark text-white"),
    html.Tbody(id='table_data')
  ])
])


@callback([
  Output('table_columns', 'children'), Output('table_data', 'children'),
  Output('output-graph', 'figure')
], Input("on_init", "n_clicks"))
def update_output_div(n_clicks):
  response_body = transformer.get_transformers({})['content']['results']
  
  # Get the list of columns from the response body
  columns = list(response_body[0].keys())
  
  #Create the table head columns
  table_columns = [html.Th(col.upper(), scope="col") for col in columns[1:]]
  
  # Create the table body, i.e. the data
  table_data = [
    html.Tr([
      html.Td(children=obj[key]) for key in columns[1:]
    ]) 
    for obj in response_body
  ]
  
  # Create the year/count columns for 
  time_count = {}
  time_count['Year'] = list({ int(obj['date_created'].split("-")[0]) for obj in response_body })
  time_count['Count'] = [
    len([
      obj['date_created'].split("-")[0] for obj in response_body 
      if int(obj['date_created'].split("-")[0]) == year
    ])
    for year in time_count['Year']
  ]
  
  fig_data = px.line(
    pd.DataFrame(time_count), x="Year", y="Count", template="plotly_white",
    width=1200
  )
  
  fig_data.update_layout(
    xaxis={
      "showline": True,
      "linewidth": 1,
      "linecolor": 'black',
      'mirror': False,
      'titlefont': {"size": 20, "family": "Helvetica"}
    },
    yaxis={
      "showline": True,
      "linewidth": 1,
      "linecolor": 'black',
      'mirror': False,
      'titlefont': {"size": 20, "family": "Helvetica"}
    }
  )
  
  return table_columns, table_data, fig_data
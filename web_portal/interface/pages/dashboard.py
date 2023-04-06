import dash
from dash import html, dcc, callback, Input, Output, clientside_callback
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

from services.http_service import ManufacturerService, TransformerService

dash.register_page(__name__, path='/', name="Dashboard")


layout = html.Div(className="mx-5", children=[
  html.H1("Dashboard", className="mt-5 mb-2", id='on_init'),
  dcc.Graph(id="output-graph", className='border-top border-bottom border-secondary'),
  
  html.Div(className="row mb-2 mt-5", children=[
    html.Div(className="col-6 d-flex justify-content-start", children=[
      html.H1("Transformers")
    ]),
    
    html.Div(className="col-6 d-flex justify-content-end", children=[
      html.Select(
        className="btn btm-sm btn-outline-secondary my-2", 
        id="sort_manufacturers"),
      html.Button(className="btn btm-sm btn-outline-secondary dropdown-toggle my-2", children="Data since")
    ])
  ]),
  html.Div(style={'overflow': 'auto'}, className="table-responsive", children=[
    html.Table(className='table table-striped table-sm', children=[
      html.Thead(id='table_columns', className="border-bottom border-dark", style={'fontSize': 16}),
      html.Tbody(id='table_data', style={'fontSize': 16})
    ])
  ])
  
])


@callback([
  Output('table_columns', 'children'), Output('table_data', 'children'),
  Output('output-graph', 'figure'),
  Output('sort_manufacturers', 'children')
], Input("on_init", "n_clicks"))
def update_output_div(n_clicks):
  response_body = TransformerService.get_transformers({})['content']['results']
  
  # Get the list of columns from the response body
  columns = list(response_body[0].keys())
  
  #Create the table head columns
  table_columns = html.Tr(
    [
      html.Th(col.replace('_', ' ').upper(), scope="col", style={'paddingRight': 72}) 
      for col in columns[1:]
    ]
  )
  
  # Create the table body, i.e. the data
  table_data = [
    html.Tr([
      html.Td(children=obj[key], style={'paddingRight': 72}) for key in columns[1:]
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
  
  # Generate graph for dashboard
  fig_data = px.line(
    pd.DataFrame(time_count), x="Year", y="Count", template="plotly_white",
    width=1200, title='Annual Transformer Distribution'
  ) 
  fig_data.update_layout(
    title={
      'text': 'Annual Transformer Distribution',
      'x': 0.5,
      'y': 0.85,
      'xanchor': 'center',
      'yanchor': 'top',
      'font': {"size": 24, "family": "Helvetica"}
    },
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
  
  sort_manufacturers = [
    html.Option(value=m['manufacturer_name'], children=m['manufacturer_name'])
    for m in ManufacturerService.get_manufacturers()['content']
  ]
  
  return table_columns, table_data, fig_data, sort_manufacturers

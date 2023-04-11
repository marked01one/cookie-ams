import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px

from services.http_service import ManufacturerService, TransformerService, RegionService

dash.register_page(__name__, path='/', name="Dashboard")


layout = html.Div(className="mx-5", children=[
  # Dashboard
  html.Div(children=[
    html.H1("Dashboard", className="mt-5 mb-2", id="dashboard_init"),
    html.Div(className="row", children=[
      html.Div(className='col-4 col-md-2 my-2 border-primary', children=[
        dcc.Dropdown(
          options=['Manufacturer', 'Region'],
          id="filter_plot_graph",
          placeholder='Plot by...'
        ),  
      ])
    ]),
    dcc.Graph(id="output-graph", className='border border-secondary'),
    
  ]),
  
  #
  html.Div(id='table_init', children=[
    html.Div(className="mb-2 mt-5", children=[
      html.Div(children=[
        html.H1("Transformers")
      ]),
      html.Div(className="row", children=[
        html.Div(className='col-4 col-md-2 my-2 border-primary', children=[
          dcc.Dropdown(options=[
              m['manufacturer_name'] for m in ManufacturerService.get_manufacturers()['content']
            ],
            id="filter_manufacturer_table",
            placeholder='Select a manufacturer...'
          ),  
        ]),
        html.Div(className='col-4 col-md-2 my-2 border-primary', children=[
          dcc.Dropdown(options=[
            r['region_name'] for r in RegionService.get_regions()['content']
          ],
          id="filter_region_table",
          placeholder='Select a region...',
          )
        ])
      ]),

      html.Div(className="form-text", id="table_items_count")
    ]),
    
    html.Div(style={'overflow': 'auto'}, className="table-responsive", children=[
      dbc.Table(
        id="transformer_table",
        className='table table-striped table-sm',
        bordered=True
      )
    ])
  ]),
  
  html.Nav([
    html.Ul()
  ])
])


@callback([
  Output('output-graph', 'figure'),
], [
  Input("dashboard_init", "n_clicks"), Input("filter_plot_graph", "value")
])
def update_output_div(n_clicks, sort_option: str):
  transformer_response = TransformerService.get_transformers({})['content']['results']
  
  query_dict = {}

  # Create the year/count columns for dashboard
  time_count = {
    'Year': [],
    'Count': []
  }
  
  if sort_option == 'Manufacturer':
    manufacturer_response = ManufacturerService.get_manufacturers()['content']
    query_dict = {
      m['manufacturer_name']: m['id']
      for m in manufacturer_response
    }
    time_count[sort_option] = []
    
  if sort_option == 'Region':
    region_response = RegionService.get_regions()['content']
    query_dict = { r['region_name']:r['id'] for r in region_response }
    time_count[sort_option] = []
  
  if query_dict != {}:
    for key, value in query_dict.items():
  
      option_response = TransformerService.get_transformers({
        f'{sort_option.lower()}_id': value
      })['content']['results']
      
      year_list = list({ int(obj['date_created'].split("-")[0]) for obj in option_response })
      count_list = [
        len([
          obj['date_created'].split("-")[0] for obj in option_response 
          if int(obj['date_created'].split("-")[0]) == year
        ])
        for year in year_list
      ]
      opt_list = [key for _ in range(len(count_list))]
      
      time_count['Year'] += year_list
      time_count['Count'] += count_list
      time_count[sort_option] += opt_list
  
  else:
    option_response = TransformerService.get_transformers({})['content']['results']
    
    year_list = list({ int(obj['date_created'].split("-")[0]) for obj in option_response })
    count_list = [
      len([
        obj['date_created'].split("-")[0] for obj in option_response 
        if int(obj['date_created'].split("-")[0]) == year
      ])
      for year in year_list
    ]
      
    time_count['Year'] += year_list
    time_count['Count'] += count_list
    
  
  df = pd.DataFrame(time_count).sort_values(by=['Year'])
  
  # Generate graph for dashboard
  if sort_option:
    fig_data = px.line(
      df, x="Year", y="Count", template="plotly_white",
      markers=True, color=sort_option,
      title="Annual Transformer Distribution by " + sort_option
    ) 
  else:
    fig_data = px.line(
      df, x="Year", y="Count", template="plotly_white",
      title='Annual Transformer Distribution', markers=True
    )
  
  fig_data.update_layout(
    title={
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
  return [fig_data]


@callback([
  Output('transformer_table', 'children'), Output('table_items_count', 'children')
], [
  Input('table_init', 'id'), 
  Input("filter_manufacturer_table", "value"), Input("filter_region_table", "value")
])
def table_init(id, manufacturer, region):
  manufacturer_response = ManufacturerService.get_manufacturers()['content']
  region_response = RegionService.get_regions()['content']
  
  transformer_query = {'page': 1, 'page_size': 25}
  
  # Extract current choice for manufacturer
  try:
    transformer_query['manufacturer_id'] = [
      m['id'] for m in manufacturer_response if m['manufacturer_name'] == manufacturer
    ][0]
  except IndexError:
    pass
  
  # Extract current choice for manufacturer
  try:
    transformer_query['region_id'] = [
      r['id'] for r in region_response if r['region_name'] == region
    ][0]
  except IndexError:
    pass
  
  transformer_response = TransformerService.get_transformers(transformer_query)['content']

  # Get the list of columns from the response body
  columns = list(transformer_response['results'][0].keys())
  
  #Create the table head columns
  table_columns = [
    html.Thead(html.Tr([
      html.Th(col.replace('_', ' ').title(), scope="col") 
      for col in columns[1:]
    ], className="bg-dark text-white")
  )]
  
  # Create the table body, i.e. the data
  table_data = [
    html.Tbody([html.Tr([html.Td(children=obj[key]) for key in columns[1:]]) 
    for obj in transformer_response['results']
    ])
  ]
  
  # Get length of table
  if transformer_response['count'] > 0:
    table_length = [
      "There are ",
      html.Strong(str(transformer_response['count'])), 
      " transformers with these specifications."
    ]  
  else:
    table_length = "There are no transformers with these specifications."
  
  return [(table_columns + table_data), table_length]


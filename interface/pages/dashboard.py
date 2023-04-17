import random
from typing import Any
import dash
from dash import html, dcc, callback, Input, Output, no_update
import dash_bootstrap_components as dbc
import pandas as pd 
import plotly.express as px

from services.http_service import ManufacturerService, TransformerService, RegionService

dash.register_page(
  __name__, path='/', name="Dashboard",
  title="CookieAMS - Main Dashboard"
)

STATUS_DEMO = [('Healthy', 'text-success') for _ in range(12)] + \
  [('Degrading', 'text-warning') for _ in range(6)] + \
  [('Critical', 'text-danger') for _ in range(3)]


layout = html.Div([
  # Dashboard
  html.Div(children=[
    html.H1("Dashboard", style={'marginBottom': 0, 'marginTop': 32}, id="dashboard_init"),
    html.Hr(style={'marginTop': 6, 'marginBottom': 32}),
    html.Div(className="row", children=[
      html.Div(id="graph-title", className="col-auto fs-4 fst-underline", style={'fontFamily': 'Montserrat'}),
      html.Div(className='col-4 col-md-2 border-primary', children=[
        dcc.Dropdown(
          options=['Manufacturer', 'Region'],
          id="filter_plot_graph",
          placeholder='Plot by...'
        ),  
      ])
    ]),
    dcc.Graph(id="output-graph"),
    
  ]),
  
  # Transformer log tables
  html.Div(id='table_init', children=[
    html.Div(className="mb-2 mt-5", children=[
      html.Div(children=[
        html.H1("Transformers", style={'marginBottom': 0, 'marginTop': 32})
      ]),
      
      # Filter rows
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
        ]),
        html.Div(className="col4 col-md-2 my-2 border-primary", children=[
          html.Button(
            "CSV Download", id="btn_download_table",
            className="btn btn-outline-primary"
          ),
          dcc.Download(id="download_table_csv")
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
  Output('output-graph', 'figure'), Output('graph-title', 'children')
], [
  Input("dashboard_init", "id"), Input("filter_plot_graph", "value")
])
def update_output_div(id, sort_option: str):
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
    option_response = TransformerService.get_transformers()['content']['results']
    
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
      markers=True, color=sort_option
    )
    graph_title = f'Annual Transformer Count by {sort_option}' 
  else:
    fig_data = px.line(
      df, x="Year", y="Count", template="plotly_white",
      markers=True
    )
    graph_title = f'Annual Transformer Count'
  
  count_max = df['Count'].sort_values().to_list()[-1] + 1
  year_sorted = df['Year'].sort_values().to_list() 
  
  fig_data.update_traces(line={'width': 3})
  fig_data.update_layout(
    margin={'l': 8, 'r': 8, 't': 24, 'b': 8},
    yaxis_range=(0, count_max), 
    xaxis_range=(int(year_sorted[0]) - 1, int(year_sorted[-1]) + 1),
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
  return [fig_data, graph_title]


@callback([
  Output('transformer_table', 'children'), Output('table_items_count', 'children')
], [
  Input('table_init', 'id'), 
  Input("filter_manufacturer_table", "value"), Input("filter_region_table", "value")
])
def table_init(id, manufacturer, region):
  '''
  Callback function for generating the data table
  '''
  transformer_query = {'page': 1, 'page_size': 25}
  
  # Extract current choice for manufacturer
  if manufacturer:
    manufacturer_response = ManufacturerService.get_manufacturers()['content']
    transformer_query['manufacturer_id'] = [
      m['id'] for m in manufacturer_response if m['manufacturer_name'] == manufacturer
    ][0]
  
  # Extract current choice for manufacturer
  if region:
    region_response = RegionService.get_regions()['content']
    transformer_query['region_id'] = [
      r['id'] for r in region_response if r['region_name'] == region
    ][0]
    
  
  
  
  transformer_response = TransformerService.get_transformers(transformer_query)['content']

  # Get the list of columns from the response body
  columns = list(transformer_response['results'][0].keys())
  
  #Create the table head columns
  table_columns = [
    html.Thead(html.Tr([
      html.Th(col.replace('_', ' ').title(), scope="col") 
      for col in columns[1:]
    ] + [html.Th('Health Status', scope='col')]
    , className="bg-dark text-white")
  )]
  
  # Create the table body, i.e. the data
  data_list = []
  
  for obj in transformer_response['results']:
    status = random.choice(STATUS_DEMO)
    
    match status[0]:
      case 'Healthy':
        percentage = random.randint(40,99)
      case 'Degrading':
        percentage = random.randint(15,39)
      case 'Critical':
        percentage = random.randint(1,14)
    
    data_list.append(html.Tr(
      [html.Td(obj[key]) for key in columns[1:]] +
      [html.Td([html.Strong(status[0]), f" ({percentage}%)"], className=status[1])]
    ))
    
  table_data = [html.Tbody(data_list)]
  
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


@callback([
  Output('download_table_csv', "data")
], [
  Input('btn_download_table', 'n_clicks')
])
def download_table_as_csv(n_clicks) -> None | dict[str, Any | None]:
  if n_clicks:
    transformer_response = TransformerService.get_transformers()['content']['results']
    
    columns = list(transformer_response[0].keys())
    
    df = pd.DataFrame({
      col:[tr[col] for tr in transformer_response]
      for col in columns
    })
    
    return [dcc.send_data_frame(df.to_csv, 'data_table.csv')]

  else:
    return [no_update]


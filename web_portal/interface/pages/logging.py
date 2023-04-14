import dash
from dash import html, dcc, callback, Input, Output, no_update
import dash_bootstrap_components as dbc

from services.http_service import ManufacturerService, RegionService

dash.register_page(
  __name__, path='/logs', name="Logging",
  title="CookieAMS - Logging"
)


layout = html.Div(id="on_init_logs", className="mx-2", children=[
  html.H1("Logging", style={'marginBottom': 0, 'marginTop': 32}, id='on_init'),
  
  html.Hr(style={'marginTop': 6, 'marginBottom': 32}),
  
  html.Div(className="my-4", children=[
    html.H3("New Transformer", style={'fontFamily': 'Montserrat'}),
    
    html.Form([
      # Serial number
      html.Div(className="row g-3 align-items-center mb-3 mt-1", children=[
        html.Div(className="col-auto", children=[
          html.Label("Serial number:", className="col-form-label", style={'fontSize': 20})
        ]),
        html.Div(className="col-6 col-md-3 col-lg-2", children=[
          dcc.Input(type="text", className="form-control", placeholder='Enter serial number...')
        ]),
        html.Div(className="col-auto form-text mt-3", children=[
          'Serial number for a new transformer. ',
          html.Strong("This should be unique!")
        ]),
      ]),
      
      # Manufacturer
      html.Div(className="row g-3 align-items-center my-3", children=[
        html.Div(className="col-auto", children=[
          html.Label("Manufacturer:", className="col-form-label", style={'fontSize': 20})
        ]),
        html.Div(className="col-6 col-md-3 col-lg-2", children=[
          dcc.Dropdown(
            options=[m['manufacturer_name'] for m in ManufacturerService.get_manufacturers()['content']],
            placeholder='Select a manufacturer...'
          ),
        ]),
        html.Div(className="col-auto form-text mt-3", children=[
          html.Span("Manufacturer of the transformer.")
        ]),
      ]),
      
      # Region
      html.Div(className="row g-3 align-items-center my-3", children=[
        html.Div(className="col-auto", children=[
          html.Label("Region:", className="col-form-label", style={'fontSize': 20})
        ]),
        html.Div(className="col-6 col-md-3 col-lg-2", children=[
          dcc.Dropdown(
            options=[m['region_name'] for m in RegionService.get_regions()['content']],
            placeholder='Select a region...'
          ),
        ]),
        html.Div(className="col-auto form-text mt-3", children=[
          html.Span("Region of the transformer.")
        ]),
      ]),
      
      # Rated kVA
      html.Div(className="row g-3 align-items-center my-3", children=[
        html.Div(className="col-auto", children=[
          html.Label("Rated kVA:", className="col-form-label", style={'fontSize': 20})
        ]),
        html.Div(className="col-6 col-md-3 col-lg-2", children=[
          dcc.Input(type="text", className="form-control", placeholder='Enter rated kVA...'),
        ]),
        html.Div(className="col-auto form-text mt-3", children=[
          html.Span("The rated kVA of the transformer.")
        ]),
      ]),
      
      # Submit button
      html.Div(className="row g-3 align-items-center my-3 mx-2", children=[
        dbc.Button(
          "Submit transformer", outline=True, color="primary", 
          className="me-1 col-6 col-md-3 col-lg-2", type="button",
          id='submit_transformer_button', n_clicks=0
        )
      ])
    
    ]),
    
    dbc.Toast(
      id="new_transformer_toast", 
      is_open=False, 
      duration=3000,
      dismissable=True,
      style={"position": "fixed", "top": 80, "right": 10, "width": 350}
    )
  ]),
  
  
  html.Hr(style={'marginBottom': 32, 'marginTop': 6}),
  
  html.H2("New Failure", style={'fontFamily': 'Montserrat'}),
  
  html.Form([
    # Search by serial
    html.Div(className="my-3", children=[
      html.Label("Search transformer by serial:", className="col-form-label", style={'fontSize': 20}),
      dcc.Input(type="text", className="form-control", placeholder='Search...'),
    ]),
    
    # Failure cause
    html.Div(className="row g-3 align-items-center my-3", children=[
      html.Div(className="col-auto", children=[
        html.Label("Failure Cause:", className="col-form-label", style={'fontSize': 20})
      ]),
      html.Div(className="col-6 col-md-3 col-lg-2", children=[
        dcc.Input(type="text", className="form-control", placeholder='Enter failure cause...'),
      ]),
      html.Div(className="col-auto form-text mt-3", children=[
        html.Span("The rated KvA of the transformer.")
      ]),
    ]),
    
    # Description
    html.Div(className="my-3", children=[
      html.Label(
        "Description of failure:", 
        className="col-form-label", style={'fontSize': 20}
      ),
      dcc.Textarea(
        className="form-control", 
        placeholder="Enter a description of the failure...",
        style={'fontFamily': 'Consolas', 'minHeight': 200}
      )
    ]),
    
    # Submit new failure
    html.Div(className="row g-3 align-items-center my-3 mx-2", children=[
      dbc.Button(
        "Submit failure", outline=True, color="primary", 
        className="me-1 col-6 col-md-2", type="button",
        id='submit_failure_button', n_clicks=0
      ),
    ]),
    
    dbc.Toast(
      id="new_failure_toast", 
      is_open=False, 
      duration=3000,
      dismissable=True,
      style={"position": "fixed", "top": 80, "right": 10, "width": 350}
    )
  ]),
])





## ! ------------------------- CALLBACKS ------------------------- ##

@callback([
  Output('new_transformer_toast', 'is_open'), Output('new_transformer_toast', 'icon'),
  Output('new_transformer_toast', 'header'), Output('new_transformer_toast', 'children') 
], [
  Input('submit_transformer_button', 'n_clicks')
])
def submit_new_transformer(n_clicks):
  '''
  Callback function for handling the transformer form
  '''
  if n_clicks > 0:
    return [True, 'success', 'Success!', 'A new transformer is registered!']
    
  return [no_update for _ in range(4)]
  


@callback([
  Output('new_failure_toast', 'is_open'), Output('new_failure_toast', 'icon'),
  Output('new_failure_toast', 'header'), Output('new_failure_toast', 'children') 
], [
  Input('submit_failure_button', 'n_clicks')
])
def submit_new_failure(n_clicks):
  '''
  Callback function for handling the failure form
  '''
  if n_clicks > 0:
    return [True, 'success', 'Success!', 'A new failure is registered!']
    
  return [no_update for _ in range(4)]
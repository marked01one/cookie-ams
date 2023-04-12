import dash
from dash import html, dcc
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
    html.H2("New Transformer"),
    
    html.Form([
      # Serial number
      html.Div(className="row g-3 align-items-center mb-3 mt-1", children=[
        html.Div(className="col-auto", children=[
          html.Label("Serial number:", className="col-form-label", style={'fontSize': 20})
        ]),
        html.Div(className="col-6 col-md-3 col-lg-2", children=[
          dcc.Input(type="text", className="form-control", placeholder='Enter serial number...')
        ]),
        html.Div(className="col-auto form-text", children=[
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
        html.Div(className="col-auto form-text", children=[
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
        html.Div(className="col-auto form-text", children=[
          html.Span("Region of the transformer.")
        ]),
      ]),
      
      # Rated kVA
      html.Div(className="row g-3 align-items-center my-3", children=[
        html.Div(className="col-auto", children=[
          html.Label("Rated kVA:", className="col-form-label", style={'fontSize': 20})
        ]),
        html.Div(className="col-6 col-md-3 col-lg-2", children=[
          dcc.Input(type="text", className="form-control", placeholder='Enter rated KvA...'),
        ]),
        html.Div(className="col-auto form-text", children=[
          html.Span("The rated kVA of the transformer.")
        ]),
      ]),
      
      # Submit button
      html.Div(className="row g-3 align-items-center my-3", children=[
        dbc.Button(
          "Submit transformer", outline=True, color="primary", 
          className="me-1 col-6 col-md-3 col-lg-2"
        )
      ])
    
    ]),
    
  ]),
  
  
  html.Hr(),
  
  html.H2("New Failure", style={'marginBottom': 0, 'marginTop': 32}),
  
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
      html.Div(className="col-auto form-text", children=[
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
    html.Div(className="row g-3 align-items-center my-3", children=[
      dbc.Button(
        "Submit failure", outline=True, color="primary", 
        className="me-1 col-6 col-md-2"
      )
    ])
  ]),
])


# @callback(
#   [Output('alert_new_transformer', 'is_open')],
#   [Input('')]
# )
# def submit_new_transformer():
#   return 
  
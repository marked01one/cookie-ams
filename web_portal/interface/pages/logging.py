from pydoc import classname
from re import M
import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

from services.http_service import ManufacturerService, TransformerService, RegionService

dash.register_page(__name__, path='/logs')

layout = html.Div(id="on_init_logs", className="mx-5", children=[
  html.H1("Logging", style={'marginBottom': 0, 'marginTop': 32}, id='on_init'),
  html.Hr(style={'marginTop': 6, 'marginBottom': 32}),
  
  html.H2("New Transformer", style={'marginBottom': 0, 'marginTop': 32}),
  
  html.Form(children=[
    html.Div(className="row g-3 align-items-center mb-3 mt-1", children=[
      html.Div(className="col-auto", children=[
        html.Label("Serial number:", className="col-form-label", style={'fontSize': 20})
      ]),
      html.Div(className="col-auto", children=[
        dcc.Input(type="text", className="form-control")
      ]),
      html.Div(className="col-auto form-text", children=[
        'Serial number for a new transformer. ',
        html.Strong("This should be unique!")
      ]),
    ]),
    
    html.Div(className="row g-3 align-items-center my-3", children=[
      html.Div(className="col-auto", children=[
        html.Label("Manufacturer:", className="col-form-label", style={'fontSize': 20})
      ]),
      html.Div(className="col-auto", children=[
        html.Select(className="form-select", id="manufacturer-form")
      ]),
      html.Div(className="col-auto", children=[
        html.Span("Manufacturer of the transformer.", className="form-text")
      ]),
    ]),
    
    html.Div(className="row g-3 align-items-center my-3", children=[
      html.Div(className="col-auto", children=[
        html.Label("Region:", className="col-form-label", style={'fontSize': 20})
      ]),
      html.Div(className="col-auto", children=[
        html.Select(className="form-select", id="region-form")
      ]),
      html.Div(className="col-auto", children=[
        html.Span("Region of the transformer.", className="form-text")
      ]),
    ]),
  ]),
])


@callback(
  Output("manufacturer-form", "children"), Output("region-form", "children"),
  Input("on_init_logs", "id")
)
def on_init(id):
  manufacturer_response = ManufacturerService.get_manufacturers()
  region_response = RegionService.get_regions()
  selectors = {
    "manufacturer": [html.Option(selected=True, children="Choose a manufacturer")],
    "region": [html.Option(selected=True, children="Choose a region")]
  }
  manufacturers_list = [
    html.Option(value=m['manufacturer_name'], children=m['manufacturer_name']) 
    for m in manufacturer_response['content']
  ]
  
  region_list = [
    html.Option(value=r['region_name'], children=r['region_name'])
    for r in region_response['content']
  ]
  
  return (selectors['manufacturer'] + manufacturers_list), (selectors['region'] + region_list)  
  
  
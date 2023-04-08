import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

from services.http_service import ManufacturerService, TransformerService

dash.register_page(__name__, path='/insights')

layout = html.Div([
  html.H1("Insights", className="mx-5", style={'marginBottom': 0, 'marginTop': 32}, id='on_init'),
  
])
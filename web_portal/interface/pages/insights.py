import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

from services.http_service import ManufacturerService, TransformerService

dash.register_page(
  __name__, path='/insights', name="Insights",
  title="CookieAMS - Insights"
)

layout = html.Div(className="mx-2", children=[
  html.H1("Insights", style={'marginBottom': 0, 'marginTop': 32}, id='insight_on_init'),
  
  html.Hr(style={'marginTop': 6, 'marginBottom': 32}),
  
  html.Div(className="row", children=[
    html.Div(className="col-8", children=[
      dcc.Graph(id="", className="col-8"),
    ]),
    
    html.Div(className="col-4", children=[
      dcc.Graph(id="pie_chart_categories"),
      dcc.RadioItems(
        options=['Manufacturer', 'Region', 'kVA'],
        value='Manufacturer',
        id="pie_chart_radio"
      )
    ]),
  ])
  
  
])


@callback([
  Output('pie_chart_categories', 'figure')
], [
  Input('insight_on_init', 'id'), Input('pie_chart_radio', 'value')
])
def pie_chart_types(id, radio_value: str):
  transformer_response = TransformerService.get_transformers()['content']['results']
  
  columns = list(transformer_response[0].keys())
  
  df = pd.DataFrame({
    col:[tr[col] for tr in transformer_response]
    for col in columns
  })
  
  fig = px.pie(df, names=radio_value.lower())
  
  return [fig]
  
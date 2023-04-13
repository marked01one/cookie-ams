import dash
from dash import html, dcc, callback, Input, Output, dash_table
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go

from services.http_service import ManufacturerService, TransformerService, FailureService

dash.register_page(
  __name__, path='/insights', name="Insights",
  title="CookieAMS - Insights"
)

layout = html.Div([
  html.H1("Insights", style={'marginBottom': 0, 'marginTop': 32}, id='insight_on_init'),
  
  html.Hr(style={'marginTop': 6, 'marginBottom': 32}),
  
  html.Div(className="row", children=[
    html.Div(className="col-12 col-md-8", children=[
      html.Div(
        id='graph_chart_share_title', 
        className="border border-bottom-0 border-2 border-muted ps-3 py-2",
        style={'fontSize': 16, 'fontFamily': 'Montserrat'}
      ),
      html.Div(className="border border-2 border-muted", children=[
        dcc.Graph(id="failure_graph_comparison"),
        dcc.Dropdown(
          options=['Manufacturer', 'Region', 'kVA', 'Failure Cause'],
          value='Manufacturer',
          className="mx-2 mb-2 d-flex justify-content-between",
          clearable=False,
          id="graph_chart_share"
        )
      ]),
      
    ]),
    
    html.Div(className="col-12 col-md-4", children=[
      html.Div(
        id='pie_chart_share_title', 
        className="border border-bottom-0 border-2 border-muted ps-3 py-2",
        style={'fontSize': 16, 'fontFamily': 'Montserrat'}
      ),
      html.Div(className="border border-2 border-muted", children=[
        dcc.Graph(id="pie_chart_categories"),
        dcc.Dropdown(
          options=['Manufacturer', 'Region', 'kVA', 'Failure Cause'],
          value='Manufacturer',
          className="mx-2 mb-2 d-flex justify-content-between",
          clearable=False,
          id="pie_chart_share"
        )
      ])  
    ])
    ,
  ])
  
  
])


@callback([
  Output('pie_chart_categories', 'figure'), Output('pie_chart_share_title', 'children')
], [
  Input('pie_chart_share', 'value')
])
def pie_chart_types(dropdown_value: str):
  if dropdown_value == 'Failure Cause':
    response = FailureService.get_failures()['content']['results']
  else:
    response = TransformerService.get_transformers()['content']['results']
  
  columns = list(response[0].keys())
    
  df = pd.DataFrame({
    col:[tr[col] for tr in response]
    for col in columns
  })
  
  filter_col = dropdown_value.lower().replace(' ', '_')
  
  fig = px.pie(df.sort_values(by=[filter_col]), names=filter_col, hole=0.3)
  fig.update_layout(margin={'l': 8, 'r': 8, 't': 8, 'b': 8})
  
  title = f'Transformer share, sorted by {dropdown_value.lower()}'
  
  return [fig, title]


@callback([
  Output('failure_graph_comparison', 'figure'), Output("graph_chart_share_title", 'children')
], [
  Input('graph_chart_share', 'value')
])
def graph_failure_correlation():
  failure_response = FailureService.get_failures()['content']['results']
  transformer_response = TransformerService.get_transformers()['content']['results']
  
  
  
  
  
  return



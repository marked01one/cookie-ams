from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash
import dash_bootstrap_components as dbc
from services.http_service import ManufacturerService, TransformerService

app = Dash(
  __name__,
  external_stylesheets=[dbc.themes.BOOTSTRAP], 
  use_pages=True
)


app.layout = html.Div([
  html.Nav(className="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0", children=[
    html.Div(className="navbar-brand col-sm-3 col-md-2", children=[
      html.A("ITC Asset Management", className="navbar-brand mx-3 my-4")
    ]),
  ]),
  html.Div(className="container-fluid", children=[
    html.Div(className="row", children=[
      html.Nav(className="col-md-2 d-none d-md-block bg-light sidebar", children=[
        html.Div(className="sidebar-sticky", children=[
          html.Ul(className="nav flex-column", children=[
            html.Li(className="nav-item", children=[
              dcc.Link(className="text-decoration-none nav-link font-bold", 
                children=f"{page['name']}", href=page['relative_path']
            )])
            for page in dash.page_registry.values()
          ])
        ])
      ]),
      html.Div(role="main", className="col-md-9", children=[
        dash.page_container
      ])
      
    ]),
  ]),
  
])




if __name__ == '__main__':
  app.run_server()
from dash import Dash, html, dcc, Input, Output, ALL, callback, callback_context
import dash, os
import dash_bootstrap_components as dbc
from typing import *

app = Dash(
  __name__,
  external_stylesheets=[dbc.themes.BOOTSTRAP], 
  use_pages=True
)

server = app.server
app.suppress_callback_exceptions = True

app.layout = html.Div([
  dcc.Location(id="url"),
  html.Nav(className="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow", children=[
    html.Div(className="navbar-brand my-2", children=[
      html.Div(className="navbar-brand mx-4", style={'fontFamily': 'Montserrat', 'fontSize': 14}, children=[
        html.Strong("CookieAMS", style={'fontSize': 24, 'fontWeight': 'bold'}),
        html.Span(
          'Your analytics partner for the Internet of Things', 
          className="text-decoration-none fst-italic ms-2"
        )
      ])
    ]),
  ]),
  html.Div(className="container-fluid", children=[
    html.Div(className="row", children=[
      html.Nav(
        className="col-md-2 d-none d-md-block bg-light sidebar sidebar-height",
        style={'fontFamily': 'Montserrat', 'fontSize': 18},
        children=[
          html.Div(className="sidebar-sticky", children=[
            html.Ul(className="nav flex-column mt-4", children=[
              html.Li(className="nav-item", children=[
                html.A(path['name'], 
                  id={"type": "link-navbar", "index": path['relative_path']}, href=path['relative_path']
                )
              ])
              for path in dash.page_registry.values()
            ])
          ])
      ]),
      html.Div(role="main", className="col-12 col-md-10 px-md-4", children=[
        dash.page_container
      ])
    ]),
  ]),
  
])


@callback(
  Output({"type":"link-navbar", "index": ALL}, "className"), 
  [Input("url", "pathname"),Input({"type":"link-navbar", "index": ALL}, "id")]
)
def highlight_current_page(pathname, link_elements) -> Iterable[str]:
    return [
      "text-decoration nav-link sidebar-anchors active" if val["index"] == pathname
      else "text-decoration-none nav-link py-1 inactive" 
      for val in link_elements
    ] 




if __name__ == '__main__':
  app.run_server(host='0.0.0.0', port=5000)
import pandas as pd
from dash import dcc, html, Input, Output
import geopandas as gpd
from dash.exceptions import PreventUpdate

from app import app
from layouts import nav_bar, CONTENT_STYLE, page1_layout, page2_layout, page3_layout
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav_bar(),
    html.Div(id='page-content',style=CONTENT_STYLE)
])

@app.callback(Output('page-content', 'children'),
        [Input('url', 'pathname')]
)

def display_page(pathname):
    if pathname == '/':
        return page1_layout
    if pathname == '/aves':
        return page2_layout
    elif pathname == '/planes':
        return page3_layout
    else:
        return '404'
    
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
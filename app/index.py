import pandas as pd
from dash import dcc, html, Input, Output
import geopandas as gpd
from dash.exceptions import PreventUpdate

from app import app
from layouts import page1_layout, page2_layout
import callbacks

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Situación de las aves', value='tab1', children=[page1_layout]),
        dcc.Tab(label='Planes de acción', value='tab2', children=[page2_layout])
    ]),
    html.Div(id='page-content')
])
@app.callback(
        [Output('page-content', 'children')],
        [Input('tabs', 'value')]
)

def render_content(tab):
    if tab == 'tab1':
        return page1_layout
    elif tab == 'tab2':
        return page2_layout
    raise PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
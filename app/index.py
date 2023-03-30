import pandas as pd
from dash import dcc, html, Input, Output
import geopandas as gpd

from app import app
from layouts import page1_layout, page2_layout
import callbacks

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Page 1', value='tab1', children=[page1_layout]),
        dcc.Tab(label='Page 2', value='tab2', children=[page2_layout])
    ]),
    html.Div(id='page-content', children=[])
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

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
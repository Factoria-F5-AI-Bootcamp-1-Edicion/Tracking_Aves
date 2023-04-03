import pandas as pd
from dash import dcc, html, Input, Output
import geopandas as gpd
from dash.exceptions import PreventUpdate

from app import app
from layouts import nav_bar, CONTENT_STYLE, page1_layout, page2_layout, page3_layout
import callbacks

#-------Diseño de lo que visualiza la usuaria
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), # Las páginas van asociadas a una url (página principal/situación de aves/planes de acción)
    nav_bar(), # Añadimos el navegador lateral
    html.Div(id='page-content',style=CONTENT_STYLE) # Definimos el espacio donde se imprimirá la página seleccionada.
])

@app.callback(Output('page-content', 'children'), # La Output es la página elegida
        [Input('url', 'pathname')] # El Input es la url introducida o seleccionada por la usuaria
)

#--------Función para mostrar página según la url introducida.
def display_page(pathname):
    if pathname == '/': # URL por defecto
        return page1_layout # Devuelve la Página Principal
    if pathname == '/aves':
        return page2_layout # Devuelve la página de Situación de Aves
    elif pathname == '/planes':
        return page3_layout # Devuelve la página de Planes de Acción
    
    else:
        return '404 No Encontrado' # Si la URL intruducida no es válida, devuelve un 404 No Encontrado
    
if __name__ == "__main__":
    app.run_server(host='0.0.0.0',debug=True, port=8050) # Corre el Servidor.
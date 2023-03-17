import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

df = pd.read_csv('./data_raw/Dataset_definitivo_con_geometrias.csv')

f = r"ESP_adm/ESP_adm1.shp"
shapes = gpd.read_file(f)

app = Dash(__name__) # inicializamos Dash

#App Layout
app.layout = html.Div([ # Definimos el diseño de La Pagina HTML donde correrá nuestro programa.
    html.H1("Web Pajaritos Dash", style={'text-align' : 'center'}), # Crea La Cabecera de la pagina HTML
    dcc.Dropdown (id="slct_nombre_comun", # Crea el Desplegable
        options=[# Lista de opciones para el Desplegable (Label: Valor que aparece para el usuario || Value: Valor inte
            {"label": "Abejaruco europeo", "value": "Abejaruco europeo"}, #Como que el valor Value es un año,
            {"label":"Acentor común", "value": "Acentor común"}, # podemos dejar el valor interno
            {"label": "Chotacabras cuellirrojo", "value": "Chotacabras cuellirrojo"}, # como un INTEGER
            {"label": "Ruiseñor común", "value": "Ruiseñor común"}],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value=2015, # Cambiamos Value a 2015 como default, asi el usuario ya tiene un mapa al entrar a la pagina
        clearable=False, # No aparece el boton de Borrar
        searchable=False, # No se puede buscar escribiendo
        style={"width": "40%"} # Style: Cambia el estilo en general del Desplegable (width: Ancho)
        ),
    html.Div(id="output_container", children= []), #Crea un bloque de texto debajo del Desplegable y crea una variable hija de t
    html. Br(), # Espacio en blanco Best InBI
    dcc.Graph(id='superstore_map', figure={}) # Crea el Mapa y crea una variable hija de tipo figura
])

# Conecta Los Graficos de Plotly con Los Componentes Dash
@app.callback( # Define Los Inputs y Outputs de la funcion update_graph (Actualizar Grafico)
    [Output (component_id='output_container', component_property='children'), # Output 1: Texto debajo del desplegable
    Output (component_id='superstore_map', component_property='figure')], #Output 2: Mapa
    [Input (component_id='slct_nombre_comun', component_property='value')] # Input: Año del Desplegable
    )

def update_graph (option_slctd):
    print(option_slctd) # Imprimimos a consola La opcion del usuario,
    print(type (option_slctd)) # y el tipo de la opcion (best practices).
    
    container="El ave seleccionada es: {}".format(option_slctd) # Cambiamos el texto debajo del desplegable al Año introducido
    
    dff = df.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original
    dff = dff[dff["NOMBRE COMÚN"] == option_slctd] # Filtramos La nueva DataFrame por año, asi tenemos solo del año introducido por el us
    
    #Plotly Express
    #Creamos el Mapa
    fig= px.choropleth_mapbox(#dff, 
        geojson=shapes.geometry,
        data_frame=dff, # Definimos La DataFrame con nuestra copia
        #locationmode='ESP', # Cambiamos el Tipo de Localizacion a Estados de EEUU
        locations=dff.index_ciudad, # Cambiamos Las Localizaciones para que  nuestra columna de Codigos de Es Best InBl
        # TIENEN QUE SER LOS CODIGOS DE ESTADO, NO PUEDEN SER LOS NOMBRES!!
        #scope="europe", # estados unidos
        color='Amenaza', # Definimos esta variable para cambiar La Columna que usa como referencia para añadir INTELIGESCOSOLUTIONS
        hover_data=['NOMBRE COMÚN', 'ARA', 'AND'],
        mapbox_style="carto-positron",
        zoom=4.3, 
        center = {"lat": 39.6, "lon": -4},
        opacity=0.5, # Definimos Los valores que aparezerán al pasar el ratón sobre un estado (C
        # Como que el Color va a estar basado en % de Beneficio, Plotly automaticamente lo asigna al ultimo valor en hover_data[
        #color_continuous_scale=px.colors.sequential.YlOrRd, # Define como cambia el color con % de Beneficio
        #emplate='plotly_dark' # Plantilla (plotly. io. templates)
    )
    return container, fig # Retornar Los Objetos que hemos creado
# IMPORTANTE: Retornar Los valores en el mismo orden que pusiste en Los Outputs!

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
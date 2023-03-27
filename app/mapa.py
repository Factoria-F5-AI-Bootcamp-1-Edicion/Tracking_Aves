import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output
import dash
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
from folium import plugins
import folium

df = pd.read_csv('./data_raw/aves_con_coordenadas.csv')

leyen_amen = pd.read_csv('./leyendas/leyendas_amenaza.csv')
leyen_plan = pd.read_csv('./leyendas/leyendas_planes.csv')

f = r"ESP/Espana_y_comunidades.shp"
shapes = gpd.read_file(f)

app = Dash(__name__) # inicializamos Dash

#App Layout
app.layout = html.Div([ # Definimos el diseño de La Pagina HTML donde correrá nuestro programa.
    html.H1("Web Pajaritos Dash", style={'text-align' : 'center'}), # Crea La Cabecera de la pagina HTML
    dcc.Dropdown (id="slct_nombre_comun", # Crea el Desplegable
        options=df['NOMBRE COMÚN'],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value='Chotacabras cuellirrojo', # Cambiamos Value a Chotacabras cuellirrojo como default, asi el usuario ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"} # Style: Cambia el estilo en general del Desplegable (width: Ancho)
        ),
    html.Div(id="output_container", children= []), #Crea un bloque de texto debajo del Desplegable y crea una variable hija de t
    html. Br(), # Espacio en blanco Best InBI
    dcc.Graph(id='superstore_map', figure={}), # Crea el Mapa y crea una variable hija de tipo figura
    html. Br(), # Espacio en blanco Best InBI
    dcc.Dropdown (id="slct_leyen_amenaza", # Crea el Desplegable
        options=[# Lista de opciones para el Desplegable (Label: Valor que aparece para el usuario || Value: Valor interno
            {"label": "(EN)", "value": 0}, #Como que el valor Value es un año,
            {"label":"EN*", "value": 1},
            {"label":"EN", "value": 2},
            {"label":"VU*", "value": 3},
            {"label":"VU", "value": 4},
            {"label":"LSPE", "value": 5}, 
            {"label":"CR", "value": 6},
            {"label":"DD", "value": 7},
            {"label":"NT", "value": 8},
            {"label":"EX", "value": 9},
            {"label":"LASRPE*", "value": 10},
            {"label":"LAESRPE", "value": 11},
            {"label":"SAH", "value": 12},
            {"label":"DIE", "value": 13},
            {"label":"IEC", "value": 14}, 
            {"label":"REPFSA", "value": 15},
            {"label":"R*", "value": 16},
            {"label":"LNESRPE", "value": 17},
            {"label":"LEFP", "value": 18},
            {"label":"TUT", "value": 19}
            ],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value=3, # Cambiamos Value a Chotacabras cuellirrojo como default, asi el usuario ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"} # Style: Cambia el estilo en general del Desplegable (width: Ancho)
        ),
    html.Div(id="output_container2", children= []),
    html. Br(),
    dcc.Slider(
        0,4,
        step=None,
        marks={
            0: 'SIN DATOS',
            1: 'LEVE',
            2: 'MEDIO',
            3: 'GRAVE',
            4: 'MUY GRAVE'},
        tooltip={"placement": "bottom", "always_visible": True}, # CREA los botones sombreados 
        id="slider",
        value=1
    ),
    html.Iframe(id='superstore_map2', width='100%', height='600'),

])

# Conecta Los Graficos de Plotly con Los Componentes Dash
@app.callback( # Define Los Inputs y Outputs de la funcion update_graph (Actualizar Grafico)
    [Output (component_id='output_container', component_property='children'), # Output 1: Texto debajo del desplegable
    Output (component_id='superstore_map', component_property='figure'),
    Output (component_id='output_container2', component_property='children'),
    Output (component_id='superstore_map2', component_property='srcDoc')], #Output 2: Mapa
    [Input (component_id='slct_nombre_comun', component_property='value'),
     Input (component_id='slct_leyen_amenaza', component_property='value'),
     Input (component_id='slider', component_property='value')] # Input: Ave seleccionada
    )

def update_graph (option_slctd, option_leyen, option_amenaza):
    print(option_slctd) # Imprimimos a consola La opcion del usuario,
    print(type (option_slctd)) # y el tipo de la opcion (best practices).
    print(option_leyen)
    print(type(option_leyen))
    print(option_amenaza)
    print(type(option_amenaza))
    
    container="El ave seleccionada es: {}".format(option_slctd) # Cambiamos el texto debajo del desplegable al Año introducido
    leyenda=leyen_amen['Leyenda'].iloc[option_leyen]
    significado=leyen_amen['Significado'].iloc[option_leyen]
    container2=f'{leyenda}'+' es igual a '+f'{significado}'
    
    dff = df.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original.
    dff = dff[dff["NOMBRE COMÚN"] == option_slctd].reset_index() # Filtramos La nueva DataFrame por ave seleccionada, asi tenemos solo el ave que buscamos.
    dfff = df.copy()
    calor = dfff[dfff['NIVEL AMENAZA']==option_amenaza]
   
    if dff['GLOBAL UICN RED LIST (consulta 2022)'][0]!='NP':
        global_cat = dff['GLOBAL UICN RED LIST (consulta 2022)'][0]
        titulo = 'La amenaza del '+f'{option_slctd}'+' a nivel global es'+' '+f'{global_cat}'
    else:
        titulo = 'No hay categorización a nivel global'
   

    #Plotly Express
    #Creamos el Mapa
    colorscale = ["rgb(33, 74, 12)", "rgb(67, 136, 33)", "rgb(94, 179, 39)", "rgb(210, 231, 154)", "rgb(255, 51, 51)"]
    fig= px.choropleth_mapbox(
        geojson=shapes.geometry,
        data_frame=dff, # Definimos La DataFrame con nuestra copia
        locations=dff.index_ciudad, # Cambiamos Las Localizaciones para que  nuestra columna de 'index_ciudad' para que sepa qué comunidad es(Números, no nombres)
        color='NIVEL AMENAZA', # Definimos esta variable para cambiar La Columna que usa como referencia para añadir colores.
        hover_name='Ubicacion', # El título en negrita de cada cuadro de información que se abre al pasar el ratón por encima.
        hover_data=['NOMBRE COMÚN', 'Amenaza', 'CEEA y LESRPE'], # Datos que se muestran en el cuadro informativo.
        labels={0 : 'Sin datos suficientes', 1: 'Amenaza Leve', 2 : 'Amenaza Media', 3 : 'Amenaza Grave', 4 :'Amenaza Muy Grave'} ,
        color_continuous_scale=colorscale,
        color_continuous_midpoint=1,
        mapbox_style='stamen-watercolor', # Estilo del mapa, hemos puesto este que es un mapa de acuarela. Otras posibilidad más seria: 'carto-positron'
        title=titulo,  # Título de la figura
        zoom=4, 
        center = {"lat": 39.6, "lon": -4},
        opacity=0.5, # Definimos Los valores que aparezerán al pasar el ratón sobre un estado
    )
    fig.update_layout(
            autosize=False,
            width=1000,
            height=1000,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            ))

    map = folium.Map(location=[40, -2], tiles="Cartodb dark_matter", zoom_start=6)
    heat_data = [[row['lat'],row['lon']] for index, row in calor.iterrows()]
    plugins.HeatMap(heat_data).add_to(map)
    map.save("map_1.html")

    return container, fig, container2, open('map_1.html', 'r').read() # Retornar Los Objetos que hemos creado
# IMPORTANTE: Retornar Los valores en el mismo orden que pusiste en Los Outputs!

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
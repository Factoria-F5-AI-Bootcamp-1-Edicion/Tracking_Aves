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
from seleccionar_img import selectImg, selectImgs
 

df = pd.read_csv('./data_raw/aves_df.csv')

leyen_amen = pd.read_csv('./leyendas/leyendas_amenaza.csv')
leyen_plan = pd.read_csv('./leyendas/leyendas_planes.csv')

f = r"ESP/Espana_y_comunidades.shp"
shapes = gpd.read_file(f)

app = Dash(__name__) # inicializamos Dash

#App Layout
app.layout = html.Div([ # Definimos el diseño de La Pagina HTML donde correrá nuestro programa.
    html.H1("Web Pajaritos Dash", style={'text-align' : 'center'}), # Crea La Cabecera de la pagina HTML
    dcc.Dropdown (id="slct_nombre_comun", # Crea el Desplegable
        options=df['nombre_comun&cientifico'],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value='Abubilla común-Upupa epops', # Cambiamos Value a Chotacabras cuellirrojo como default, asi el usuario ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"} # Style: Cambia el estilo en general del Desplegable (width: Ancho)
        ),
    html.Div(id="output_container", children= []), #Crea un bloque de texto debajo del Desplegable y crea una variable hija de t
    html. Br(), # Espacio en blanco Best InBI
    dcc.Graph(id='superstore_map', figure={}, style={'float': 'right','margin': 'auto'}),
    dcc.Tabs(
        id="tabs",
        value="tab-1",
        children=[
            dcc.Tab(
                label="Canarias 2004 & 2021",
                value="tab-1",
                children=[html.H4(id='texto1'),
                          html.Img(id='img1', style={'display': 'inline-block', 'height':'20%'}),
                          html.H4(id='texto2'),
                          html.Img(id='img2', style={'display': 'inline-block', 'height':'20%'})]
            ),
            dcc.Tab(
                label="Península Reproductoras 2004 & 2021",
                value="tab-2",
                children=[html.H4(id='texto3'),
                          html.Img(id='img3', style={'display': 'inline-block', 'height':'20%'}),
                          html.H4(id='texto4'),
                          html.Img(id='img4', style={'display': 'inline-block', 'height':'20%'})]
            ),
            dcc.Tab(
                label="Península Migratorias 2004 & 2021",
                value="tab-3",
                children=[html.H4(id='texto5'),
                          html.Img(id='img5', style={'display': 'inline-block', 'height':'20%'}),
                          html.H4(id='texto6'),
                          html.Img(id='img6', style={'display': 'inline-block', 'height':'20%'})]
            )
        ],style={'float': 'right','margin': 'auto'} # 'float': 'right','margin': 'auto' -- 'width': '49%', 'display': 'inline-block'
    ),
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
            {"label":"TUT", "value": 19},
            {"label":"NE", "value": 20},
            {"label":"RE", "value": 21}
            ],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value=3, # Cambiamos Value a Chotacabras cuellirrojo como default, asi el usuario ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"} # Style: Cambia el estilo en general del Desplegable (width: Ancho)
        ),
    html.Div(id="output_container2", children= [])
])                

# Conecta Los Graficos de Plotly con Los Componentes Dash
@app.callback( # Define Los Inputs y Outputs de la funcion update_graph (Actualizar Grafico)
    [Output (component_id='output_container', component_property='children'), # Output 1: Texto debajo del desplegable
    Output (component_id='superstore_map', component_property='figure'),
    Output (component_id='output_container2', component_property='children'),
    Output ('img1', 'src'),  Output('texto1', 'children'),
    Output ('img2', 'src'),  Output('texto2', 'children'),
    Output ('img3', 'src'),  Output('texto3', 'children'),
    Output ('img4', 'src'),  Output('texto4', 'children'),
    Output ('img5', 'src'),  Output('texto5', 'children'),
    Output ('img6', 'src'),  Output('texto6', 'children')], 
    [Input (component_id='slct_nombre_comun', component_property='value'),
     Input (component_id='slct_leyen_amenaza', component_property='value')] 
    )

def update_graph (option_slctd, option_leyen):
    print(option_slctd) # Imprimimos a consola La opcion del usuario,
    print(type (option_slctd)) # y el tipo de la opcion (best practices).
    print(option_leyen)
    print(type(option_leyen))
    
    container="El ave seleccionada es: {}".format(option_slctd) # Cambiamos el texto debajo del desplegable al Año introducido
    leyenda=leyen_amen['Leyenda'].iloc[option_leyen]
    significado=leyen_amen['Significado'].iloc[option_leyen]
    container2=f'{leyenda}'+' es igual a '+f'{significado}'
    
    dff = df.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original.
    dff = dff[dff["nombre_comun&cientifico"] == option_slctd].reset_index() # Filtramos La nueva DataFrame por ave seleccionada, asi tenemos solo el ave que buscamos.
       
    if dff['GLOBAL UICN RED LIST (consulta 2022)'][0]!='NP':
        global_cat = dff['GLOBAL UICN RED LIST (consulta 2022)'][0]
        titulo = 'La amenaza del '+f'{option_slctd}'+' a nivel global es'+' '+f'{global_cat}'
    else:
        titulo = 'No hay categorización a nivel global'
   

    #Plotly Express
    #Creamos el Mapa
    colorscale = [ "rgb(210, 231, 154)", "rgb(94, 179, 39)", "rgb(255, 51, 51)"]
    fig = px.choropleth_mapbox(
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
        )
    )

    imagen1, texto1, imagen2, texto2 = selectImgs(dff, 'Lista Roja 2004 Canarias', 'Lista Roja 2021 Canarias')
    imagen3, texto3, imagen4, texto4 = selectImgs(dff, 'Lista Roja 2004 Península', 'Lista Roja 2021 Reproductoras Península')
    imagen5, texto5, imagen6, texto6 = selectImgs(dff, 'Lista Roja 2004 Península', 'Lista Roja 2021 Migratorias')
    return container, fig, container2, app.get_asset_url(imagen1), texto1, app.get_asset_url(imagen2), texto2, app.get_asset_url(imagen3), texto3, app.get_asset_url(imagen4), texto4, app.get_asset_url(imagen5), texto5, app.get_asset_url(imagen6), texto6 # Retornar Los Objetos que hemos creado

# IMPORTANTE: Retornar Los valores en el mismo orden que pusiste en Los Outputs!

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
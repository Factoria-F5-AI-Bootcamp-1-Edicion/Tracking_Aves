import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
import folium.plugins as plugins
from dash import dcc, html
import os

from app import app
import layouts
from dash import Input, Output
from seleccionar_img import selectImgs
from crea_mapa import creaMapa

df = pd.read_csv('./app/data/aves_df.csv') # Cargamos dataset de aves
planes = pd.read_csv('./app/data/planes_aves.csv') # Cargamos dataset de planes

leyen_amen = pd.read_csv('./app/data/leyendas_amenaza.csv') # Cargamos dataset de leyendas de amenaza
leyen_plan = pd.read_csv('./app/data/leyendas_planes.csv') # Cargamos dataset de leyendas de amenaza

f = r"./app/data/Espana_y_comunidades.shp"
shapes = gpd.read_file(f) # Cargamos las geometrías de las Comunidades Autónomas (CCAA)

@app.callback( # Define Los Inputs y Outputs de la funcion first_callback()
    [Output (component_id='output_container', component_property='children'), # Output 1: Texto debajo del desplegable
    Output (component_id='superstore_map', component_property='figure'), # Mapa de ubicación del ave seleccionada
    Output (component_id='output_container2', component_property='children'), # Texto del significado de la leyenda
    Output ('img1', 'src'),  Output('texto1', 'children'), # Imágenes de pajaros de colores, en función de la lista roja.
    Output ('img2', 'src'),  Output('texto2', 'children'),
    Output ('img3', 'src'),  Output('texto3', 'children'),
    Output ('img4', 'src'),  Output('texto4', 'children'),
    Output ('img5', 'src'),  Output('texto5', 'children'),
    Output ('img6', 'src'),  Output('texto6', 'children')], 
    [Input (component_id='slct_nombre_comun', component_property='value'), # Input 1: Desplegable para seleccionar ave
     Input (component_id='slct_leyen_amenaza', component_property='value')] # INput 2: Desplegable para seleccionar leyenda
    )

def first_callback(option_slctd, option_leyen): # Función para actuaizar el mapa, las imágenes de colores de pajaritos y el significado de la leyenda.
    print(option_slctd) # Imprimimos a consola La opcion del usuario,
    print(type (option_slctd)) # y el tipo de la opcion (best practices).
    print(option_leyen)
    print(type(option_leyen))
    
    #---------Creamos container y container2
    container="El ave seleccionada es: {}".format(option_slctd) # Cambiamos el texto debajo del desplegable al ave seleccionada
    leyenda=leyen_amen['Leyenda'].iloc[option_leyen] # Seleccionamos la leyenda elegida
    significado=leyen_amen['Significado'].iloc[option_leyen] # Seleccionamos el significado de la leyenda
    container2=f'{leyenda}'+' es igual a '+f'{significado}' # Texto de significado correspondiente a leyenda.
    
    dff = df.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original.
    dff = dff[dff["nombre_comun&cientifico"] == option_slctd].reset_index() # Filtramos La nueva DataFrame por ave seleccionada, asi tenemos solo el ave que buscamos.
       
    if dff['GLOBAL UICN RED LIST (consulta 2022)'][0]!='NP': # Si el ave tiene categoría global
        global_cat = dff['GLOBAL UICN RED LIST (consulta 2022)'][0] # Seleccionamos la categoría global
        titulo = 'La amenaza del '+f'{option_slctd}'+' a nivel global es'+' '+f'{global_cat}' # Devolvemos un título que indique la amenaza a nivel global.
    else:
        titulo = 'No hay categorización a nivel global' # Si el ave no tiene categoría a nivel global, se devuelve este texto.
   
    #---------Creamos el Mapa
    colorscale = [ "rgb(210, 231, 154)", "rgb(94, 179, 39)", "rgb(255, 51, 51)"] # Colores que usaremos para el mapa.
    fig = px.choropleth_mapbox(
        geojson=shapes.geometry, # Utilizamos las geometrías que cargamos al comienzo.
        data_frame=dff, # Definimos La DataFrame con nuestra copia
        locations=dff.index_ciudad, # Cambiamos Las Localizaciones para que  nuestra columna de 'index_ciudad' para que sepa qué comunidad es(Números, no nombres)
        color='NIVEL AMENAZA', # Definimos esta variable para cambiar La Columna que usa como referencia para añadir colores.
        hover_name='Ubicacion', # El título del cuadro informativo que aparece al pasar el ratón, en este caso la Comunidad Autónoma.
        hover_data=['Categoría_Regional', 'CEEA y LESRPE', 'Coincide_con_categoría_en_LR'], # Datos que se muestran en el cuadro informativo.
        labels={0 : 'Sin datos suficientes', 1: 'Amenaza Leve', 2 : 'Amenaza Media', 3 : 'Amenaza Grave', 4 :'Amenaza Muy Grave'} ,
        color_continuous_scale=colorscale, # La escala de color, usaremos los que definimos arriba en 'colorscale'.
        color_continuous_midpoint=1,
        mapbox_style='stamen-watercolor', # Estilo del mapa, hemos puesto este que es un mapa de acuarela. Otras posibilidad más seria: 'carto-positron'
        title=titulo,  # Título de la figura
        zoom=4, 
        center = {"lat": 39.6, "lon": -4},
        opacity=0.5, # Definimos la opacidad que aparezerán al pasar el ratón sobre una ccaa.
    )
    fig.update_layout( # Ajustamos el tamaño y las proporciones del mapa.
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

    imagen1, texto1, imagen2, texto2 = selectImgs(dff, 'Lista Roja 2004 Canarias', 'Lista Roja 2021 Canarias') # Utilizamos la función selecImgs del archivo seleccionar_img.
    imagen3, texto3, imagen4, texto4 = selectImgs(dff, 'Lista Roja 2004 Península', 'Lista Roja 2021 Reproductoras Península')
    imagen5, texto5, imagen6, texto6 = selectImgs(dff, 'Lista Roja 2004 Península', 'Lista Roja 2021 Migratorias')
    return container, fig, container2, app.get_asset_url(imagen1), texto1, app.get_asset_url(imagen2), texto2, app.get_asset_url(imagen3), texto3, app.get_asset_url(imagen4), texto4, app.get_asset_url(imagen5), texto5, app.get_asset_url(imagen6), texto6 # Retornar Los Objetos que hemos creado
               # Devolvemos los containers, el mapa y las imágenes. 
               # NOTA: Las imágenes deben estar en la carpeta assets/ para que las lea la función .get_asset_url

#-------------------------------Primer Callback: Página 1. Situación de aves------------------------------
@app.callback(
    Output (component_id='planes_si_no', component_property='children'), # La salida es un objeto html.
    [Input (component_id='slct_hay_plan', component_property='value')] # El Input es el dropdown donde seleccionamos que planes queremos ver.
    )
# Función para crear los mapas de planes.
def muestraPlanes(value):
    print(value)
    print(type(value))
    os.makedirs('./app/mapas', exist_ok = True)
    if value == 'SI': # Si seleccionamos 'Con el correspondiente plan':
        planes_elegidos = planes.copy() 
        planes_elegidos = planes_elegidos[planes_elegidos["HAY_PLAN"] == value] # Seleccionamos los datos de todos los planes activos.
        color_si_hay = '#00FF00' # Color verde
        creaMapa(planes_elegidos, color_si_hay, 'si_planes') # Creamos el mapa de planes activos
        planes_caducados = planes.copy()
        planes_caducados = planes_caducados[planes_caducados["Caducado"] == 'SI'] # Seleccionamos los datos de planes activos caducados.
        color_caducados = '#FF0000'
        creaMapa(planes_caducados, color_caducados, 'planes_caducados')
        planes_vigentes = planes.copy()
        planes_vigentes = planes_vigentes[planes_vigentes["Caducado"] == 'NO'] # Seleccionamos los datos de planes activos vigentes.
        color_vigentes = '#00FF00'
        creaMapa(planes_vigentes, color_vigentes, 'planes_vigentes')
        return html.Div([ # Devuelve un objeto html con los 3 mapas creados.
            html.Iframe(srcDoc=open('./app/mapas/si_planes.html', 'r').read(), width='100%', height='500px'),
            html. Br(),
            dcc.Tabs([
                dcc.Tab(
                    label="Planes Caducados (+5 años)",
                    children=[html.Iframe(srcDoc=open('./app/mapas/planes_caducados.html', 'r').read(), width='100%', height='500px')]
                ),
                dcc.Tab(
                    label="Planes Vigentes",
                    children=[html.Iframe(srcDoc=open('./app/mapas/planes_vigentes.html', 'r').read(), width='100%', height='500px')]
                ),
            ],style={'float': 'right','margin': 'auto'} # 'float': 'right','margin': 'auto' -- 'width': '49%', 'display': 'inline-block'
            )
        ])
    else: # Si seleccionamos 'Sin el correspondiente plan'
        planes_elegidos = planes.copy() 
        planes_elegidos = planes_elegidos[planes_elegidos["HAY_PLAN"] == value] # Seleccionamos los datos de planes que faltan.
        color_no_hay = '#FF0000' # Color rojo
        creaMapa(planes_elegidos, color_no_hay, 'no_planes') # Creamos el mapa de planes que faltan.
        return html.Iframe(srcDoc=open('./app/mapas/no_planes.html', 'r').read(), width='100%', height='500px') # Devuelve un objeto html con el mapa de folium,

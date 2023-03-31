import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
import folium.plugins as plugins

from app import app
import layouts
from dash import Input, Output
from seleccionar_img import selectImgs

df = pd.read_csv('./data_raw/aves_df.csv')
planes = pd.read_csv('./data_raw/planes_aves.csv')

leyen_amen = pd.read_csv('./leyendas/leyendas_amenaza.csv')
leyen_plan = pd.read_csv('./leyendas/leyendas_planes.csv')

f = r"ESP/Espana_y_comunidades.shp"
shapes = gpd.read_file(f)

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

def first_callback(option_slctd, option_leyen):
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

@app.callback(
    [Output (component_id='mapa_planes', component_property='srcDoc')],
    [Input (component_id='slct_hay_plan', component_property='value')]
    )

def second_callback(value):
    print(value) # Imprimimos a consola La opcion del usuario,
    print(type (value))

    planes_elegidos = planes.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original.
    planes_elegidos = planes_elegidos[planes_elegidos["HAY_PLAN"] == value]

    def cuentaTotalPlanes(data):
        total_planes_ciudad = []
        for i in data['Ubicacion'].unique():
            x = len(data[data['Ubicacion']==i])
            total_planes_ciudad.append(x)
        return total_planes_ciudad

    mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
    total = cuentaTotalPlanes(planes_elegidos)
    for index, row in planes_elegidos.iterrows():
        ciudad = row["Ubicacion"]
        latitud = row["lat"]
        longitud = row["lon"]
        
        # Crear un marcador de burbuja para la ciudad
        burbuja = folium.CircleMarker(location=[latitud, longitud],
                                    radius=total,
                                    color='#3186cc',
                                    fill=True,
                                    fill_color='#3186cc')
        
        # Agregar el número de etiqueta encima de la burbuja
        folium.Marker([latitud, longitud], icon=plugins.BeautifyIcon(
                            icon="arrow-down", icon_shape="marker",
                            number=5,
                            border_color= '#3186cc',
                            background_color='#3186cc'
                        )
                    ).add_to(mapa)
        
        # Agregar la burbuja al mapa
        burbuja.add_to(mapa)
    map.save("../map_1.html")

    return open('../map_1.html', 'r').read()
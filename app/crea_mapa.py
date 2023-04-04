import folium
import folium.plugins as plugins

#----------------------Función para crear mapas de folium-------------------
def creaMapa(dataframe, color_burbujas, nombre): # Los argumentos serán el dataframe, el color para las burbujas (marcadores), y el nombre del archivo del mapa.
    mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6) # Creamos un mapa de folium, con localización en España.
    folium.TileLayer('stamenwatercolor').add_to(mapa) # Ledamos estilo de 'watercolor' al mapa creado
    for index, row in dataframe.iterrows(): # Recorremos las filas del dataframe.
                ciudad = row["Ubicacion"]
                latitud = row["lat"]
                longitud = row["lon"]
                misma_ciudad = dataframe[dataframe['Ubicacion']==ciudad] # Seleccionamos los datos de las aves de los planes de una misma ciudad.
                aves_ciudad = misma_ciudad['Nombre científico'].to_list() # # Seleccionamos los nombres científicos las aves de los planes de una misma ciudad.
                text = "<br>".join(aves_ciudad) # Unimos los nombres con <br>, que indica un salto de línea después de cada nombre.
                total = len(dataframe[dataframe['Ubicacion']==ciudad]) # Total de planes de cada ciudad
                # Crear un marcador de burbuja para la ciudad
                burbuja = folium.CircleMarker(location=[latitud, longitud],
                                            radius=total, # Radio de la burbuja, basado en el Total
                                            color=color_burbujas,
                                            fill=True,
                                            fill_color=color_burbujas,
                                            tooltip=f"{text}" # Información que aparece al pasar el ratón por encima.
                                            )
                
                # Agregar el número de etiqueta encima de la burbuja
                folium.Marker([latitud, longitud], tooltip=f'{ciudad}', # Información que aparece al pasar el ratón por encima.
                                icon=plugins.BeautifyIcon(
                                    icon="arrow-down", icon_shape="marker",
                                    number=total,
                                    border_color= color_burbujas,
                                    background_color=color_burbujas
                                )
                            ).add_to(mapa)
                
                # Agregar la burbuja al mapa
                burbuja.add_to(mapa) # Añadimos los marcadores al mapa
    mapa.save(f"./app/mapas/{nombre}.html") # Guardamos el mapa como html en la carpeta mapas/
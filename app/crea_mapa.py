import folium
import folium.plugins as plugins

def creaMapa(dataframe, color_burbujas, nombre):
    mapa = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
    folium.TileLayer('stamenwatercolor').add_to(mapa)
    for index, row in dataframe.iterrows():
                ciudad = row["Ubicacion"]
                latitud = row["lat"]
                longitud = row["lon"]
                misma_ciudad = dataframe[dataframe['Ubicacion']==ciudad]
                aves_ciudad = misma_ciudad['Nombre científico'].to_list()
                text = "<br>".join(aves_ciudad)
                total = len(dataframe[dataframe['Ubicacion']==ciudad])
                # Crear un marcador de burbuja para la ciudad
                burbuja = folium.CircleMarker(location=[latitud, longitud],
                                            radius=total,
                                            color=color_burbujas,
                                            fill=True,
                                            fill_color=color_burbujas,
                                            tooltip=f"{text}"
                                            )
                
                # Agregar el número de etiqueta encima de la burbuja
                folium.Marker([latitud, longitud], tooltip=f'{ciudad}', icon=plugins.BeautifyIcon(
                                    icon="arrow-down", icon_shape="marker",
                                    number=total,
                                    border_color= color_burbujas,
                                    background_color=color_burbujas
                                )
                            ).add_to(mapa)
                
                # Agregar la burbuja al mapa
                burbuja.add_to(mapa)
    mapa.save(f"./mapas/{nombre}.html")
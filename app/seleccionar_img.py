import pandas as pd
import numpy as np

#---------------Función para seleccionar imágenes de pajaritos de colores---------------
def selectImg(df, nombreLR): # Los argumentos serán el dataframe y el nombre de la columna de Lista Roja elegida.
    categoria = df[nombreLR][0] # Seleccionamos la categoría del ave introducida, en la Lisa Roja introducida.
    texto = f'{nombreLR}'+f': {categoria}' # Generamos un teto que indique la Lista Roja y la Categoría.
    if df[nombreLR][0] == 'NE':
        imagen = 'NE.png' # Dependiendo de la categoría se seleecionará una imagen, las imágenes están en assets/
    elif df[nombreLR][0] == 'DD':
        imagen = 'DD.png'
    elif df[nombreLR][0] == 'LC':
        imagen = 'LC.png'
    elif df[nombreLR][0] == 'NT':
        imagen = 'NT.png'
    elif df[nombreLR][0] == 'VU':
        imagen = 'VU.png'
    elif df[nombreLR][0] == 'EN':
        imagen = 'EN.png'
    elif df[nombreLR][0] == 'EW':
        imagen = 'EW.png'
    elif df[nombreLR][0] == 'RE':
        imagen = 'RE.png'
    elif df[nombreLR][0] == 'CR':
        imagen = 'CR.png'
    elif df[nombreLR][0] == 'EX':
        imagen = 'EX.png'
    else:
        imagen = 'NP.png'
        texto = f'Sin datos' # Si el ave seleccionada no tiene datos en la lista Roja seleccionada, se imprimirá esto.
    return imagen, texto

#-------------------Función para generar comparativa entre Listas Rojas de 2004 y 2021-------------
def selectImgs(df, nombreLR1, nombreLR2):
    img1, text1 = selectImg(df, nombreLR1) # Utiliza la función de arriba
    img2, text2 = selectImg(df, nombreLR2)
    return img1, text1, img2, text2

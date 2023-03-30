import pandas as pd
import numpy as np

'''aves_df = pd.read_csv('./data_raw/aves_df.csv')

option_slctd = 'Vencejo moro-Apus affinis'

dff = aves_df.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original.
dff = dff[dff["nombre_comun&cientifico"] == option_slctd].reset_index()'''


def selectImg(df, nombreLR):
    categoria = df[nombreLR][0]
    texto = 'Situación en '+f'{nombreLR}'+f' : {categoria}'
    if df[nombreLR][0] == 'NE':
        imagen = 'NE.png'
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
        imagen = 'paj.jpg'
        texto = f'No hay datos sobre la situación de esta ave en {categoria}'
    return imagen, texto

def selectImgs(df, nombreLR1, nombreLR2):
    img1, text1 = selectImg(df, nombreLR1)
    img2, text2 = selectImg(df, nombreLR2)
    return img1, text1, img2, text2

#selectImgs(dff, 'LR2004_PENINSULA', 'LR2021_REPROD_PENINSULA')
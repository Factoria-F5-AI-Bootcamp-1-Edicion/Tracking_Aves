import pandas as pd
import numpy as np

def selectImg(df, nombreLR):
    categoria = df[nombreLR][0]
    texto = 'Situación en '+f'{nombreLR}'+f': {categoria}'
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
        imagen = 'NP.png'
        texto = f'No hay datos sobre la situación de esta ave en {nombreLR}'
    return imagen, texto

def selectImgs(df, nombreLR1, nombreLR2):
    img1, text1 = selectImg(df, nombreLR1)
    img2, text2 = selectImg(df, nombreLR2)
    return img1, text1, img2, text2

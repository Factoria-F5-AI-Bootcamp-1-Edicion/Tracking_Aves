from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from app import app

df = pd.read_csv('./data_raw/aves_df.csv')
planes = pd.read_csv('./data_raw/planes_aves.csv')

NAVBAR_STYLE = { # Estilo del navegador lateral.
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#3daee3",
}

CONTENT_STYLE = { # Estilo del contenido de la página.
    "top":0,
    "margin-top":'2rem',
    "margin-left": "18rem",
    "margin-right": "2rem",
}

#-----------------------Función para crear eL Navegador Lateral-------------------------
def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = html.Div(
        [
            html.Img(src=app.get_asset_url('seo_logo.png'), style={'display': 'block', # Imagen del logo de SEO.
                                                                    'margin-left': 'auto',
                                                                    'margin-right': 'auto',
                                                                    'width': '50%'}),
            html.H4("¿Qué deseas ver?", className="display-10",style={'textAlign':'center'}), # Texto principal.
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Página Principal ", href="/",active="exact", external_link=True, className="page-link"), # Link 1
                    html. Br(),
                    dbc.NavLink("Situacion de aves ", href="/aves",active="exact", external_link=True, className="page-link"), # Link 2
                    html. Br(),
                    dbc.NavLink("Planes de acción ", href="/planes", active="exact", external_link=True, className="page-link") # Link 3
                ],
                pills=True, # Permite utilizar archivo CSS de la carpeta assets/ para el diseño de los links.
                vertical=True # Los links se colocan en vertical.
            ),
        ],
    style=NAVBAR_STYLE # Utilizamos el estilo definido al principio para el navegador lateral.
    )  
    return navbar

#---------------------------Diseño PÁGINA 1: Página Principal----------------------------------
page1_layout = html.Div([ 
    html.Img(src=app.get_asset_url('Portada.png'), style={'display': 'block', # Portada
                                                                    'margin-left': 'scale_factor',
                                                                    'margin-right': 'scale_factor',
                                                                    'width': '100%'})
                        ])
 
#---------------------------Diseño PÁGINA 2: Situación de Aves----------------------------------
page2_layout = html.Div([ # Definimos el diseño de La Pagina HTML donde correrá nuestro programa.
    html.H1("Situación de las aves en peligro de España", style={'text-align' : 'center'}), # Título
    dcc.Dropdown (id="slct_nombre_comun", # Crea el Desplegable
        options=df['nombre_comun&cientifico'], # Las opciones son odos los nombres comunes y científicos.
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value='Abubilla común-Upupa epops', # Cambiamos Value a Abubilla común-Upupa epops como default, asi la usuaria ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"} 
        ),
    html.Div(id="output_container", children= []), # Crea un bloque de texto debajo del Desplegable y crea una variable hija.
    html. Br(), # Espacio en blanco.
    dcc.Graph(id='superstore_map', figure={}, style={'float': 'right','margin': 'auto'}), # Espacio para la figura del mapa.
    dcc.Tabs( # Creamos las tablas para las imágenes de los pajaritos de colores.
        id="tabs_comparacion",
        value="tab-1", # Valor por defeco, así la usuaria ve una tabla al entrar.
        children=[
            dcc.Tab(
                label="Canarias 2004 & 2021", # Título de la tabla 1
                value="tab-1",
                children=[html.H5(id='texto1'), # Texto del pajarito
                          html.Img(id='img1', style={'display': 'inline-block', 'width': '20%'}), # Imagen del pajarito.
                          html.H5(id='texto2'),
                          html.Img(id='img2', style={'display': 'inline-block', 'width': '20%'})]
            ),
            dcc.Tab(
                label="Península Reproductoras 2004 & 2021",
                value="tab-2",
                children=[html.H5(id='texto3'),
                          html.Img(id='img3', style={'display': 'inline-block', 'width': '20%'}),
                          html.H5(id='texto4'),
                          html.Img(id='img4', style={'display': 'inline-block', 'width': '20%'})]
            ),
            dcc.Tab(
                label="Península Migratorias 2004 & 2021",
                value="tab-3",
                children=[html.H5(id='texto5'),
                          html.Img(id='img5', style={'display': 'inline-block', 'width': '20%'}),
                          html.H5(id='texto6'),
                          html.Img(id='img6', style={'display': 'inline-block', 'width': '20%'})]
            )
        ],style={'float': 'right','margin': 'auto'} 
    ),
    html. Br(), # Espacio en blanco.
    dcc.Dropdown (id="slct_leyen_amenaza", # Crea el Desplegable
        options=[# Lista de opciones para el Desplegable (Label: Valor que aparece para el usuario || Value: Valor interno
            {"label": "(EN)", "value": 0}, # Lo que ve la usuaria es la leyenda de la que quiere conocer el significado.
            {"label":"EN*", "value": 1},   # El valor interno es el índice de esa leyenda.
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
        multi=False, 
        value=3, # Cambiamos Value a 3 como default, asi la usuario ya tiene un significado de leyenda.
        clearable=False, 
        searchable=True, 
        style={"width": "60%"} 
        ),
    html.Div(id="output_container2", children= []) # Contenedor del texto debajo del desplegable de leyendas.
]) 

#---------------------------Diseño PÁGINA 3: Planes de Acción----------------------------------
page3_layout = html.Div([
    html.H1("Planes de protección de Aves de España", style={'text-align' : 'center'}), # Título
    dcc.Dropdown(
        options=[
            {"label": "Sin el correspondiente plan", "value": 'NO'}, 
            {"label":"Con el correspondiente plan", "value": 'SI'}
        ],
        multi=False, 
        value='NO',
        clearable=False,
        searchable=True,
        style={"width": "60%"},
        id='slct_hay_plan'
    ),
    html.Div(id='planes_si_no',style=CONTENT_STYLE) # Objeto html donde se verán los mapas de planes seleccionados.
])

from dash import Dash, dcc, html, Input, Output
import pandas as pd

df = pd.read_csv('./data_raw/aves_df.csv')
planes = pd.read_csv('./data_raw/planes_aves.csv')

page1_layout = html.Div([ # Definimos el diseño de La Pagina HTML donde correrá nuestro programa.
    html.H1("Situación de las aves amenazas de España", style={'text-align' : 'center'}), # Crea La Cabecera de la pagina HTML
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
        id="tabs_comparacion",
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

page2_layout = html.Div([
    html.H1("Planes de protección de Aves de España", style={'text-align' : 'center'}),
    dcc.Dropdown(
        options=[
            {"label": "Sin el correspondiente plan", "value": 'NO'}, #Como que el valor Value es un año,
            {"label":"Con el correspondiente plan", "value": 'SI'}
        ],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value='NO', # Cambiamos Value a Chotacabras cuellirrojo como default, asi el usuario ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"}
    ),
    dcc.Graph(id='mapa_planes', figure={})
])

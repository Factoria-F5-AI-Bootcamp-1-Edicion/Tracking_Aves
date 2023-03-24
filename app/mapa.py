import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import folium

df = pd.read_csv('./data_raw/Dataset_definitivo_con_geometrias.csv')
total_aves_0 = pd.read_csv('./data_raw/total_aves_0.csv')
total_aves_1 = pd.read_csv('./data_raw/total_aves_1.csv')
total_aves_2 = pd.read_csv('./data_raw/total_aves_2.csv')
total_aves_3 = pd.read_csv('./data_raw/total_aves_3.csv')
total_aves_4 = pd.read_csv('./data_raw/total_aves_4.csv')


f = r"ESP/Espana_y_comunidades.shp"
shapes = gpd.read_file(f)
punto = r"ESP/puntos_ciudades_espana.gpkg"
mapapuntos = gpd.read_file(punto)

app = Dash(__name__) # inicializamos Dash

#App Layout
app.layout = html.Div([        # Definimos el diseño de La Pagina HTML donde correrá nuestro programa.
    html.H1("Web Pajaritos Dash", style={'text-align' : 'center'}), # Crea La Cabecera de la pagina HTML
    dcc.Dropdown (id="slct_nombre_comun", # Crea el Desplegable
        options=[# Lista de opciones para el Desplegable (Label: Valor que aparece para el usuario || Value: Valor inte
            {"label": "Abejaruco europeo", "value": "Abejaruco europeo"}, #Como que el valor Value es un año,
            {"label":"Abejero europeo", "value": "Abejero europeo"},
            {"label":"Abubilla común", "value": "Abubilla común"},
            {"label":"Acentor alpino", "value": "Acentor alpino"},
            {"label":"Acentor común", "value": "Acentor común"}, # podemos dejar el valor interno
            {"label":"Agachadiza chica", "value": "Agachadiza chica"}, 
            {"label":"Agachadiza común", "value": "Agachadiza común"},
            {"label":"Agateador euroasiático", "value": "Agateador euroasiático"},
            {"label":"Agateador europeo", "value": "Agateador europeo"},
            {"label":"Águila calzada", "value": "Águila calzada"},
            {"label":"Águila imperial ibérica", "value": "Águila imperial ibérica"},
            {"label":"Águila perdicera", "value": "Águila perdicera"},
            {"label":"Águila pescadora", "value": "Águila pescadora"},
            {"label":"Águila real", "value": "Águila real"},
            {"label":"Aguilucho cenizo", "value": "Aguilucho cenizo"}, 
            {"label":"Aguilucho lagunero occidental", "value": "Aguilucho lagunero occidental"},
            {"label":"Aguilucho pálido", "value": "Aguilucho pálido"},
            {"label":"Aguilucho papialbo", "value": "Aguilucho papialbo"},
            {"label":"Aguja colinegra", "value": "Aguja colinegra"},
            {"label":"Aguja colipinta", "value": "Aguja colipinta"},
            {"label":"Alcatraz atlántico", "value": "Alcatraz atlántico"},
            {"label":"Alcaudón chico", "value": "Alcaudón chico"},
            {"label":"Alcaudón común", "value": "Alcaudón común"},
            {"label":"Alcaudón norteño", "value": "Alcaudón norteño"},
            {"label":"Alcaudón real", "value": "Alcaudón real"},
            {"label":"Alcotán europeo", "value": "Alcotán europeo"},
            {"label":"Alimoche común", "value": "Alimoche común"},
            {"label":"Alondra común", "value": "Alondra común"},
            {"label":"Alondra ricotí", "value": "Alondra ricotí"},
            {"label":"Alondra totovía", "value": "Alondra totovía"},
            {"label":"Alzacola rojizo", "value": "Alzacola rojizo"},
            {"label":"Ánade azulón", "value": "Ánade azulón"},
            {"label":"Ánade friso", "value": "Ánade friso"},
            {"label":"Ánade rabudo norteño", "value": "Ánade rabudo norteño"},
            {"label":"Andarríos bastardo", "value": "Andarríos bastardo"},
            {"label":"Andarríos chico", "value": "Andarríos chico"},
            {"label":"Andarríos grande", "value": "Andarríos grande"},
            {"label":"Ánsar común", "value": "Ánsar común"},
            {"label":"Ánsar piquicorto", "value": "Ánsar piquicorto"},
            {"label":"Arao común", "value": "Arao común"},
            {"label":"Archibebe claro", "value": "Archibebe claro"},
            {"label":"Archibebe común", "value": "Archibebe común"},
            {"label":"Archibebe fino", "value": "Archibebe fino"},
            {"label":"Archibebe oscuro", "value": "Archibebe oscuro"},
            {"label":"Arrendajo euroasiático", "value": "Arrendajo euroasiático"},
            {"label":"Autillo europeo", "value": "Autillo europeo"},
            {"label":"Avefría europea", "value": "Avefría europea"},
            {"label":"Avetorillo común", "value": "Avetorillo común"},
            {"label":"Avetoro común", "value": "Avetoro común"},
            {"label":"Avión común occidental", "value": "Avión común occidental"},
            {"label":"Avión roquero", "value": "Avión roquero"},
            {"label":"Avión zapador", "value": "Avión zapador"},
            {"label":"Avoceta común", "value": "Avoceta común"},
            {"label":"Avutarda euroasiática", "value": "Avutarda euroasiática"},
            {"label":"Avutarda hubara africana", "value": "Avutarda hubara africana"},
            {"label":"Azor común", "value": "Azor común"},
            {"label":"Bigotudo", "value": "Bigotudo"},
            {"label":"Bisbita alpino", "value": "Bisbita alpino"},
            {"label":"Bisbita caminero", "value": "Bisbita caminero"},
            {"label":"Bisbita campestre", "value": "Bisbita campestre"},
            {"label":"Bisbita costero", "value": "Bisbita costero"},
            {"label":"Bisbita de Richard", "value": "Bisbita de Richard"},
            {"label":"Bisbita gorgirrojo", "value": "Bisbita gorgirrojo"},
            {"label":"Bisbita pratense", "value": "Bisbita pratense"},
            {"label":"Búho campestre", "value": "Búho campestre"},
            {"label":"Búho chico", "value": "Búho chico"},
            {"label":"Búho real", "value": "Búho real"},
            {"label":"Buitre leonado", "value": "Buitre leonado"},
            {"label":"Buitre negro", "value": "Buitre negro"},
            {"label":"Busardo ratonero", "value": "Busardo ratonero"},
            {"label":"Buscarla pintoja", "value": "Buscarla pintoja"},
            {"label":"Buscarla unicolor", "value": "Buscarla unicolor"},
            {"label":"Calamón común", "value": "Calamón común"},
            {"label":"Calandria común", "value": "Calandria común"},
            {"label":"Camachuelo trompetero", "value": "Camachuelo trompetero"},
            {"label":"Canastera común", "value": "Canastera común"},
            {"label":"Cárabo común", "value": "Cárabo común"},
            {"label":"Carbonero garrapinos", "value": "Carbonero garrapinos"},
            {"label":"Carbonero palustre", "value": "Carbonero palustre"},
            {"label":"Carraca europea", "value": "Carraca europea"},
            {"label":"Carricerín cejudo", "value": "Carricerín cejudo"},
            {"label":"Carricerín común", "value": "Carricerín común"},
            {"label":"Carricerín real", "value": "Carricerín real"},
            {"label":"Carricero común", "value": "Carricero común"},
            {"label":"Carricero tordal", "value": "Carricero tordal"},
            {"label":"Cerceta carretona", "value": "Cerceta carretona"},
            {"label":"Cerceta común", "value": "Cerceta común"},
            {"label":"Cerceta pardilla", "value": "Cerceta pardilla"},
            {"label":"Cernícalo patirrojo", "value": "Cernícalo patirrojo"},
            {"label":"Cernícalo primilla", "value": "Cernícalo primilla"},
            {"label":"Cetia ruiseñor", "value": "Cetia ruiseñor"},
            {"label":"Charrán ártico", "value": "Charrán ártico"},
            {"label":"Charrán bengalí", "value": "Charrán bengalí"},
            {"label":"Charrán común", "value": "Charrán común"},
            {"label":"Charrán patinegro", "value": "Charrán patinegro"},
            {"label":"Charrán rosado", "value": "Charrán rosado"},
            {"label":"Charrancito común", "value": "Charrancito común"},
            {"label":"Chocha perdiz", "value": "Chocha perdiz"},
            {"label":"Chochín paleártico", "value": "Chochín paleártico"},
            {"label":"Chorlitejo chico", "value": "Chorlitejo chico"},
            {"label":"Chorlitejo grande", "value": "Chorlitejo grande"},
            {"label":"Chorlitejo patinegro", "value": "Chorlitejo patinegro"},
            {"label":"Chorlito carambolo", "value": "Chorlito carambolo"},
            {"label":"Chorlito dorado europeo", "value": "Chorlito dorado europeo"},
            {"label":"Chorlito gris", "value": "Chorlito gris"},
            {"label":"Chotacabras cuellirrojo", "value": "Chotacabras cuellirrojo"},
            {"label":"Chotacabras europeo", "value": "Chotacabras europeo"},
            {"label":"Chova piquigualda", "value": "Chova piquigualda"},
            {"label":"Chova piquirroja", "value": "Chova piquirroja"},
            {"label":"Cigüeña blanca", "value": "Cigüeña blanca"},
            {"label":"Cigüeñuela común", "value": "Cigüeñuela común"},
            {"label":"Cistícola buitrón", "value": "Cistícola buitrón"},
            {"label":"Codorniz común", "value": "Codorniz común"},
            {"label":"Cogujada común", "value": "Cogujada común"},
            {"label":"Cogujada montesina", "value": "Cogujada montesina"},
            {"label":"Colimbo ártico", "value": "Colimbo ártico"},
            {"label":"Colimbo chico", "value": "Colimbo chico"},
            {"label":"Colimbo grande", "value": "Colimbo grande"},
            {"label":"Colirrojo real", "value": "Colirrojo real"},
            {"label":"Colirrojo tizón", "value": "Colirrojo tizón"},
            {"label":"Collalba gris", "value": "Collalba gris"},
            {"label":"Collalba negra", "value": "Collalba negra"},
            {"label":"Collalba rubia", "value": "Collalba rubia"},
            {"label":"Combatiente", "value": "Combatiente"},
            {"label":"Cormorán grande", "value": "Cormorán grande"},
            {"label":"Corneja negra", "value": "Corneja negra"},
            {"label":"Corredor sahariano", "value": "Corredor sahariano"},
            {"label":"Correlimos canelo", "value": "Correlimos canelo"},
            {"label":"Correlimos común", "value": "Correlimos común"},
            {"label":"Correlimos gordo", "value": "Correlimos gordo"},
            {"label":"Correlimos menudo", "value": "Correlimos menudo"},
            {"label":"Correlimos oscuro", "value": "Correlimos oscuro"},
            {"label":"Correlimos pectoral", "value": "Correlimos pectoral"},
            {"label":"Correlimos tridáctilo", "value": "Correlimos tridáctilo"},
            {"label":"Correlimos zarapitín", "value": "Correlimos zarapitín"},
            {"label":"Críalo europeo", "value": "Críalo europeo"},
            {"label":"Cuchara común", "value": "Cuchara común"},
            {"label":"Cuco común", "value": "Cuco común"},
            {"label":"Culebrera europea", "value": "Culebrera europea"},
            {"label":"Curruca balear", "value": "Curruca balear"},
            {"label":"Curruca cabecinegra", "value": "Curruca cabecinegra"},
            {"label":"Curruca capirotada", "value": "Curruca capirotada"},
            {"label":"Curruca carrasqueña", "value": "Curruca carrasqueña"},
            {"label":"Curruca mirlona occidenta", "value": "Curruca mirlona occidenta"},
            {"label":"Curruca mosquitera", "value": "Curruca mosquitera"},
            {"label":"Curruca rabilarga", "value": "Curruca rabilarga"},
            {"label":"Curruca tomillera", "value": "Curruca tomillera"},
            {"label":"Curruca zarcera", "value": "Curruca zarcera"},
            {"label":"Éider común", "value": "Éider común"},
            {"label":"Elanio común", "value": "Elanio común"},
            {"label":"Escribano cerillo", "value": "Escribano cerillo"},
            {"label":"Escribano hortelano", "value": "Escribano hortelano"},
            {"label":"Escribano montesino", "value": "Escribano montesino"},
            {"label":"Escribano nival", "value": "Escribano nival"},
            {"label":"Escribano soteño", "value": "Escribano soteño"},
            {"label":"Escribano triguero", "value": "Escribano triguero"},
            {"label":"Esmerejón", "value": "Esmerejón"},
            {"label":"Espátula común", "value": "Espátula común"},
            {"label":"Estornino negro", "value": "Estornino negro"},
            {"label":"Estornino pinto", "value": "Estornino pinto"},
            {"label":"Falaropo picofino", "value": "Falaropo picofino"},
            {"label":"Falaropo picogrueso", "value": "Falaropo picogrueso"},
            {"label":"Flamenco común", "value": "Flamenco común"},
            {"label":"Flamenco enano", "value": "Flamenco enano"},
            {"label":"Focha común", "value": "Focha común"},
            {"label":"Focha moruna", "value": "Focha moruna"},
            {"label":"Frailecillo atlántico", "value": "Frailecillo atlántico"},
            {"label":"Fulmar boreal", "value": "Fulmar boreal"},
            {"label":"Fumarel aliblanco", "value": "Fumarel aliblanco"},
            {"label":"Fumarel cariblanco", "value": "Fumarel cariblanco"},
            {"label":"Fumarel común", "value": "Fumarel común"},
            {"label":"Gallineta común", "value": "Gallineta común"},
            {"label":"Ganga ibérica", "value": "Ganga ibérica"},
            {"label":"Ganga ortega", "value": "Ganga ortega"},
            {"label":"Garceta común", "value": "Garceta común"},
            {"label":"Garceta grande", "value": "Garceta grande"},
            {"label":"Garcilla bueyera", "value": "Garcilla bueyera"},
            {"label":"Garcilla cangrejera", "value": "Garcilla cangrejera"},
            {"label":"Garza imperial", "value": "Garza imperial"},
            {"label":"Garza real", "value": "Garza real"},
            {"label":"Gavilán común", "value": "Gavilán común"},
            {"label":"Gavión atlántico", "value": "Gavión atlántico"},
            {"label":"Gavión hiperbóreo", "value": "Gavión hiperbóreo"},
            {"label":"Gaviota argéntea europea", "value": "Gaviota argéntea europea"},
            {"label":"Gaviota cabecinegra", "value": "Gaviota cabecinegra"},
            {"label":"Gaviota cana", "value": "Gaviota cana"},
            {"label":"Gaviota de Audouin", "value": "Gaviota de Audouin"},
            {"label":"Gaviota de Delaware", "value": "Gaviota de Delaware"},
            {"label":"Gaviota de Sabine", "value": "Gaviota de Sabine"},
            {"label":"Gaviota del Caspio", "value": "Gaviota del Caspio"},
            {"label":"Gaviota enana", "value": "Gaviota enana"},
            {"label":"Gaviota groenlandesa", "value": "Gaviota groenlandesa"},
            {"label":"Gaviota patiamarilla", "value": "Gaviota patiamarilla"},
            {"label":"Gaviota picofina", "value": "Gaviota picofina"},
            {"label":"Gaviota reidora", "value": "Gaviota reidora"},
            {"label":"Gaviota sombría", "value": "Gaviota sombría"},
            {"label":"Gaviota tridáctila", "value": "Gaviota tridáctila"},
            {"label":"Golondrina común", "value": "Golondrina común"},
            {"label":"Gorrión alpino", "value": "Gorrión alpino"},
            {"label":"Gorrión chillón", "value": "Gorrión chillón"},
            {"label":"Gorrión molinero", "value": "Gorrión molinero"},
            {"label":"Gorrión moruno", "value": "Gorrión moruno"},
            {"label":"Graja", "value": "Graja"},
            {"label":"Grajilla occidental", "value": "Grajilla occidental"},
            {"label":"Grulla común", "value": "Grulla común"},
            {"label":"Grulla damisela", "value": "Grulla damisela"},
            {"label":"Guión de codornices", "value": "Guión de codornices"},
            {"label":"Halcón borní", "value": "Halcón borní"},
            {"label":"Halcón de Eleonora", "value": "Halcón de Eleonora"},
            {"label":"Halcón peregrino", "value": "Halcón peregrino"},
            {"label":"Herrerillo capuchino", "value": "Herrerillo capuchino"},
            {"label":"Ibis eremita", "value": "Ibis eremita"},
            {"label":"Jilguero europeo", "value": "Jilguero europeo"},
            {"label":"Jilguero lúgano", "value": "Jilguero lúgano"},
            {"label":"Lagópodo alpino", "value": "Lagópodo alpino"},
            {"label":"Lavandera blanca", "value": "Lavandera blanca"},
            {"label":"Lavandera boyera", "value": "Lavandera boyera"},
            {"label":"Lavandera cascadeña", "value": "Lavandera cascadeña"},
            {"label":"Lavandera cetrina", "value": "Lavandera cetrina"},
            {"label":"Lechuza común", "value": "Lechuza común"},
            {"label":"Malvasía cabeciblanca", "value": "Malvasía cabeciblanca"},
            {"label":"Martín pescador común", "value": "Martín pescador común"},
            {"label":"Martinete común", "value": "Martinete común"},
            {"label":"Milano negro", "value": "Milano negro"},
            {"label":"Milano real", "value": "Milano real"},
            {"label":"Mirlo acuático europeo", "value": "Mirlo acuático europeo"},
            {"label":"Mirlo capiblanco", "value": "Mirlo capiblanco"},
            {"label":"Mirlo común", "value": "Mirlo común"},
            {"label":"Mito común", "value": "Mito común"},
            {"label":"Mochuelo boreal", "value": "Mochuelo boreal"},
            {"label":"Mochuelo europeo", "value": "Mochuelo europeo"},
            {"label":"Morito común", "value": "Morito común"},
            {"label":"Mosquitero canario", "value": "Mosquitero canario"},
            {"label":"Mosquitero común", "value": "Mosquitero común"},
            {"label":"Mosquitero ibérico", "value": "Mosquitero ibérico"},
            {"label":"Mosquitero musical", "value": "Mosquitero musical"},
            {"label":"Mosquitero papialbo", "value": "Mosquitero papialbo"},
            {"label":"Mosquitero silbador", "value": "Mosquitero silbador"},
            {"label":"Negrón común", "value": "Negrón común"},
            {"label":"Negrón especulado", "value": "Negrón especulado"},
            {"label":"Oropéndola europea", "value": "Oropéndola europea"},
            {"label":"Ostrero euroasiático", "value": "Ostrero euroasiático"},
            {"label":"Ostrero negro canario", "value": "Ostrero negro canario"},
            {"label":"Págalo grande", "value": "Págalo grande"},
            {"label":"Págalo parásito", "value": "Págalo parásito"},
            {"label":"Págalo pomarino", "value": "Págalo pomarino"},
            {"label":"Págalo rabero", "value": "Págalo rabero"},
            {"label":"Pagaza piconegra", "value": "Pagaza piconegra"},
            {"label":"Pagaza piquirroja", "value": "Pagaza piquirroja"},
            {"label":"Paíño boreal", "value": "Paíño boreal"},
            {"label":"Paíño de Madeira", "value": "Paíño de Madeira"},
            {"label":"Paíño de Wilson", "value": "Paíño de Wilson"},
            {"label":"Paíño europeo", "value": "Paíño europeo"},
            {"label":"Paíño pechialbo", "value": "Paíño pechialbo"},
            {"label":"Pájaro moscón europeo", "value": "Pájaro moscón europeo"},
            {"label":"Paloma bravía", "value": "Paloma bravía"},
            {"label":"Paloma rabiche", "value": "Paloma rabiche"},
            {"label":"Paloma torcaz", "value": "Paloma torcaz"},
            {"label":"Paloma turqué", "value": "Paloma turqué"},
            {"label":"Paloma zurita", "value": "Paloma zurita"},
            {"label":"Papamoscas cerrojillo", "value": "Papamoscas cerrojillo"},
            {"label":"Papamoscas gris", "value": "Papamoscas gris"},
            {"label":"Pardela balear", "value": "Pardela balear"},
            {"label":"Pardela capirotada", "value": "Pardela capirotada"},
            {"label":"Pardela cenicienta atlántica", "value": "Pardela cenicienta atlántica"},
            {"label":"Pardela cenicienta mediterránea", "value": "Pardela cenicienta mediterránea"},
            {"label":"Pardela chica", "value": "Pardela chica"},
            {"label":"Pardela mediterránea", "value": "Pardela mediterránea"},
            {"label":"Pardela pichoneta", "value": "Pardela pichoneta"},
            {"label":"Pardela sombría", "value": "Pardela sombría"},
            {"label":"Pardillo común", "value": "Pardillo común"},
            {"label":"Pato colorado", "value": "Pato colorado"},
            {"label":"Pato havelda", "value": "Pato havelda"},
            {"label":"Perdiz moruna", "value": "Perdiz moruna"},
            {"label":"Perdiz pardilla", "value": "Perdiz pardilla"},
            {"label":"Perdiz roja", "value": "Perdiz roja"},
            {"label":"Petirrojo europeo", "value": "Petirrojo europeo"},
            {"label":"Petrel de Bulwer", "value": "Petrel de Bulwer"},
            {"label":"Petrel de las Desertas", "value": "Petrel de las Desertas"},
            {"label":"Petrel freira", "value": "Petrel freira"},
            {"label":"Petrel gongón", "value": "Petrel gongón"},
            {"label":"Picamaderos negro", "value": "Picamaderos negro"},
            {"label":"Pico dorsiblanco", "value": "Pico dorsiblanco"},
            {"label":"Pico mediano", "value": "Pico mediano"},
            {"label":"Pico menor", "value": "Pico menor"},
            {"label":"Pico picapinos", "value": "Pico picapinos"},
            {"label":"Picogordo común", "value": "Picogordo común"},
            {"label":"Pinzón azul de Gran Canaria", "value": "Pinzón azul de Gran Canaria"},
            {"label":"Pinzón azul de Tenerife", "value": "Pinzón azul de Tenerife"},
            {"label":"Pinzón real", "value": "Pinzón real"},
            {"label":"Pinzón vulgar", "value": "Pinzón vulgar"},
            {"label":"Piquituerto común", "value": "Piquituerto común"},
            {"label":"Pito real ibérico", "value": "Pito real ibérico"},
            {"label":"Polluela bastarda", "value": "Polluela bastarda"},
            {"label":"Polluela chica", "value": "Polluela chica"},
            {"label":"Polluela pintoja", "value": "Polluela pintoja"},
            {"label":"Porrón bastardo", "value": "Porrón bastardo"},
            {"label":"Porrón moñudo", "value": "Porrón moñudo"},
            {"label":"Porrón pardo", "value": "Porrón pardo"},
            {"label":"Quebrantahuesos", "value": "Quebrantahuesos"},
            {"label":"Rabijunco etéreo", "value": "Rabijunco etéreo"},
            {"label":"Rascón europeo", "value": "Rascón europeo"},
            {"label":"Reyezuelo listado", "value": "Reyezuelo listado"},
            {"label":"Roquero rojo", "value": "ARoquero rojo"},
            {"label":"Roquero solitario", "value": "Roquero solitario"},
            {"label":"Ruiseñor pechiazul", "value": "Ruiseñor pechiazul"},
            {"label":"Serín canario", "value": "Serín canario"},
            {"label":"Serín verdecillo", "value": "Serín verdecillo"},
            {"label":"Silbón europeo", "value": "Silbón europeo"},
            {"label":"Sisón común", "value": "Sisón común"},
            {"label":"Somormujo lavanco", "value": "Somormujo lavanco"},
            {"label":"Tarabilla canaria", "value": "Tarabilla canaria"},
            {"label":"Tarabilla europea", "value": "Tarabilla europea"},
            {"label":"Tarabilla norteña", "value": "Tarabilla norteña"},
            {"label":"Tarro blanco", "value": "Tarro blanco"},
            {"label":"Tarro canelo", "value": "Tarro canelo"},
            {"label":"Terrera común", "value": "Terrera común"},
            {"label":"Terrera marismeña", "value": "Terrera marismeña"},
            {"label":"Torcecuello euroasiático", "value": "Torcecuello euroasiático"},
            {"label":"Torillo andaluz", "value": "Torillo andaluz"},
            {"label":"Tórtola europea", "value": "Tórtola europea"},
            {"label":"Tórtola turca", "value": "Tórtola turca"},
            {"label":"Trepador azul", "value": "Trepador azul"},
            {"label":"Treparriscos", "value": "Treparriscos"},
            {"label":"Urraca común", "value": "Urraca común"},
            {"label":"Vencejo cafre", "value": "Vencejo cafre"},
            {"label":"Vencejo común", "value": "Vencejo común"},
            {"label":"Vencejo moro", "value": "Vencejo moro"},
            {"label":"Vencejo pálido", "value": "Vencejo pálido"},
            {"label":"Vencejo real", "value": "Vencejo real"},
            {"label":"Vencejo unicolor", "value": "Vencejo unicolor"},
            {"label":"Verderón común", "value": "Verderón común"},
            {"label":"Verderón serrano", "value": "Verderón serrano"},
            {"label":"Vuelvepiedras común", "value": "Vuelvepiedras común"},
            {"label":"Zampullín común", "value": "Zampullín común"},
            {"label":"Zampullín cuellinegro", "value": "Zampullín cuellinegro"},
            {"label":"Zampullín cuellirrojo", "value": "Zampullín cuellirrojo"},
            {"label":"Zarapito trinador", "value": "Zarapito trinador"},
            {"label":"Zarcero bereber", "value": "Zarcero bereber"},
            {"label":"Zarcero icterino", "value": "Zarcero icterino"},
            {"label":"Zarcero pálido", "value": "Zarcero pálido"},
            {"label":"Zarcero políglota", "value": "Zarcero políglota"},
            {"label":"Zorzal alirrojo", "value": "Zorzal alirrojo"},
            {"label":"Zorzal charlo", "value": "Zorzal charlo"},
            {"label":"Zorzal común", "value": "Zorzal común"},
            {"label":"Zorzal real", "value": "Zorzal real"}],
        multi=False, # Multi: Deja el Usuario introducir multiples valores a la vez
        value='Chotacabras cuellirrojo', # Cambiamos Value a Chotacabras cuellirrojo como default, asi el usuario ya tiene un mapa al entrar a la pagina.
        clearable=False, # No aparece el boton de Borrar
        searchable=True, # Se puede buscar escribiendo
        style={"width": "60%"} # Style: Cambia el estilo en general del Desplegable (width: Ancho)
        ),
    html.Div(id="output_container", children= []), #Crea un bloque de texto debajo del Desplegable y crea una variable hija de t
    html. Br(), # Espacio en blanco Best InBI
    dcc.Graph(id='superstore_map', figure={}), # Crea el Mapa y crea una variable hija de tipo figura
    # aplicamos el componente Slider para CREAR el deslizante
    dcc.Slider(
    0,4,
    step=None,
    marks={
        0: 'SIN DATOS',
        1: 'LEVE',
        2: 'MEDIO',
        3: 'GRAVE',
        4: 'MUY GRAVE'},
    tooltip={"placement": "bottom", "always_visible": True}, # CREA los botones sombreados 
    id="slider",
    value=0
    ),
    dcc.Graph(id='superstore_map2', figure={})
    
])    
  
    
# Conecta Los Graficos de Plotly con Los Componentes Dash
@app.callback( # Define Los Inputs y Outputs de la funcion update_graph (Actualizar Grafico)
    [Output (component_id='output_container', component_property='children'), # Output 1: Texto debajo del desplegable
    Output (component_id='superstore_map', component_property='figure'), 
    Output (component_id='superstore_map2', component_property='figure')], #Output 2: Mapa2
    [Input (component_id='slct_nombre_comun', component_property='value'),
     Input (component_id='slider', component_property='value')] # Input: Ave seleccionada
)

def update_graph (option_slctd, value):
    print(option_slctd) # Imprimimos a consola La opcion del usuario,
    print(type (option_slctd)) # y el tipo de la opcion (best practices).
    
    container="El ave seleccionada es: {}".format(option_slctd) # Cambiamos el texto debajo del desplegable al Año introducido
    
    dff = df.copy() # Creamos una copia de nuestra DataFrame, asi no modificamos datos de la original.
    dff = dff[dff["NOMBRE COMÚN"] == option_slctd] # Filtramos La nueva DataFrame por ave seleccionada, asi tenemos solo el ave que buscamos.
    
    if value==0:
        df_puntos=total_aves_0
    else:
        pass
    if value==1:
        df_puntos=total_aves_1
    else:
        pass
    if value==2:
        df_puntos=total_aves_2
    else:
        pass
    if value==3:
        df_puntos=total_aves_3
    else:
        pass
    if value==4:
        df_puntos=total_aves_4
    else:
        pass
    
    
    #Plotly Express
    #Creamos el Mapa
    fig= px.choropleth_mapbox(
        geojson=shapes.geometry,
        data_frame=dff, # Definimos La DataFrame con nuestra copia
        locations=dff.index_ciudad, # Cambiamos Las Localizaciones para que  nuestra columna de 'index_ciudad' para que sepa qué comunidad es.
        # TIENEN QUE SER UN NÚMERO, NO PUEDEN SER LOS NOMBRES!!
        color='NIVEL AMENAZA', # Definimos esta variable para cambiar La Columna que usa como referencia para añadir colores.
        hover_name='Ubicacion', # El título en negrita de cada cuadro de información que se abre al pasar el ratón por encima.
        hover_data=['NOMBRE COMÚN', 'Amenaza', 'CEEA y LESRPE'], # Datos que se muestran en el cuadro informativo.
        labels={0 : 'Sin datos suficientes', 1: 'Amenaza Leve', 2 : 'Amenaza Media', 3 : 'Amenaza Grave', 4 :'Amenaza Muy Grave'} ,
        mapbox_style='stamen-watercolor', # Estilo del mapa, hemos puesto este que es un mapa de acuarela. Otras posibilidad más seria: 'carto-positron'
        title='Situación de las aves en peligro de España',  # Título de la figura
        zoom=4, 
        center = {"lat": 39.6, "lon": -4},
        opacity=0.5, # Definimos Los valores que aparezerán al pasar el ratón sobre un estado
    ),
        
    fig2 = go.Figure(
        go.Scattermapbox(
            lat=df_puntos["lat"],
            lon=df_puntos["lon"],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=df_puntos["TOTAL AVES"],
                color= '#ff8533'
            )
        )
    )


    return container, fig, fig2 # Retornar Los Objetos que hemos creado
# IMPORTANTE: Retornar Los valores en el mismo orden que pusiste en Los Outputs!

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False) # Corre el Servidor:
    
    
    
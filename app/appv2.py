import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import joblib

import folium
from folium.plugins import HeatMap

# 1. Procesos iniciales para la carga de la app
# Cargar el modelo desde el archivo .pkl
modelo = joblib.load('../models/modelo_random_forest.pkl')

# Carga de las variables del modelo y su peso
importance_variables = pd.read_csv('../data/importance_variables.csv')

# Inicialización de las variables
def initialize_inputs():
    return np.zeros(59)

X_names = [
    'bathrooms', 'bedrooms', 'num_amenities', 'square_feet', 'Patio/Deck',
    'Parking', 'Internet Access', 'Storage', 'pets', 'state_AL', 'state_AR',
    'state_AZ', 'state_CA', 'state_CO', 'state_CT', 'state_DC', 'state_DE',
    'state_FL', 'state_GA', 'state_HI', 'state_IA', 'state_ID', 'state_IL',
    'state_IN', 'state_KS', 'state_KY', 'state_LA', 'state_MA', 'state_MD',
    'state_ME', 'state_MI', 'state_MN', 'state_MO', 'state_MS', 'state_MT',
    'state_NC', 'state_ND', 'state_NE', 'state_NH', 'state_NJ', 'state_NM',
    'state_NV', 'state_NY', 'state_OH', 'state_OK', 'state_OR', 'state_PA',
    'state_RI', 'state_SC', 'state_SD', 'state_TN', 'state_TX', 'state_UT',
    'state_VA', 'state_VT', 'state_WA', 'state_WI', 'state_WV', 'state_WY'
]

X_values = initialize_inputs()

def new_request(request):
    
    X_values = initialize_inputs()

    for variable in request.keys():
        position = X_names.index(variable)
        X_values[position] = request[variable]

    X = pd.DataFrame([X_values], columns=X_names)

    y_pred = modelo.predict(X)

    return y_pred

def importance_variables(request):
    
    names = []
    values = []
    
    for variable in request.keys():
        
        position = X_names.index(variable)
        X_values[position] = request[variable]

    X = pd.DataFrame([X_values], columns=X_names)

    return 0

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Cargar los datos
file_path = '../data/datos_clean.csv'
df = pd.read_csv(file_path, encoding="utf-8",sep=',')


def get_locations(df):
    df['location'] = df['state'] + ' | ' + df['cityname']
    return df['location'].drop_duplicates().to_list()

def get_ammenities():
    return [
        'Internet Access', 'Alarm', 'Elevator', 'View', 'Refrigerator', 'Storage', 'Dishwasher', 'Playground', 'Clubhouse', 'Gated', 
        'Patio/Deck', 'Pool', 'Parking', 'Golf', 'AC', 'Doorman', 'Cable or Satellite', 'Tennis', 'Hot Tub', 'Garbage Disposal', 'Fireplace',
        'TV', 'Basketball', 'Washer Dryer', 'Luxury', 'Wood Floors', 'Gym'
        ]



def get_map(data, value):
    
    summary_data = data.groupby(['latitude','longitude'])[['latitude','longitude','price']].mean('price')
    summary_data['color'] = np.where(summary_data['price'] >= value, 'red', 'blue')
    
    map_center = [summary_data["latitude"].mean(), summary_data["longitude"].mean()]

    #Crear el mapa
    m = folium.Map(location=map_center, zoom_start=8)

    #Agregar cada punto al mapa
    for _, row in summary_data.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=3,
            color=row["color"],
            fill=True,
            fill_color="blue",
            fill_opacity=0.5
        ).add_to(m)

    return m
def get_map_init(data):
    
    map_center = [data["latitude"].mean(), data["longitude"].mean()]

    #Crear el mapa
    m = folium.Map(location=map_center, zoom_start=3)

    return m


# Inicia la arquitectura de la applicación
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    style={'display': 'flex'},
    children=[
        html.Div(
           style={
                'width': '25%',
                'backgroundColor': '#f0f0f0',  # optional styling
                'padding': '10px'
            },
            # Seccion de panel de control
            children=[
                 html.H1("Panel de control"),
                 html.Div(
                    style={
                        'padding': '10px'
                    },
                    children=[
                        "Pies cuadrados:",
                        dcc.Input(
                            id='input-sf',
                            type='number',
                            placeholder='Escribe un número',
                            value=''
                        )
                    ]
                 ),
                 html.Div(
                    style={
                        'padding': '10px'
                    },
                    children=[
                        "Habitaciones:",
                        dcc.Input(
                            id='input-rooms',
                            type='number',
                            placeholder='Escribe un número',
                            value=''
                        )
                    ]
                 ),
                html.Div(
                    style={
                        'padding': '10px'
                    },
                    children=[
                        "Baños:",
                        dcc.Input(
                            id='input-baths',
                            type='number',
                            placeholder='Escribe un número',
                            value=''
                        )
                    ]
                 ),
                 html.Div(
                    style={
                        'padding': '10px'
                    },
                    children=[
                        "Ciudad:",
                        dcc.Dropdown(
                            get_locations(df),
                            searchable=True,
                            id='input-city'
                        )
                    ]
                 ), 
                 html.Div(
                    style={
                        'padding': '10px',

                    },
                    children=[
                        "Servicios:",
                        dcc.Dropdown(
                            get_ammenities(),
                            searchable=True,
                            multi=True,
                            id='input-amenities'
                        )
                    ]
                 ),
                 html.Div(
                    style={
                        'padding': '10px',

                    },
                    children=[
                        "Permite mascotas:",
                        dcc.Checklist(
                            ['Perros', 'Gatos'],
                            inline=True,
                            id='input-pets'
                        )
                    ]
                 ),
                html.Button('Submit', id='my-button', n_clicks=0)
            ]
        ),
        # Seccion de salidas / resultado
        html.Div(
            style={
                'width': '75%',
                'backgroundColor': '#e0e0e0',  # optional styling
                'padding': '10px',
            },
            children=[
                html.Div(
                    style={
                        'padding': '10px',
                        # 'backgroundColor': '#000000',  # optional styling
                    },
                    children=html.H3("Mercado de venta de apartamentos")
                ),
                html.Div(
                    style={
                        'padding': '10px',
                        # 'backgroundColor': '#e0e0e0',  # optional styling
                        'display': 'flex'
                    },
                    children=[
                        html.Div(
                            style={
                                'width': '50%',
                                # 'backgroundColor': '#000000',  # optional styling
                                'padding': '10px'
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-weight": "bold"
                                    },
                                    children="Precio estimado: "
                                ),
                                html.Div(
                                    id='output-est'
                                ),
                                html.Div(
                                    id='output-diff'
                                ),
                            ]
                        ),
                        html.Div(
                            style={
                                'width': '50%',
                                'backgroundColor': '#e0e0e0',  # optional styling
                                'padding': '10px'
                            },
                            children=[
                                html.Div(
                                    style={
                                        "font-weight": "bold"
                                    },
                                    children="Precio del mercado"
                                ),
                                html.Div(
                                    id='output-mean-mkt'
                                ),
                                html.Div(
                                    id='output-min-mkt'
                                ),
                                html.Div(
                                    id='output-max-mkt'
                                ),
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={
                        'padding': '10px',
                        # 'backgroundColor': '#e0e0e0',  # optional styling
                        'display': 'flex'
                    },
                    children=[
                        html.Div(
                            style={
                                'width': '50%',
                                'backgroundColor': '#e0e0e0',  # optional styling
                                'padding': '10px'
                            },
                            children='Primera parte'
                        ),
                        html.Div(
                            style={
                                'width': '50%',
                                'backgroundColor': '#e0e0e0',  # optional styling
                                'padding': '10px'
                            },
                            children=[
                                html.Div("Diferencia de precios en otras ciudades del estado:"),
                                html.Iframe(
                                    id='map-iframe',  # This is the id you can reference in callbacks
                                    # srcDoc=get_map(df)._repr_html_(),
                                    width='100%',
                                    height='325',
                                    style={'border': 'none'}
                                ),
                                html.Div(
                                    style={
                                        'font-size': '10px',
                                    },
                                    children="Rojo: Precios por encima del valor estimado; Azul: Precios por debajo del valor estimado"
                                )
                            ]
                        ),
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('output-est', 'children'), Output('output-diff', 'children'),
        Output('output-mean-mkt', 'children'), Output('output-min-mkt', 'children'), Output('output-max-mkt', 'children'),
        Output('map-iframe', 'srcDoc')
    ],
    Input('my-button', 'n_clicks'),
    [
        State('input-sf', 'value'), State('input-rooms', 'value'),
        State('input-baths', 'value'), State('input-city', 'value'),
        State('input-amenities', 'value'), State('input-pets', 'value'),
    ]
)
def update_output(n_clicks, sf, rooms, baths, city, amenities, pets):
    
    #Valores iniciales
    estimate_value = 'Ingrese los valores en el panel izquierdo'
    mean_makt = 'Precio promedio: '
    min_makt = 'Precio mayor: '
    max_makt = 'Precio menor: '
    diff_est = '0 vs. el promedio del mercado'
    m = get_map_init(df)._repr_html_()
    
    # Cuando el usuario ya agregó valores
    if n_clicks > 0:
        
        # 1. Calculo de estimacion
        req = {
            'bathrooms':baths,
            'bedrooms':rooms,
            'num_amenities':len(amenities),
            'square_feet':sf,
            'Patio/Deck': 1 if 'Patio/Deck' in amenities else 0,
            'Parking':  1 if 'Parking' in amenities else 0,
            'Internet Access': 1 if 'Internet Access' in amenities else 0,
            'Storage': 1 if 'Storage' in amenities else 0,
            'pets': 1 if not pets else 0,
            'state_' + city[:2]:1
        }

        value = int(new_request(req)[0])

        estimate_value = f'{value} USD/Mes'

        # 2. Calculo de precios promedio
        subset = df[df['location'] == city]
        mean_makt = 'Precio promedio: {value}'.format(value=int(np.mean(subset['price'])))
        min_makt = 'Precio menor: {value}'.format(value=int(np.min(subset['price'])))
        max_makt = 'Precio mayor: {value}'.format(value=int(np.max(subset['price'])))

        diff = value - int(np.mean(subset['price']))

        diff_est = '{value} vs. el promedio del mercado'.format(value=diff)

        m = get_map(df[df['state'] == city[:2]], value)._repr_html_()

    # Recien iniciada la app
    return estimate_value, diff_est, mean_makt, min_makt, max_makt, m

if __name__ == '__main__':
    app.run_server(host = " 0.0.0.0 ", debug=True)
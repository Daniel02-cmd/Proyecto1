import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

import joblib

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


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Cargar los datos
file_path = '../data/datos_apartamentos_rent.csv'
df = pd.read_csv(file_path, encoding="utf-8",sep=';')

def get_locations(df):
    df['location'] = df['state'] + ' | ' + df['cityname']
    return df['location'].drop_duplicates().to_list()

def get_ammenities(a):
    return [
        'Internet Access', 'Alarm', 'Elevator', 'View', 'Refrigerator', 'Storage', 'Dishwasher', 'Playground', 'Clubhouse', 'Gated', 
        'Patio/Deck', 'Pool', 'Parking', 'Golf', 'AC', 'Doorman', 'Cable or Satellite', 'Tennis', 'Hot Tub', 'Garbage Disposal', 'Fireplace',
        'TV', 'Basketball', 'Washer Dryer', 'Luxury', 'Wood Floors', 'Gym'
        ]


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
                 "Panel de control",
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
                            get_ammenities(df),
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
                            ['dog', 'Cat'],
                            inline=True,
                            id='input-pets'
                        )
                    ]
                 ),
                html.Button('Submit', id='my-button', n_clicks=0)
            ]
        ),
        html.Div(
            style={
                'width': '75%',
                'backgroundColor': '#e0e0e0',  # optional styling
                'padding': '10px'
            },
            children=[
                "Estimación",
                html.Div(id='output-div')
            ]
        )
    ]
)

@app.callback(
    Output('output-div', 'children'),
    Input('my-button', 'n_clicks'),
    [
        State('input-sf', 'value'), State('input-rooms', 'value'),
        State('input-baths', 'value'), State('input-city', 'value'),
        State('input-amenities', 'value'), State('input-pets', 'value'),
    ]
)
def update_output(n_clicks, sf, rooms, baths, city, amenities, pets):
    # Cuando el usuario ya agregó valores
    if n_clicks > 0:
        
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

        estimate_value = int(new_request(req)[0])

        return f'You request: {estimate_value} USD'
    
    # Recien iniciada la app
    return 'Please enter a value and click submit.'

if __name__ == '__main__':
    app.run_server(debug=True)
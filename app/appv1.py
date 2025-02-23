import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Cargar los datos
file_path = '../data/datos_apartamentos_rent.csv'
df = pd.read_csv(file_path, encoding="utf-8",sep=';')

def get_locations(df):
    df['location'] = df['state'] + ' | ' + df['cityname']
    return df['location'].drop_duplicates().to_list()

def get_ammenities(a):
    return ['Internet Access', 'Alarm', 'Elevator', 'View', 'Refrigerator', 'Storage', 'Dishwasher', 'Playground', 'Clubhouse', 'Gated', 'Patio/Deck', 'Pool', 'Parking', 'Golf', 'AC', 'Doorman', 'Cable or Satellite', 'Tennis', 'Hot Tub', 'Garbage Disposal', 'Fireplace', 'TV', 'Basketball', 'Washer Dryer', 'Luxury', 'Wood Floors', 'Gym']


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
                        'font-size': '15px'

                    },
                    children=[
                        "Servicios:",
                        dcc.Checklist(
                            get_ammenities(df),
                            id='input-amenities'
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
                "Right Frame",
                html.Div(id='output-div')
            ]
        )
    ]
)

@app.callback(
    Output('output-div', 'children'),
    Input('my-button', 'n_clicks'),
    State('input-sf', 'value')
)
def update_output(n_clicks, input_value):
    if n_clicks > 0:
        return f'You entered: {input_value}'
    return 'Please enter a value and click submit.'

if __name__ == '__main__':
    app.run_server(debug=True)
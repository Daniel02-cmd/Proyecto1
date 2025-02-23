import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Leer el archivo CSV
df = pd.read_csv("/Users/Usuario/Downloads/datos1.csv")

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
app.title = "Apartamentos en Estados Unidos"

# Rango de precios
min_price = df["price"].min()
max_price = df["price"].max()

# Rango de habitaciones
min_bedrooms = df["bedrooms"].min()
max_bedrooms = df["bedrooms"].max()

# Rango de baños
min_bano = df["bathrooms"].min()
max_bano = df["bathrooms"].max()

app.layout = html.Div([
    html.Div([
        html.Label("Selecciona un rango de precios:"),
        dcc.RangeSlider(
            id='range-slider-price',
            min=min_price, max=max_price, step=100,
            marks={min_price: f"{min_price:,}", max_price: f"{max_price:,}"},
            value=[min_price, max_price]
        ),
        html.Div(id='selected-range-price', style={'marginTop': '10px', 'fontSize': '18px', 'color': 'lightgray'}),

        html.Label("Selecciona un rango de habitaciones:", style={'marginTop': '20px'}),
        dcc.RangeSlider(
            id='range-slider-bedrooms',
            min=min_bedrooms, max=max_bedrooms, step=1,
            marks={min_bedrooms: f"{min_bedrooms:,}", max_bedrooms: f"{max_bedrooms:,}"},
            value=[min_bedrooms, max_bedrooms]
        ),
        html.Div(id='selected-range-bedrooms', style={'marginTop': '10px', 'fontSize': '18px', 'color': 'lightgray'}),

        html.Label("Selecciona un rango de baños:", style={'marginTop': '20px'}),
        dcc.RangeSlider(
            id='range-slider-bano',
            min=min_bano, max=max_bano, step=0.5,
            marks={min_bano: f"{min_bano:,}", max_bano: f"{max_bano:,}"},
            value=[min_bano, max_bano]
        ),
        html.Div(id='selected-range-bano', style={'marginTop': '10px', 'fontSize': '18px', 'color': 'lightgray'}),

        html.Button("Filtrar", id='filter-button', n_clicks=0),

 ], style={'width': '30%', 'padding': '20px', 'backgroundColor': '#f8f9fa'}),

    html.Div([
        html.H1("Caracterizacion de Apartamentos",  style={'textAlign': 'center'}),
        html.Div(id="output-container", style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'width': '60%', 'padding': '20px'})
])

@app.callback(
    Output('selected-range-price', 'children'),
    Input('range-slider-price', 'value')
)
def update_selected_range_price(selected_range):
    return f"Rango de precios seleccionado: {selected_range[0]:,} - {selected_range[1]:,}"

@app.callback(
    Output('selected-range-bedrooms', 'children'),
    Input('range-slider-bedrooms', 'value')
)
def update_selected_range_bedrooms(selected_range):
    return f"Rango de habitaciones seleccionado: {selected_range[0]:,} - {selected_range[1]:,}"

@app.callback(
    Output('selected-range-bano', 'children'),
    Input('range-slider-bano', 'value')
)
def update_selected_range_bano(selected_range):
    return f"Rango de baños seleccionado: {selected_range[0]:,} - {selected_range[1]:,}"

@app.callback(
    Output('output-container', 'children'),
    Input('filter-button', 'n_clicks'),
    Input('range-slider-price', 'value'),
    Input('range-slider-bedrooms', 'value'),
    Input('range-slider-bano', 'value'),
    Input('range-slider-sf', 'value')
)
def update_output(n_clicks, selected_range_price, selected_range_bedrooms, selected_range_bano):
    if n_clicks > 0:

        pmin = selected_range_price[0]
        pmax = selected_range_price[1]
        bemin = selected_range_bedrooms[0]
        bemax = selected_range_bedrooms[1]
        bamin = selected_range_bano[0]
        bamax = selected_range_bano[1]

            
        filtro = df[(df["price"] >= pmin) & (df["price"] <= pmax) 
                & (df['bedrooms'] >= bemin) & (df['bedrooms'] <= bemax)
                & (df['bathrooms'] >= bamin) & (df['bathrooms'] <= bamax)]

        promedio_precio_filtrado = round(filtro["price"].mean(),2)
        promedio_habitaciones_filtrado = round(filtro["bedrooms"].mean())
        promedio_bano_filtrado = round(filtro["bathrooms"].mean())

        return html.Div([
            html.P(f"El precio promedio por apartamento es: {promedio_precio_filtrado:,}"),
            html.P(f"El número promedio de habitaciones por apartamento es: {promedio_habitaciones_filtrado:,}"),
            html.P(f"El número promedio de baños por apartamento es: {promedio_bano_filtrado:,}")
        ])
    return "Presiona 'Filtrar' para calcular."

if __name__ == '__main__':
    app.run_server(debug=True)
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

# Rango de square_feet
min_sf = df["square_feet"].min()
max_sf = df["square_feet"].max()

# Estados
estados = df["state"].unique()

# Ciudades
ciudades = df["cityname"].unique()

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

        html.Label("Selecciona un rango de square feet:"),
        dcc.RangeSlider(
            id='range-slider-sf',
            min=min_sf, max=max_sf, step=10,
            marks={min_sf: f"{min_sf:,}", max_sf: f"{max_sf:,}"},
            value=[min_sf, max_sf]
        ),
        html.Div(id='selected-range-sf', style={'marginTop': '10px', 'fontSize': '18px', 'color': 'lightgray'}),

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

        html.Label("Filtrar por estados"),
        dcc.Checklist(
            id="switch-1",
            options=[{"label": "Activar", "value": "on"}],
            value=[],
            inline=True
        ),

        dcc.Dropdown(
            id="dropdown-1",
            options=estados,
            placeholder="Selecciona una opción",
            clearable=False,
            disabled=True
        ),

        html.Label("Filtrar por ciudades"),
        dcc.Checklist(
            id="switch-2",
            options=[{"label": "Activar", "value": "on"}],
            value=[],
            inline=True
        ),

        dcc.Dropdown(
            id="dropdown-2",
            options=ciudades,
            placeholder="Selecciona una opción",
            clearable=False,
            disabled=True
        ),

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
    Output('selected-range-sf', 'children'),
    Input('range-slider-sf', 'value')
)
def update_selected_range_sf(selected_range):
    return f"Rango de square feet seleccionado: {selected_range[0]:,} - {selected_range[1]:,}"

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

# Callback para manejar la lógica de exclusividad entre los interruptores
@app.callback(
    [Output("dropdown-1", "disabled"),
     Output("dropdown-2", "disabled"),
     Output("switch-2", "value"),
     Output("switch-1", "value")],
    [Input("switch-1", "value"),
     Input("switch-2", "value")]
)
def toggle_dropdowns(switch_1, switch_2):
    if "on" in switch_1:
        return False, True, [], switch_1  # Habilita lista 1, deshabilita lista 2
    elif "on" in switch_2:
        return True, False, switch_2, []  # Habilita lista 2, deshabilita lista 1
    return True, True, [], []  # Ambas listas deshabilitadas si no hay selección

@app.callback(
    Output('output-container', 'children'),[
    Input("switch-1", "value"),
    Input("switch-2", "value"),
    Input("dropdown-1", "value"),
    Input("dropdown-2", "value")],
    Input('filter-button', 'n_clicks'),
    Input('range-slider-price', 'value'),
    Input('range-slider-bedrooms', 'value'),
    Input('range-slider-bano', 'value'),
    Input('range-slider-sf', 'value')
)
def update_output(n_clicks, selected_range_price, selected_range_bedrooms, selected_range_bano, selected_range_sf, switch_1, switch_2, dropdown_1, dropdown_2):
    if n_clicks > 0:

        pmin = selected_range_price[0]
        pmax = selected_range_price[1]
        bemin = selected_range_bedrooms[0]
        bemax = selected_range_bedrooms[1]
        bamin = selected_range_bano[0]
        bamax = selected_range_bano[1]
        sfmin = selected_range_sf[0]
        sfmax = selected_range_sf[1]

        if "on" in switch_1:
            if dropdown_1:

                filtro = df[(df["price"] >= pmin) & (df["price"] <= pmax) 
                    & (df['bedrooms'] >= bemin) & (df['bedrooms'] <= bemax)
                    & (df['bathrooms'] >= bamin) & (df['bathrooms'] <= bamax)
                    & (df['square_feet'] >= sfmin) & (df['square_feet'] <= sfmax)
                    & (df['state'] == dropdown_1)]
                
                promedio_precio_filtrado = round(filtro["price"].mean(),2)
                promedio_habitaciones_filtrado = round(filtro["bedrooms"].mean())
                promedio_bano_filtrado = round(filtro["bathrooms"].mean())
                promedio_sf_filtrado = round(filtro["square_feet"].mean())

                return html.P(f"Seleccionaste: {dropdown_1}")
            return "Debes seleccionar un Estado."

        if "on" in switch_2:
            if dropdown_2:

                filtro = df[(df["price"] >= pmin) & (df["price"] <= pmax) 
                    & (df['bedrooms'] >= bemin) & (df['bedrooms'] <= bemax)
                    & (df['bathrooms'] >= bamin) & (df['bathrooms'] <= bamax)
                    & (df['square_feet'] >= sfmin) & (df['square_feet'] <= sfmax)
                    & (df['cityname'] == dropdown_2)]
                
                promedio_precio_filtrado = round(filtro["price"].mean(),2)
                promedio_habitaciones_filtrado = round(filtro["bedrooms"].mean())
                promedio_bano_filtrado = round(filtro["bathrooms"].mean())
                promedio_sf_filtrado = round(filtro["square_feet"].mean())

                return html.P(f"Seleccionaste: {dropdown_2}")
            return "Debes seleccionar una Ciudad."
        
        else:
            
            filtro = df[(df["price"] >= pmin) & (df["price"] <= pmax) 
                & (df['bedrooms'] >= bemin) & (df['bedrooms'] <= bemax)
                & (df['bathrooms'] >= bamin) & (df['bathrooms'] <= bamax)
                & (df['square_feet'] >= sfmin) & (df['square_feet'] <= sfmax)]

            promedio_precio_filtrado = round(filtro["price"].mean(),2)
            promedio_habitaciones_filtrado = round(filtro["bedrooms"].mean())
            promedio_bano_filtrado = round(filtro["bathrooms"].mean())
            promedio_sf_filtrado = round(filtro["square_feet"].mean())   

        return html.Div([
            html.P(f"El precio promedio por apartamento es: {promedio_precio_filtrado:,}"),
            html.P(f"El número promedio de habitaciones por apartamento es: {promedio_habitaciones_filtrado:,}"),
            html.P(f"El número promedio de baños por apartamento es: {promedio_bano_filtrado:,}"),
            html.P(f"El número promedio de square feet por apartamento es: {promedio_sf_filtrado:,}")
        ])
    return "Presiona 'Filtrar' para calcular."

if __name__ == '__main__':
    app.run_server(debug=True)

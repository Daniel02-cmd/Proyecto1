import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("/Users/Usuario/Downloads/datos1.csv")

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
app.title = "Ciudades y Estados"

# Estados
estados = df["state"].unique()

# Ciudades
ciudades = df["cityname"].unique()

app.layout = html.Div([
    html.Div([
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
    ], style={'width': '30%', 'padding': '20px', 'backgroundColor': '#f8f9fa'}),

    html.Div([
        html.H1("Resultado", style={'textAlign': 'center'}),
        html.Div(id="output-container", style={'textAlign': 'center', 'marginTop': '20px'})
    ], style={'width': '60%', 'padding': '20px'})
])

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

# Callback para mostrar el resultado en la parte principal
@app.callback(
    Output("output-container", "children"),
    [Input("switch-1", "value"),
     Input("switch-2", "value"),
     Input("dropdown-1", "value"),
     Input("dropdown-2", "value")]
)
def update_output(switch_1, switch_2, dropdown_1, dropdown_2):
    if "on" in switch_1:
        if dropdown_1:
            return html.P(f"Seleccionaste: {dropdown_1}")
        return "Debes seleccionar una opción de la Lista 1."

    if "on" in switch_2:
        if dropdown_2:
            return html.P(f"Seleccionaste: {dropdown_2}")
        return "Debes seleccionar una opción de la Lista 2."

    return "Sin listas activas."

if __name__ == "__main__":
    app.run_server(debug=True)

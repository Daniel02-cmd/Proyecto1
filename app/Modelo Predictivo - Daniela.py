import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Función para cargar y preprocesar datos
def cargar_datos():
    # Cargar datos desde Excel
    datos = pd.read_excel("datos_clean.xlsx", sheet_name="Hoja4")
    
    # Convertir variables categóricas en tipo categoría
    for col in datos.select_dtypes(include=['object']).columns:
        datos[col] = datos[col].astype('category')
    
    # Tratar valores faltantes en numéricos con la mediana
    for col in datos.select_dtypes(include=['number']).columns:
        datos[col].fillna(datos[col].median(), inplace=True)
    
    # Tratar valores faltantes en categóricos con "Desconocido"
    for col in datos.select_dtypes(include=['category']).columns:
        datos[col] = datos[col].cat.add_categories(["Desconocido"]).fillna("Desconocido")
    
    # Convertir variables categóricas en dummies (One-Hot Encoding)
    datos = pd.get_dummies(datos, columns=datos.select_dtypes(include=['category']).columns, drop_first=False)
    
    return datos

# Cargar y dividir los datos
datos = cargar_datos()
print(f"Tamaño del conjunto de datos original: {datos.shape}")
print("Primeras filas del dataset original:")
print(datos.head())

# Separar en datos de entrenamiento y prueba
X = datos.drop(columns=["price"])
y = datos["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

# Optimización de hiperparámetros en Random Forest
rf = RandomForestRegressor(n_estimators=3000, max_features='sqrt', min_samples_leaf=2, max_leaf_nodes=500, random_state=123)
rf.fit(X_train, y_train)

# Hacer predicciones
y_pred = rf.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# Mostrar métricas optimizadas
print(f"\nRMSE Optimizado (Random Forest): {rmse}")
print(f"R² Optimizado (Random Forest): {r2}")

# Función para predecir precio basado en input del usuario
def predecir_precio(modelo, trainData):
    print("\nIngrese los datos para la predicción:")
    
    # Solicitar entrada del usuario
    bedrooms = float(input("Número de habitaciones: "))
    bathrooms = float(input("Número de baños: "))
    square_feet = float(input("Tamaño en pies cuadrados: "))
    
    # Obtener nombres de las variables dummy del estado
    columnas_estado = [col for col in trainData.columns if col.startswith("state_")]
    
    # Extraer nombres reales de estados, excluyendo "Desconocido"
    estados_disponibles = [col.replace("state_", "") for col in columnas_estado if col != "state_Desconocido"]
    
    if not estados_disponibles:
        print("⚠️ No se encontraron estados disponibles en los datos. Verifique el preprocesamiento.")
        return
    
    # Mostrar opciones de estado al usuario
    print("\nEstados disponibles:")
    for i, estado in enumerate(estados_disponibles, 1):
        print(f"{i}: {estado}")
    
    # Pedir al usuario que elija un estado
    seleccion = int(input("\nSeleccione el número del estado: "))
    
    # Validar la selección
    if seleccion < 1 or seleccion > len(estados_disponibles):
        print("⚠️ Error: Selección inválida. Intente de nuevo ingresando un número de la lista.")
        return
    
    # Obtener el estado seleccionado
    estado_seleccionado = estados_disponibles[seleccion - 1]
    
    # Crear un DataFrame con los datos ingresados por el usuario
    datos_usuario = pd.DataFrame({
        "bedrooms": [bedrooms],
        "bathrooms": [bathrooms],
        "square_feet": [square_feet]
    })
    
    # Agregar todas las variables dummy del estado con valor 0
    for col in columnas_estado:
        datos_usuario[col] = 0
    
    # Activar la variable correspondiente al estado elegido (poner 1)
    estado_dummy = f"state_{estado_seleccionado}"
    if estado_dummy in datos_usuario.columns:
        datos_usuario[estado_dummy] = 1
    
    # Asegurar que las columnas coincidan con las del modelo
    datos_usuario = datos_usuario.reindex(columns=X_train.columns, fill_value=0)
    
    # Hacer la predicción
    precio_predicho = modelo.predict(datos_usuario)
    
    # Mostrar resultado
    print(f"\n📢 Precio estimado: {round(precio_predicho[0], 2)}")

    predecir_precio(rf, X_train)
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

file_path = '../data/datos_clean.csv'  # Ajusta la ruta correcta


#Cargar los datos
file_path = '../data/datos_clean.csv'
df_clean=pd.read_csv(file_path,encoding="utf-8",sep=',')
print(df_clean.head())

#Modelo 1 y=log_price

#Definir las variables predictoras (X) y la variable objetivo (y)
X = df_clean[['state', 'bathrooms', 'bedrooms', 'square_feet', 'num_amenities', 'Patio/Deck', 'Parking', 'Internet Access', 'Storage', 'pets']]  # Variables seleccionadas
y = df_clean['log_price']  # Variable objetivo

#Convertir las variables categóricas en variables dummy
X = pd.get_dummies(X, columns=['state'], drop_first=True)

#Dividir en conjunto de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Verificar tamaños de los conjuntos
print(f"Datos de entrenamiento: {X_train.shape}, Datos de prueba: {X_test.shape}")

#Inicializar el modelo Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

#Entrenar el modelo
rf_model.fit(X_train, y_train)

#Realizar predicciones
y_pred = rf_model.predict(X_test)

#Calcular métricas
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Primer modelo: Mean Squared Error (MSE): {mse:.4f}")
print(f"Primer Modelo: R cuadrado Score: {r2:.4f}")


#Modelo 2 y=price

#Definir las variables predictoras (X) y la variable objetivo (y)
X2 = df_clean[['state', 'bathrooms', 'bedrooms', 'num_amenities', 'square_feet', 'Patio/Deck', 'Parking', 'Internet Access', 'Storage', 'pets']]  # Variables seleccionadas
y2 = df_clean['price']  # Variable objetivo

#Convertir las variables categóricas en variables dummy
X2 = pd.get_dummies(X2, columns=['state'], drop_first=True)

#Convertir las variables categóricas en variables dummy

#Dividir en conjunto de entrenamiento (80%) y prueba (20%)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, test_size=0.2, random_state=42)

#Verificar tamaños de los conjuntos
print(f"Datos de entrenamiento: {X_train2.shape}, Datos de prueba: {X_test2.shape}")

#Inicializar el modelo Random Forest
rf_model2 = RandomForestRegressor(n_estimators=100, random_state=42)

#Entrenar el modelo
rf_model2.fit(X_train2, y_train2)

#Realizar predicciones
y_pred2 = rf_model2.predict(X_test2)

#Calcular métricasx
mse2 = mean_squared_error(y_test2, y_pred2)
r2_2 = r2_score(y_test2, y_pred2)

print(f"Segundo modelo: Mean Squared Error (MSE): {mse2:.4f}")
print(f"Segundo modelo: R cuadrado Score: {r2_2:.4f}")

joblib.dump(rf_model2, "../models/modelo_random_forest.pkl")


## Extracción de la importancia de las variables ---------------------------------------------------------
# Extraer la importancia de las variables
importances = rf_model2.feature_importances_

# Si 'X_train' es un DataFrame, se pueden obtener los nombres de las variables
feature_names = X_train2.columns

# Crear una Serie de pandas para visualizar mejor la importancia
feat_importances = pd.Series(importances, index=feature_names)

# Ordenar las importancias de mayor a menor
feat_importances = feat_importances.sort_values(ascending=False).reset_index()

feat_importances.columns = ['variable', 'importance']

feat_importances.to_csv('../data/importance_variables.csv', index=False)

print(X_train2.columns)

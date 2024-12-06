# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:49:52 2024

@author: pablo
"""

# Importar librerías necesarias
import pandas as pd

# Rutas de los archivos
ruta_cores2024 = r"C:\Users\pablo\OneDrive\Escritorio\Proyeccion electoral congreso\cores_servel_comunas_nacional.xlsx"

# Cargar los datos
cores2024 = pd.read_excel(ruta_cores2024)

# Filtrar los datos según condiciones específicas
condicion = (
    cores2024["candidato"].str.match(r"^[a-zA-Z]", na=False) & 
    ~cores2024["candidato"].isin(["Votos nulos", "Votos blancos"])
)

cores2024_filtrado = cores2024.copy()  # Crear una copia para manipulación

# Actualizar columna 'partido' con valores de la siguiente fila si cumplen la condición
for index in cores2024_filtrado[condicion].index:
    if index + 1 < len(cores2024_filtrado):  # Validar existencia de fila posterior
        cores2024_filtrado.loc[index, "partido"] = cores2024_filtrado.loc[index + 1, "partido"]

# Convertir y limpiar datos de la columna 'votos'
#cores2024_filtrado['votos'] = cores2024_filtrado['votos'].astype(str)
#cores2024_filtrado['votos'] = cores2024_filtrado['votos'].str.replace('.', '', regex=False).astype(int)

# Rellenar la columna 'partido' con valores específicos
cores2024_filtrado.loc[cores2024_filtrado['candidato'] == 'Votos Nulos', 'partido'] = 'Votos Nulos'
cores2024_filtrado.loc[cores2024_filtrado['candidato'] == 'Votos Blancos', 'partido'] = 'Votos blancos'

#Borrar elementos que tengan partido nan
cores2024_filtrado = cores2024_filtrado.dropna(subset=['partido'])
#Borrar candidatos y dejar solo totales de subpactos
cores2024_filtrado = cores2024_filtrado[~cores2024_filtrado['candidato'].str.match(r'^\d', na=False)]


#Se asumen que todos los votos del partido POPULAR son de PH

#['partido'] = cores2024_filtrado['partido'].replace("POPULAR", "PH")
#cores2024_filtrado.loc[cores2024_filtrado['candidato'] == "B - IZQUIERDA ECOLOGISTA POPULAR", 'partido'] = "PH"

# Reemplazar "IND" en 'partido' por "IND" concatenado con el valor de 'candidato'
cores2024_filtrado['partido'] = cores2024_filtrado.apply(
    lambda row: f"IND - {row['candidato']}" if row['partido'] == "IND" else row['partido'],
    axis=1
)

ruta_salida = r"C:\Users\pablo\OneDrive\Escritorio\Proyeccion electoral congreso\cores2024_f_preeliminar.xlsx"
cores2024_filtrado.to_excel(ruta_salida, index=True)



#Hasta acá voy bien


#Repite la operación para concejales
import pandas as pd
#cargar los datos
ruta_concejales2024 = r"C:\Users\pablo\OneDrive\Escritorio\Proyeccion electoral congreso\concejales_servel_comunas_nacional.xlsx"
# Cargar los datos
concejales2024 = pd.read_excel(ruta_concejales2024)

# Filtrar los datos según condiciones específicas
condicion = (
    concejales2024["candidato"].str.match(r"^[a-zA-Z]", na=False) & 
    ~concejales2024["candidato"].isin(["Votos nulos", "Votos blancos"])
)

concejales2024_filtrado = concejales2024.copy()  # Crear una copia para manipulación

# Actualizar columna 'partido' con valores de la siguiente fila si cumplen la condición
for index in concejales2024_filtrado[condicion].index:
    if index + 1 < len(concejales2024_filtrado):  # Validar existencia de fila posterior
        concejales2024_filtrado.loc[index, "partido"] = concejales2024_filtrado.loc[index + 1, "partido"]

# Rellenar la columna 'partido' con valores específicos
concejales2024_filtrado.loc[concejales2024_filtrado['candidato'] == 'Votos Nulos', 'partido'] = 'Votos Nulos'
concejales2024_filtrado.loc[concejales2024_filtrado['candidato'] == 'Votos Blancos', 'partido'] = 'Votos blancos'

#Borrar elementos que tengan partido nan
concejales2024_filtrado = concejales2024_filtrado.dropna(subset=['partido'])
#Borrar candidatos y dejar solo totales de subpactos
concejales2024_filtrado = concejales2024_filtrado[~concejales2024_filtrado['candidato'].str.match(r'^\d', na=False)]


#Se asumen que todos los votos del partido POPULAR son de PH

#['partido'] = cores2024_filtrado['partido'].replace("POPULAR", "PH")
#cores2024_filtrado.loc[cores2024_filtrado['candidato'] == "B - IZQUIERDA ECOLOGISTA POPULAR", 'partido'] = "PH"

# Reemplazar "IND" en 'partido' por "IND" concatenado con el valor de 'candidato'
concejales2024_filtrado['partido'] = concejales2024_filtrado.apply(
    lambda row: f"IND - {row['candidato']}" if row['partido'] == "IND" else row['partido'],
    axis=1
)

ruta_salida = r"C:\Users\pablo\OneDrive\Escritorio\Proyeccion electoral congreso\concejales2024_f_preeliminar.xlsx"
concejales2024_filtrado.to_excel(ruta_salida, index=True)



#DESDE AQUI COMIENZA OTRO CÓDIGO, DESCOMENTAR PARA USAR








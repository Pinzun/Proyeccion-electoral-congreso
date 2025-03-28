#importa pandas para el manejo de df
import pandas as pd
import numpy as np

#import plotly.express as px
import gdown
import os

#Define funciones para leer archivos de GDrive
def descargar_archivo_drive(url, nombre_salida):
    """Descarga un archivo de Google Drive usando gdown."""
    gdown.download(url, nombre_salida, quiet=False)

def leer_excel_desde_drive(url):
    """
    Descarga y lee un archivo Excel compartido desde Google Drive.
    Elimina el archivo temporal después de leerlo.
    Retorna un DataFrame.
    """
    archivo_temporal = 'archivo_temporal.xlsx'
    descargar_archivo_drive(url, archivo_temporal)

    try:
        # Leer el archivo descargado en un DataFrame
        df = pd.read_excel(archivo_temporal)
    finally:
        # Asegurarse de que el archivo temporal sea eliminado
        if os.path.exists(archivo_temporal):
            os.remove(archivo_temporal)

    return df

def leer_csv_desde_drive(url):
    """
    Descarga y lee un archivo Excel compartido desde Google Drive.
    Elimina el archivo temporal después de leerlo.
    Retorna un DataFrame.
    """
    archivo_temporal = 'archivo_temporal.csv'
    descargar_archivo_drive(url, archivo_temporal)

    try:
        # Leer el archivo descargado en un DataFrame
        df = pd.read_csv(archivo_temporal)
    finally:
        # Asegurarse de que el archivo temporal sea eliminado
        if os.path.exists(archivo_temporal):
            os.remove(archivo_temporal)

    return df

#url para eleccion de diputados
#url_comunas=r"https://drive.google.com/uc?id=1SGJXB8iu7384-3a94mV2QFjTMfjbeVpL"
#url para eleccion de senadores
url_comunas=r"https://drive.google.com/uc?id=1lhFt_SBBUDEPn-eJ84xkaLGBxAl7P8J3"
territorios=leer_excel_desde_drive(url_comunas)
resultados_proyectados=pd.read_csv("panel/data/resultados_proyectados_senadores.csv", encoding= 'utf-8',sep=';')
# Eliminar todas las columnas cuyo nombre contenga "Unnamed"
resultados_proyectados = resultados_proyectados.loc[:, ~resultados_proyectados.columns.str.contains('^Unnamed')]
territorios = territorios.set_index('comuna')
resultados_proyectados = resultados_proyectados.set_index('Comuna')

# Paso 2: Ahora unimos 'resultados_proyectados_transpuesto' con la columna 'Distrito' o 'Circunscripcion' de 'territorios' según la eleccion
#resultados_proyectados['Distrito'] = resultados_proyectados.index.map(territorios['Distrito'])
resultados_proyectados['Circunscripcion'] = resultados_proyectados.index.map(territorios['Circunscripcion'])


# Paso 3: Agrupar por 'Distrito' o 'Circunscripcion' y sumar los votos de cada partido
#resultados_proyectados_territorio = resultados_proyectados.groupby('Distrito').sum()
resultados_proyectados_territorio = resultados_proyectados.groupby('Circunscripcion').sum()

resultados_proyectados_territorio.index = resultados_proyectados_territorio.index.astype(int)
# Eliminar las columnas "Votos Blancos" y "Votos Nulos" del DataFrame
#resultados_proyectados_territorio = resultados_proyectados_territorio.drop(columns=['Votos Blancos', 'Votos Nulos'])
# Paso 1: Calcular la suma de votos por fila y almacenarlo en una nueva columna
resultados_proyectados_territorio['total_votos'] = resultados_proyectados_territorio.sum(axis=1)

# Paso 2: Dividir cada valor de la fila por el total de votos de la misma fila
resultados_proyectados_territorio_normalizado = resultados_proyectados_territorio.div(resultados_proyectados_territorio['total_votos'], axis=0)

# Paso 3: Eliminar la columna 'total_votos' del DataFrame normalizado (si no la necesitas)
resultados_proyectados_territorio_normalizado = resultados_proyectados_territorio_normalizado.drop(columns=['total_votos'])
resultados_proyectados_territorio_normalizado = resultados_proyectados_territorio_normalizado.rename(columns={'IND - CANDIDATURAS INDEPENDIENTES': 'IND'})
resultados_proyectados_territorio_normalizado.to_csv("resultados_proyectados_proporciones_senadores.csv", encoding= 'utf-8',sep=';')

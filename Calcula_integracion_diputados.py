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

def calcula_dhont(numero_concejales, numero_pactos, votos_por_pacto):
    # Crear una lista para almacenar los resultados de la distribución de escaños por pacto
    escaños_por_pacto = []
    
    # Inicializar una lista con el número de escaños ganados por cada pacto a cero
    for _ in range(numero_pactos):
        escaños_por_pacto.append(0)
    
    # Iterar para asignar los escaños a cada pacto
    for i in range(numero_concejales):
        # Crear una lista para almacenar los cocientes electorales
        cocientes_electorales = []
        
        # Calcular el cociente electoral para cada pacto
        for j in range(numero_pactos):
            cociente = votos_por_pacto[j] / (escaños_por_pacto[j] + 1)
            cocientes_electorales.append((cociente, j))
        
        # Encontrar el pacto con el mayor cociente electoral
        max_cociente, index_pacto_ganador = max(cocientes_electorales)
        
        # Incrementar el número de escaños del pacto ganador
        escaños_por_pacto[index_pacto_ganador] += 1
    
    return escaños_por_pacto

url_escaños=r"https://drive.google.com/uc?id=1yZsg51IdmOwt7JWQbZ5p7eBLR2n944hN"
url_comunas_distro=r"https://drive.google.com/uc?id=1SGJXB8iu7384-3a94mV2QFjTMfjbeVpL"
'''
#pacto partidos
#url_pactos=r"https://drive.google.com/uc?id=1pDYs6g-DBMOECk74rGwWZS_uf2rdlDE6"
#pacto convencion
#url_pactos=r"https://drive.google.com/uc?id=1Dh2pLORNFTH5u1ni2smJIl044eS0mESn"
#pacto consejo
#url_pactos=r"https://drive.google.com/uc?id=1RXvbEtWK5bz7bdfigfr01Jr8XAW74hmV"
#pacto municipal
#url_pactos=r"https://drive.google.com/uc?id=1J1utmL2bLOWL_E9Cnsrirf27Rk3psb9L"
#pacto personalizado 1 CHV+
#url_pactos=r"https://drive.google.com/uc?id=1-dDlut6F32orBTJxVr_o3i2zD892Zdet"
#pacto personalizado 1 CHV
#url_pactos=r"https://drive.google.com/uc?id=1HT2mVFBB2_mHAWUqbI7lvlzycQd4MJsX"
#pacto personalizado 2 CHV+
#url_pactos=r"https://drive.google.com/uc?id=1SMo8FuDZsCurOOnqLsWdX1jKoVCYYwip"
#pacto personalizado 2 CHV
#url_pactos=r"https://drive.google.com/uc?id=1PxqtwIJHOH3ZT1II5eX8Eq-5m1B6zhpY"
#pacto personalizado 3 CHV+
#url_pactos=r"https://drive.google.com/uc?id=1plEm7CG3slcySyjZXybAPpApfcWwx85t"
#pacto personalizado 3 CHV
url_pactos=r"https://drive.google.com/uc?id=1imzAeLaauPK63-WSnCDCW8fHpbBcFJ6d"
'''

pactos_url = {
    "EscPart": "https://drive.google.com/uc?id=1pDYs6g-DBMOECk74rGwWZS_uf2rdlDE6",
    "EscConv": "https://drive.google.com/uc?id=1Dh2pLORNFTH5u1ni2smJIl044eS0mESn",
    "EscCons": "https://drive.google.com/uc?id=1RXvbEtWK5bz7bdfigfr01Jr8XAW74hmV",
    "EscMun": "https://drive.google.com/uc?id=1J1utmL2bLOWL_E9Cnsrirf27Rk3psb9L",
    "EscPers1_CHV1": "https://drive.google.com/uc?id=1-dDlut6F32orBTJxVr_o3i2zD892Zdet",
    "EscPers1_CHV": "https://drive.google.com/uc?id=1HT2mVFBB2_mHAWUqbI7lvlzycQd4MJsX",
    "EscPers2_CHV1": "https://drive.google.com/uc?id=1SMo8FuDZsCurOOnqLsWdX1jKoVCYYwip",
    "EscPers2_CHV": "https://drive.google.com/uc?id=1PxqtwIJHOH3ZT1II5eX8Eq-5m1B6zhpY",
    "EscPers3_CHV1": "https://drive.google.com/uc?id=1plEm7CG3slcySyjZXybAPpApfcWwx85t",
    "EscPers3_CHV": "https://drive.google.com/uc?id=1imzAeLaauPK63-WSnCDCW8fHpbBcFJ6d",
}

for nombre_pacto, url in pactos_url.items():

    escaños=leer_excel_desde_drive(url_escaños)
    comunas_distrito=leer_excel_desde_drive(url_comunas_distro)
    pactos=leer_excel_desde_drive(url)
    resultados_proyectados=pd.read_csv("resultados_proyectados.csv", encoding= 'utf-8',sep=';')
    resultados_proyectados = resultados_proyectados.loc[:, ~resultados_proyectados.columns.str.contains('^Unnamed')]
    #Se calculan los votos de cada partido por distriro
    # Asegurarnos de que 'comunas_distrito' tiene 'comuna' como índice
    comunas_distrito = comunas_distrito.set_index('comuna')
    resultados_proyectados = resultados_proyectados.set_index('Comuna')

    # Paso 2: Ahora unimos 'resultados_proyectados_transpuesto' con la columna 'Distrito' de 'comunas_distrito'
    resultados_proyectados['Distrito'] = resultados_proyectados.index.map(comunas_distrito['Distrito'])

    # Paso 3: Agrupar por 'Distrito' y sumar los votos de cada partido
    resultados_proyectados_distrito = resultados_proyectados.groupby('Distrito').sum()
    resultados_proyectados_distrito.index = resultados_proyectados_distrito.index.astype(int)


    #se procede a calcular el dhont para diputados

    
    #Se agrupan los votos por pacto
    # Paso 1: Transponer el DataFrame 'resultados_proyectados_distrito' para que los partidos sean las filas
    resultados_proyectados_transpuesto = resultados_proyectados_distrito.T
    # Paso 2: Unir el DataFrame 'resultados_proyectados_transpuesto' con el DataFrame 'pactos' para agregar la columna 'pacto'
    resultados_proyectados_transpuesto = resultados_proyectados_transpuesto.merge(pactos, how='left', left_index=True, right_on='partido')
    # Paso 3: Agrupar por 'pacto' y sumar los votos de los partidos dentro de cada pacto
    resultados_proyectados_por_pacto = resultados_proyectados_transpuesto.groupby('pacto').sum()
    resultados_proyectados_por_partido = resultados_proyectados_transpuesto.groupby(['pacto','partido']).sum()
    # Paso 4: Volver a transponer para tener las comunas como índice y los pactos como columnas
    resultados_proyectados_por_pacto = resultados_proyectados_por_pacto.T
    resultados_proyectados_por_pacto = resultados_proyectados_por_pacto.drop("partido", axis=0)


    # Crear DataFrame para guardar los resultados, usando pactos como columnas
    pactos_unicos = resultados_proyectados_por_pacto.columns  # Extraer los pactos únicos
    partidos_unicos = resultados_proyectados_distrito.columns
    integracion_pacto = pd.DataFrame(index=resultados_proyectados_distrito.index, columns=pactos_unicos)
    integracion_pacto=integracion_pacto.fillna(0)
    integracion_partido = pd.DataFrame(index=resultados_proyectados_distrito.index, columns=partidos_unicos)
    integracion_partido=integracion_partido.fillna(0)
    # Asegurarse de que la columna 'Distrito' sea el índice de 'escaños'
    escaños = escaños.set_index('Distrito')

    # Aplica D'Hondt en cada distrito
    for d in resultados_proyectados_distrito.index:    
        # Obtener el número de escaños asignados para este distrito
        n_escaños = escaños.loc[d, 'Diputados']    
        # Seleccionar la fila correspondiente al distrito en 'resultados_proyectados_por_pacto'
        fila = resultados_proyectados_por_pacto.loc[d]    
        # Crear la lista omitiendo los valores iguales a 0
        votos_por_pacto = fila[fila != 0].tolist()      
        # Calcular la distribución de escaños con D'Hondt
        numero_pactos = len(votos_por_pacto)
        integracion = calcula_dhont(n_escaños, numero_pactos, votos_por_pacto)    
        # Asignar los resultados al DataFrame
        # Mapear los resultados de integración al índice de pactos con votos
        pactos_no_cero = fila[fila != 0].index  # Índices (pactos) con votos
        for pacto, escaños_asignados in zip(pactos_no_cero, integracion):
            integracion_pacto.loc[d, pacto] = escaños_asignados
    for indice, row in integracion_pacto.iterrows():
        for pacto in pactos_unicos:
            n_electos=row[pacto]
            partidos=pactos.loc[pactos['pacto']==pacto,'partido'].tolist()
            n_partidos=len(partidos)
            votos_partido=resultados_proyectados_distrito.loc[indice,partidos].tolist()
            integracion_partidos=calcula_dhont(n_electos, n_partidos, votos_partido)
            for partido, escaños_partido in zip(partidos,integracion_partidos):
                integracion_partido.loc[indice,partido] = escaños_partido
                                

    integracion_partido = integracion_partido.rename(columns={
        'IND - CANDIDATURAS INDEPENDIENTES': 'IND',
        'AMARILLOS': 'AMA',
        'EVOPOLI': 'EVO',
        'IGUALDAD': 'IGU',
        'POPULAR': 'POP',
        'DEMOCRATAS': 'DEM',
        'REPUBLICANO': 'REP'})
   
    # Guardar los archivos con el nombre del pacto
    resultados_proyectados_por_pacto.to_csv(f"resultados_proyectados_{nombre_pacto}.csv", encoding='utf-8', sep=';')
    integracion_pacto.to_csv(f"resultados_integracion_pacto_{nombre_pacto}.csv", encoding='utf-8-sig', sep=';')
    integracion_partido.to_csv(f"resultados_integracion_partido_{nombre_pacto}.csv", encoding='utf-8-sig', sep=';')

    #resultados_proyectados_por_pacto.to_csv("resultados_proyectados_por_pacto.csv", encoding= 'utf-8',sep=';')
    #integracion_pacto.to_csv("resultados_integracion_pacto.csv", encoding= 'utf-8-sig',sep=';')
    #integracion_partido.to_csv("resultados_integracion_partido.csv", encoding= 'utf-8-sig',sep=';')
    #integracion_partido.csv("resultados_url_integracion_partido.csv", encoding= 'utf-8',sep=';')

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:12:11 2024

@author: pablo
"""
""" este script aplica la siguiente metodología:
1.Utilizaremos los resultados de las elecciones de concejales y consejeros regionales 2024 de manera combinada (a nivel comunal, para cada partido) para construir
 una variable ficticia base de resultados electorales para 2025, entregando el mismo peso a ambas elecciones. 
El motivo de usar ambas elecciones de manera combinada y con la misma ponderación a nivel comunal para proyectar resultados posibles para 2025,
 es porque la primera logra captar el efecto de caudillos locales, mientras que la segunda evalúa principalmente las marcas de los partidos. De tal modo,
 la base de proyección combina dos factores que son relevantes para el rendimiento electoral, y permite no sobre estimar o sub representar su importancia 
 para los futuros comicios parlamentarios.
Asimismo, se trata de un proceso electoral con mayores niveles de similitud con lo que será la elección parlamentaria de 2025. Esto por dos razones: por 
una parte, se trata de resultados obtenidos en un escenario de voto obligatorio; por otro, se trata de procesos electorales donde se medirá el peso relativo 
de las fuerzas políticas de manera más directa y a escala subnacional. Ello a diferencia del segundo ciclo electoral constituyente 
(consejeros y plebiscito de salida 2023), que estuvo cruzado por un clivaje político nacional de rasgos muy distintos.
2. Mediante una combinación de parámetros definidos a continuación, simularemos 100 escenarios aleatorios de resultados a nivel comunal para la variable ficticia
 base construida en el punto 1. Esto con el objetivo de integrar variaciones posibles sobre el resultado histórico considerado (resultados electorales de 2024). 
 Los parámetros para modelar la variación aleatoria de los resultados 2024 serán:
     -Porcentaje de variación aleatoria.
     -Porcentaje de retención de votos por incumbencia.
3. Una vez construidas las 100 simulaciones, las integraremos en una variable ficticia nueva promediando todos los resultados simulados (variable modelo).
 Con tal variable modelo construida, simularemos los resultados de la elección parlamentaria de 2025: para ello distribuiremos la proporción de votos en 
 distintos pactos utilizando el algoritmo del método D’Hondt establecido por el SERVEL, considerando distintos escenarios de alianza entre los partidos políticos 
 en competencia (tanto del oficialismo como de la oposición).
"""
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

#Define función que crea las matrices de variación para cada partido

def matriz_votos(partidos, comunas, incumbencia, incumbencia_cruzada, variacion, iteracion, eleccion, part):
    """Genera una matriz de votos por partido y comuna basada en una combinación
    lineal de un factor constante y una variación pseudoaleatoria.

    Args:
    - partidos (df): Lista de nombres de partidos (columnas).
    - comunas (list): Lista de nombres de comunas (filas).
    - incumbencia (df): matriz de dimensiones comunas x partidos que indica la cantidad de incumbencias de un partido.
    - incumbencia_cruzada (df): matriz de dimensiones comunas x que indica la cantidad de incumbencias cruzadas de un partido.
    - variacion (float): Valor máximo de la variación aleatoria permitida (entre -variacion y +variacion).
    - part (df): matriz con la participacion de cada comuna 
    Returns:
    - pd.DataFrame: Matriz de votos con índices como comunas y columnas como partidos.
    """
    # Límites para la variación aleatoria
    variacion_max = variacion
    variacion_min = -variacion
    print(f"Límites de variación: {variacion_min} a {variacion_max}")

    # Definir un factor constante
    incumb = 1.078  
    print(f"Factor constante (incumbencia): {incumb}")
    # Definir un factor constante
    incumb_cruz = 1.094  
    print(f"Factor constante (incumbencia_cruzada): {incumb_cruz}")

    # Crear la matriz de votos
    m_variacion = pd.DataFrame(index=comunas, columns=partidos)
    m_variacion = m_variacion.fillna(0)
    print(f"Matriz inicial (vacía):\n{m_variacion}")
    # Rellenar la matriz con los valores calculados
    for i, comuna in enumerate(comunas):
        print(f"\nProcesando comuna {i + 1}/{len(comunas)}: {comuna}")
        for j, partido in enumerate(partidos):
            print(f"  Procesando partido {j + 1}/{len(partidos)}: {partido}, para la iteración {iteracion} de {eleccion}")
            # Generar un valor pseudoaleatorio dentro del rango especificado
            x = np.random.uniform(variacion_min, variacion_max)
            print(f"    Variación aleatoria generada: {x}")
            # Calcular el voto como combinación lineal: constante + variación
            m_variacion.loc[comuna, partido] = max(1,incumbencia.loc[comuna,partido]*incumb,incumbencia_cruzada.loc[comuna,partido]*incumb_cruz) + x
            print(f"    Valor calculado: {m_variacion.loc[comuna, partido]}")
        sum_com=m_variacion.loc[comuna].sum()-len(partidos)
        if sum_com>1/part.loc[comuna,'Participacion']:
            ajus=(sum_com-1/part.loc[comuna, 'Participacion'])/len(partidos)
            for j, partido in enumerate(partidos):
                m_variacion.loc[comuna, partido]-=ajus
    print("\nMatriz final generada:")
    print(m_variacion)

    return m_variacion

"""Luego de definidas las funciones, se deben simular los escenarios
se simularán 100 escenarios para cada caso, luego se gráficaran para visualizar
la distribución de los datos y se calcularán estadísticos representativos.
El proceso se repetira para concejales y cores"""
#Asigna las rutas de los archivos a ser leídos

url_concejales= "https://drive.google.com/uc?id=1IjIMMccD2PBs45YrS4XGQxF-IJrQziIV"
url_cores = r"https://drive.google.com/uc?id=1U2KgH6EFu-Jbcm3c6t27x7UXvl7Lovzc"
#Activa incumbencias
#url_incumbencia=r"https://drive.google.com/uc?id=1YvIryAKIsw53R4D3ty21Bvywq5lmRsPB"
#url_incumbencia_cruzada=r"https://drive.google.com/uc?id=1yzLzPUnnKRuJw4Si0vO-y8FR_c4iKGkb"
#Desactiva incumbencias
url_incumbencia=r"https://drive.google.com/uc?id=1M_d6Kvpj3bUvv8SST-JGamprjT2FyFYA"
url_incumbencia_cruzada=r"https://drive.google.com/uc?id=1mLarX73K5oMovM8i5Ix4VmUVDd-_qPeh"
url_participacion=r"https://drive.google.com/uc?id=1nbtmcbExTNszNUT4uI3_SH1Y-CPtvK8q"


concejales=pd.read_csv("concejales2024_definitivo.csv",delimiter=",", encoding="utf-8")
cores=pd.read_csv("cores2024_definitivo.csv",delimiter=",", encoding="utf-8")
incumbencia=leer_excel_desde_drive(url_incumbencia)
# Configurar la columna 'Comuna' como índice
incumbencia.set_index('Comuna', inplace=True)
incumbencia_cruzada=leer_excel_desde_drive(url_incumbencia_cruzada)
# Configurar la columna 'Comuna' como índice
incumbencia_cruzada.set_index('Comuna', inplace=True)
participacion=leer_excel_desde_drive(url_participacion)
# Configurar la columna 'Comuna' como índice
participacion.set_index('Comuna', inplace=True)




#CORES
# Convertir la columna "partido" en una lista
partidos_cores = list(set(cores['partido'].tolist()))
# Convertir la columna "comunas" en una lista
comunas_cores = list(set(cores['comuna'].tolist()))

cores=cores.drop(columns=["region"])
cores["votos"]=cores["votos"].astype("int")
cores_pivot = cores.pivot(index='comuna', columns='partido', values='votos')


#CONCEJALES
# Convertir la columna "partido" en una lista
partidos_concejales = list(set(concejales['partido'].tolist()))
# Convertir la columna "comunas" en una lista
comunas_concejales = list(set(concejales['comuna'].tolist()))

concejales=concejales.drop(columns=["region"])
concejales["votos"]=concejales["votos"].astype("int")
concejales_pivot = concejales.pivot(index='comuna', columns='partido', values='votos')


print("Concluyó el pre procesamiento de datos")

#Simula concejales
resultados_concejales = {} # El resultado de concejales es un diccionario que almaneca multiples df
# cada df está definido como columns=partidos, index=comunas
variacion=0.15
contador=0
eleccion="concejales"
while contador <10: 
#while contador <100:    
    m_variacion=matriz_votos(partidos_concejales, comunas_concejales, incumbencia, incumbencia_cruzada, variacion, contador, eleccion, participacion)    
    resultados_concejales[contador] = concejales_pivot.multiply(m_variacion) 
    resultados_concejales[contador] = resultados_concejales[contador].fillna(0)
    print(f"iteración {contador} de concejales")
    contador+=1 


#Simula CORES
resultados_cores= {} # El resultado de cores es un diccionario que almaneca multiples df
# cada df está definido como columns=partidos, index=comunas
variacion=0.15
contador=0
eleccion="cores"
while contador <10:
    m_variacion=matriz_votos(partidos_cores, comunas_cores, incumbencia, incumbencia_cruzada, variacion, contador, eleccion, participacion)
    resultados_cores[contador] = cores_pivot.multiply(m_variacion)
    resultados_cores[contador] = resultados_cores[contador].fillna(0)

    print(f"iteración {contador} de cores")
    contador+=1
    
#Se calculan los promedios, medias y mediana a partir de las 100 simulaciones anteriores (resultados_cores y resultados_concejales)



#Luego de determinada la proyección se cálculan los dhont para cada distrito y circunscripción 

# Calcula los promedios, medias y medianas para los resultados de concejales para cada comuna y partido
promedio_concejales = pd.DataFrame()
media_concejales = pd.DataFrame()
mediana_concejales = pd.DataFrame()

for comuna in comunas_concejales:    
    promedio_concejales[comuna] = pd.concat([resultados_concejales[i].loc[comuna] for i in range(10)], axis=1).mean(axis=1)
    mediana_concejales[comuna] = pd.concat([resultados_concejales[i].loc[comuna] for i in range(10)], axis=1).median(axis=1)


# Calcular los promedios, medias y medianas para los resultados de cores para cada comuna y partido
promedio_cores = pd.DataFrame()
mediana_cores = pd.DataFrame()

for comuna in comunas_cores:    
    promedio_cores[comuna] = pd.concat([resultados_cores[i].loc[comuna] for i in range(10)], axis=1).mean(axis=1)
    mediana_cores[comuna] = pd.concat([resultados_cores[i].loc[comuna] for i in range(10)], axis=1).median(axis=1)
# Truncar los valores en los DataFrames de promedios y medianas
promedio_concejales = promedio_concejales.applymap(lambda x: np.trunc(x))
mediana_concejales = mediana_concejales.applymap(lambda x: np.trunc(x))
promedio_cores = promedio_cores.applymap(lambda x: np.trunc(x))
mediana_cores = mediana_cores.applymap(lambda x: np.trunc(x))

# Agregar la fila 'IND - CANDIDATURAS INDEPENDIENTES' con ceros a promedio_cores si no existe
if 'IND - CANDIDATURAS INDEPENDIENTES' not in promedio_cores.index:
    promedio_cores.loc['IND - CANDIDATURAS INDEPENDIENTES'] = 0

# Ajustar los valores con la función where
adjusted_cores = promedio_cores.where(promedio_cores != 0, promedio_concejales)
adjusted_concejales = promedio_concejales.where(promedio_concejales != 0, promedio_cores)

# Truncar los resultados proyectados después de la división
# Calcular el promedio con los valores ajustados
resultados_proyectados = (adjusted_cores + adjusted_concejales) / 2
resultados_proyectados = resultados_proyectados.applymap(lambda x: np.trunc(x))

#A partir del promedio de cores y concejales se calcular un valor único de votos para cada comuna y partido


#Luego de obtenidos los resultados se deben obtener los votos por distrito y circunscripcion para cada partido
# Calculamos el promedio de ambos DataFrames para cada celda
resultados_proyectados=(promedio_cores + promedio_concejales) / 2
resultados_proyectados=resultados_proyectados.fillna(0)
resultados_proyectados = np.trunc(resultados_proyectados).astype(int)
# Paso 1: Transponer el DataFrame 'resultados_proyectados' para que las comunas sean el índice
resultados_proyectados = resultados_proyectados.T
# Combinar las columnas de cada partido con su independiente asociado
# Aplica un castigo del 20% a los independientes antes de sumarlos al partido principal

# Filtrar las columnas de independientes asociados (que contienen "IND -") pero excluir "IND - CANDIDATURAS INDEPENDIENTES"
independientes_asociados = [
    col for col in resultados_proyectados.columns
    if col.startswith("IND -") and col != "IND - CANDIDATURAS INDEPENDIENTES"
]

# Manejo de casos especiales donde los votos deben distribuirse en partes iguales
casos_especiales = {
    "IND - FREVS/PL": ["FREVS", "PL"],
    "IND - POPULAR/PH/IGUALDAD": ["POPULAR", "PH", "IGUALDAD"]
}

# Iterar sobre las columnas de independientes
for col_ind in independientes_asociados:
    if col_ind in casos_especiales:
        # Si es un caso especial, distribuir los votos en partes iguales con castigo del 20%
        partidos = casos_especiales[col_ind]
        n_partidos = len(partidos)
        for partido in partidos:
            if partido in resultados_proyectados.columns:
                resultados_proyectados[partido] += (
                    resultados_proyectados[col_ind]*0.8 / n_partidos
                )
    else:
        # Caso general: sumar al partido principal con un castigo del 20%
        partido_asociado = col_ind.split("IND - ")[1]
        if partido_asociado in resultados_proyectados.columns:
            resultados_proyectados[partido_asociado] += (
                resultados_proyectados[col_ind] * 0.8
            )
    
    # Eliminar la columna del independiente asociado
    resultados_proyectados.drop(columns=[col_ind], inplace=True)
# Asegurarse de que 'comuna' sea una columna explícita
resultados_proyectados.reset_index(inplace=True)
resultados_proyectados.rename(columns={'index': 'Comuna'}, inplace=True)
resultados_proyectados.to_csv("resultados_proyectados.csv", encoding= 'utf-8',sep=';')

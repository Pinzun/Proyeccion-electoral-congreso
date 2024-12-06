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


#Define función que crea las matrices de variación para cada partido

def matriz_votos(partidos, comunas, incumbencia, incumbencia_cruzada, variacion, iteracion, eleccion, part):
    """Genera una matriz de votos por partido y comuna basada en una combinación
    lineal de un factor constante y una variación pseudoaleatoria.

    Args:
    - partidos (df): Lista de nombres de partidos (columnas).
    - comunas (list): Lista de nombres de comunas (filas).
    - incumbencia (df): matriz de dimensiones comunas x partidos con 0 y 1 que indica si un partido tiene incumbencia o no.
    - incumbencia_cruzada (df): matriz de dimensiones comunas x partidos con 0 y 1 que indica si un partido tiene incumbencia cruzada o no.
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



#Luego de definida la función se define la función d'hont para calcular los escaños obtenidos por 
#cada partido
#Define funcion d'hont
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


"""Luego de definidas las funciones, se deben simular los escenarios
se simularán 100 escenarios para cada caso, luego se gráficaran para visualizar
la distribución de los datos y se calcularán estadísticos representativos.
El proceso se repetira para concejales y cores"""
#Asigna las rutas de los archivos a ser leídos

url_concejales= "https://drive.google.com/uc?id=1IjIMMccD2PBs45YrS4XGQxF-IJrQziIV"
url_cores = r"https://drive.google.com/uc?id=1U2KgH6EFu-Jbcm3c6t27x7UXvl7Lovzc"
url_escaños=r"https://drive.google.com/uc?id=1yZsg51IdmOwt7JWQbZ5p7eBLR2n944hN"
url_comunas_distro=r"https://drive.google.com/uc?id=1SGJXB8iu7384-3a94mV2QFjTMfjbeVpL"
url_pactos=r"https://drive.google.com/uc?id=1Dh2pLORNFTH5u1ni2smJIl044eS0mESn"
url_incumbencia=r"https://drive.google.com/uc?id=1YvIryAKIsw53R4D3ty21Bvywq5lmRsPB"
url_incumbencia_cruzada=r"https://drive.google.com/uc?id=1yzLzPUnnKRuJw4Si0vO-y8FR_c4iKGkb"
url_participacion=r"https://drive.google.com/uc?id=1nbtmcbExTNszNUT4uI3_SH1Y-CPtvK8q"




concejales=leer_excel_desde_drive(url_concejales)
cores= leer_excel_desde_drive(url_cores)
escaños=leer_excel_desde_drive(url_escaños)
comunas_distrito=leer_excel_desde_drive(url_comunas_distro)
pactos=leer_excel_desde_drive(url_pactos)
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
while contador <100:    
    m_variacion=matriz_votos(partidos_concejales, comunas_concejales, incumbencia, incumbencia_cruzada, variacion, contador, eleccion, participacion)    
    resultados_concejales[contador] = concejales_pivot.multiply(m_variacion) 
    resultados_concejales[contador] = resultados_concejales[contador].fillna(0)
    print(f"iteración {contador} de concejales")
    contador+=1 


#Simula CORES
resultados_cores= {} # El resultado de concejales es un diccionario que almaneca multiples df
# cada df está definido como columns=partidos, index=comunas
variacion=0.15
contador=0
eleccion="cores"
while contador <100:
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
    promedio_concejales[comuna] = pd.concat([resultados_concejales[i].loc[comuna] for i in range(100)], axis=1).mean(axis=1)
    mediana_concejales[comuna] = pd.concat([resultados_concejales[i].loc[comuna] for i in range(100)], axis=1).median(axis=1)

# Calcular los promedios, medias y medianas para los resultados de cores para cada comuna y partido
promedio_cores = pd.DataFrame()
mediana_cores = pd.DataFrame()

for comuna in comunas_cores:
    promedio_cores[comuna] = pd.concat([resultados_cores[i].loc[comuna] for i in range(100)], axis=1).mean(axis=1)
    mediana_cores[comuna] = pd.concat([resultados_cores[i].loc[comuna] for i in range(100)], axis=1).median(axis=1)

# Truncar los valores en los DataFrames de promedios y medianas
promedio_concejales = promedio_concejales.applymap(lambda x: np.trunc(x))
mediana_concejales = mediana_concejales.applymap(lambda x: np.trunc(x))
promedio_cores = promedio_cores.applymap(lambda x: np.trunc(x))
mediana_cores = mediana_cores.applymap(lambda x: np.trunc(x))

# Truncar los resultados proyectados después de la división
resultados_proyectados = (promedio_cores + promedio_concejales) / 2
resultados_proyectados = resultados_proyectados.applymap(lambda x: np.trunc(x))

#A partir del promedio de cores y concejales se calcular un valor único de votos para cada comuna y partido


#Luego de obtenidos los resultados se deben obtener los votos por distrito y circunscripcion para cada partido
# Calculamos el promedio de ambos DataFrames para cada celda
resultados_proyectados = (promedio_cores + promedio_concejales) / 2

#Se calculan los votos de cada partido por distriro
# Asegurarnos de que 'comunas_distrito' tiene 'comuna' como índice
comunas_distrito = comunas_distrito.set_index('comuna')

# Paso 1: Transponer el DataFrame 'resultados_proyectados' para que las comunas sean el índice
resultados_proyectados_transpuesto = resultados_proyectados.T

# Paso 2: Ahora unimos 'resultados_proyectados_transpuesto' con la columna 'Distrito' de 'comunas_distrito'
resultados_proyectados_transpuesto['Distrito'] = resultados_proyectados_transpuesto.index.map(comunas_distrito['Distrito'])

# Paso 3: Agrupar por 'Distrito' y sumar los votos de cada partido
resultados_proyectados_distrito = resultados_proyectados_transpuesto.groupby('Distrito').sum()
resultados_proyectados_distrito.index = resultados_proyectados_distrito.index.astype(int)


#se procede a calcular el dhont para diputados

 
#Se agrupan los votos por pacto
# Paso 1: Transponer el DataFrame 'resultados_proyectados_distrito' para que los partidos sean las filas
resultados_proyectados_transpuesto = resultados_proyectados_distrito.T
# Paso 2: Unir el DataFrame 'resultados_proyectados_transpuesto' con el DataFrame 'pactos' para agregar la columna 'pacto'
resultados_proyectados_transpuesto = resultados_proyectados_transpuesto.merge(pactos, how='left', left_index=True, right_on='partido')
# Paso 3: Agrupar por 'pacto' y sumar los votos de los partidos dentro de cada pacto
resultados_proyectados_por_pacto = resultados_proyectados_transpuesto.groupby('pacto').sum()
# Paso 4: Volver a transponer para tener las comunas como índice y los pactos como columnas
resultados_proyectados_por_pacto = resultados_proyectados_por_pacto.T
resultados_proyectados_por_pacto = resultados_proyectados_por_pacto.drop("partido", axis=0)


# Crear DataFrame para guardar los resultados, usando pactos como columnas
pactos_unicos = resultados_proyectados_por_pacto.columns  # Extraer los pactos únicos
integracion_pacto = pd.DataFrame(index=resultados_proyectados_distrito.index, columns=pactos_unicos)

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





resultados_proyectados_distrito.to_csv("resultados_proyectados_distrito.csv",index=False, encoding= 'utf-8',sep=';')
resultados_proyectados_por_pacto.to_csv("resultados_proyectados_por_pacto.csv",index=False, encoding= 'utf-8',sep=';')
integracion_pacto.to_csv("resultados_url_integracion_pacto.csv",index=False, encoding= 'utf-8',sep=';')
#integracion_partido.csv("resultados_url_integracion_partido.csv",index=False, encoding= 'utf-8',sep=';')

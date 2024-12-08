# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:49:52 2024

@author: pablo
"""

# Importar librerías necesarias
import pandas as pd

# Rutas de los archivos
ruta_cores2024 = r"C:\Users\Ivan\OneDrive\Asesorias varias-PCIvan\Datos electorales\EstrategiaSur\Scrapeos\cores_servel_comunas_nacional.xlsx"

# Cargar los datos
df = pd.read_excel(ruta_cores2024)

# Filtrar los datos según condiciones específicas
#condicion = (
#    cores2024["candidato"].str.match(r"^[a-zA-Z]", na=False) & 
#    ~cores2024["candidato"].isin(["Votos nulos", "Votos blancos"])
#)

# Crear una copia del DataFrame para trabajar
df_filtrado = df.copy()
# Variable para guardar el partido válido más cercano
ultimo_partido_valido = None

# Lógica para procesar la columna 'partido'
for index in df_filtrado.index:
    candidato = df_filtrado.at[index, 'candidato']
    partido = df_filtrado.at[index, 'partido']
    aux = df_filtrado.at[index, 'aux']
    
    # Si el partido está vacío pero es "Votos Nulos" o "Votos Blancos"
    if pd.isna(partido) and candidato in ["Votos Nulos", "Votos Blancos"]:
        df_filtrado.at[index, 'partido'] = candidato   
    
    # Si el partido es válido y no es "IND", actualizar el último partido válido
    elif pd.notna(aux) and pd.isna(partido):
        ultimo_partido_valido = aux
    
    # Si el partido es "IND", usar el último partido válido
    elif partido == "IND":
        if ultimo_partido_valido:
            df_filtrado.at[index, 'partido'] = f"IND - {ultimo_partido_valido}"
        else:
            # Si no hay un partido válido previo, mantener como "IND"
            df_filtrado.at[index, 'partido'] = "IND"
            
# Eliminar filas con partido vacío al final
df_filtrado = df_filtrado.dropna(subset=['partido'])

# Reiniciar índices después del filtrado
df_filtrado.reset_index(drop=True, inplace=True)# Reiniciar índices después del filtrado
#df_filtrado.reset_index(drop=True, inplace=True)

#Se asumen que todos los votos del partido POPULAR son de PH

#['partido'] = cores2024_filtrado['partido'].replace("POPULAR", "PH")
#cores2024_filtrado.loc[cores2024_filtrado['candidato'] == "B - IZQUIERDA ECOLOGISTA POPULAR", 'partido'] = "PH"

#PL=['DE ARICA Y PARINACOTA','DE TARAPACA','DE ANTOFAGASTA','DE VALPARAISO','METROPOLITANA DE SANTIAGO','DE ÑUBLE','DEL BIOBIO','DE LA ARAUCANIA','DE LOS LAGOS']
#FREVS=['DE ARICA Y PARINACOTA','DE TARAPACA','DE ANTOFAGASTA','DE ATACAMA','DE COQUIMBO','DE VALPARAISO','METROPOLITANA DE SANTIAGO',"DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS",'DEL MAULE','DE ÑUBLE','DEL BIOBIO','DE LA ARAUCANIA','DE LOS RIOS','DE LOS LAGOS','DE AYSEN DEL GENERAL CARLOS IBAÑEZ DEL CAMPO']



# Reemplazar "IND - FREVS" en 'partido' por "IND - FREVS/PL y similares"
df_filtrado['partido'] = df_filtrado.apply(
    lambda row: "IND - FREVS/PL" if row['partido'] == "IND - FREVS" else row['partido'],
    axis=1
)


df_filtrado['partido'] = df_filtrado.apply(
    lambda row: "IND - FREVS/PL" if row['partido'] == "IND - PL" else row['partido'],
    axis=1
)

df_filtrado['partido'] = df_filtrado.apply(
    lambda row: "IND - POPULAR/PH/IGUALDAD" if row['partido'] == "IND - POPULAR" else row['partido'],
    axis=1
)

df_filtrado['partido'] = df_filtrado.apply(
    lambda row: "IND - POPULAR/PH/IGUALDAD" if row['partido'] == "IND - PH" else row['partido'],
    axis=1
)

df_filtrado['partido'] = df_filtrado.apply(
    lambda row: "IND - POPULAR/PH/IGUALDAD" if row['partido'] == "IND - IGUALDAD" else row['partido'],
    axis=1
)

df_filtrado = df_filtrado.groupby(['comuna','partido']).agg({
    'votos': 'sum',
    'region': 'first',
    })

ruta_salida = r"C:\Users\Ivan\OneDrive\Asesorias varias-PCIvan\Datos electorales\EstrategiaSur\Scrapeos\cores2024_definitivo.csv"
df_filtrado.to_csv(ruta_salida, index=True, encoding='utf-8-sig')



#Hasta acá voy bien


#Repite la operación para concejales
import pandas as pd
#cargar los datos
ruta_concejales2024 = r"C:\Users\Ivan\OneDrive\Asesorias varias-PCIvan\Datos electorales\EstrategiaSur\Scrapeos\concejales_servel_comunas_nacional.xlsx"
# Cargar los datos
df_2 = pd.read_excel(ruta_concejales2024)


df_2_filtrado = df_2.copy()  # Crear una copia para manipulación

# Variable para guardar el partido válido más cercano
ultimo_partido_valido = None

# Lógica para procesar la columna 'partido'
for index in df_2_filtrado.index:
    candidato = df_2_filtrado.at[index, 'candidato']
    partido = df_2_filtrado.at[index, 'partido']
    aux = df_2_filtrado.at[index, 'aux']
    
    # Si el partido está vacío pero es "Votos Nulos" o "Votos Blancos"
    if pd.isna(partido) and candidato in ["Votos Nulos", "Votos Blancos"]:
        df_2_filtrado.at[index, 'partido'] = candidato

    # Si el partido es válido y no es "IND", actualizar el último partido válido
    elif pd.notna(aux) and pd.isna(partido):
        ultimo_partido_valido = aux
    
    
    # Si el partido es "IND", usar el último partido válido
    elif partido == "IND":
        if ultimo_partido_valido:
            df_2_filtrado.at[index, 'partido'] = f"IND - {ultimo_partido_valido}"
        else:
            # Si no hay un partido válido previo, mantener como "IND"
            df_2_filtrado.at[index, 'partido'] = "IND"
            
# Eliminar filas con partido vacío al final
df_2_filtrado = df_2_filtrado.dropna(subset=['partido'])

# Reiniciar índices después del filtrado
df_2_filtrado.reset_index(drop=True, inplace=True)# Reiniciar índices después del filtrado

# Reemplazar "IND - FREVS" en 'partido' por "IND - FREVS/PL"
df_2_filtrado['partido'] = df_2_filtrado.apply(
    lambda row: "IND - FREVS/PL" if row['partido'] == "IND - FREVS" else row['partido'],
    axis=1
)

# Reemplazar "IND - FREVS" en 'partido' por "IND - FREVS/PL"
df_2_filtrado['partido'] = df_2_filtrado.apply(
    lambda row: "IND - FREVS/PL" if row['partido'] == "IND - PL" else row['partido'],
    axis=1
)

df_2_filtrado['partido'] = df_2_filtrado.apply(
    lambda row: "IND - POPULAR/PH/IGUALDAD" if row['partido'] == "IND - POPULAR" else row['partido'],
    axis=1
)

df_filtrado['partido'] = df_2_filtrado.apply(
    lambda row: "IND - POPULAR/PH/IGUALDAD" if row['partido'] == "IND - PH" else row['partido'],
    axis=1
)

df_2_filtrado['partido'] = df_2_filtrado.apply(
    lambda row: "IND - POPULAR/PH/IGUALDAD" if row['partido'] == "IND - IGUALDAD" else row['partido'],
    axis=1
)

df_2_filtrado = df_2_filtrado.groupby(['comuna','partido']).agg({
    'votos': 'sum',
    'region': 'first',
    })
ruta_salida = r"C:\Users\Ivan\OneDrive\Asesorias varias-PCIvan\Datos electorales\EstrategiaSur\Scrapeos\concejales2024_definitivo.csv"
df_2_filtrado.to_csv(ruta_salida, index=True, encoding='utf-8-sig')



#DESDE AQUI COMIENZA OTRO CÓDIGO, DESCOMENTAR PARA USAR
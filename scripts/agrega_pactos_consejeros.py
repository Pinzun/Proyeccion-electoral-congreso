import pandas as pd
"Este codigo es un auxuliar que agrega pactos al archivo Proyeccion-electoral-congreso/Elecciones/cores_servel_comunas_nacional.xlsx"
#ruta="../Elecciones/consejeros_servel_comunas_nacional.xlsx"
ruta=r"C:\Users\EstrategiaSur\Proyeccion-electoral-congreso\Elecciones\consejeros_servel_comunas_nacional.xlsx"
df=pd.read_excel(ruta)
# Diccionario de secuencias
secuencia = {
    "PARTIDO DE LA GENTE": "A - PARTIDO DE LA GENTE",
    "PARTIDO DEMOCRATA CRISTIANO": "B - TODO POR CHILE",
    "PARTIDO REPUBLICANO DE CHILE": "C - PARTIDO REPUBLICANO DE CHILE",
    "ACCION HUMANISTA": "D - UNIDAD PARA CHILE",
    "INDEPENDIENTE": "ZZI - INDEPENDIENTES"
}

# Lista para almacenar nuevas filas
nuevas_filas = []

# Iterar sobre el DataFrame original
for index, row in df.iterrows():
    if row["partido"] in secuencia and (row["partido"]!=df.iloc[index + 1]["partido"]):
        # Crear nueva fila
        nueva_fila = {"partido": None, "candidato": secuencia[row["partido"]], "votos": None,"region":row["region"],"comuna":row["comuna"]}
        nuevas_filas.append((index, nueva_fila))
        print(nuevas_filas)

# Insertar las nuevas filas en el DataFrame
for offset, (index, new_row) in enumerate(nuevas_filas):
    df = pd.concat([df.iloc[:index + offset], pd.DataFrame([new_row]), df.iloc[index + offset:]]).reset_index(drop=True)

# Detectar filas donde la columna "votos" está vacía
#df["votos_vacio"] = df["votos"].isna()

# Almacenar los índices de las celdas vacías en la columna "votos"
indices_votos_vacios = df[df["votos"].isna()].index.tolist()
print("Índices de celdas vacías en 'votos':", indices_votos_vacios)

# Sumar valores entre índices consecutivos de celdas vacías en "votos"
sumas_votos = {}
for i in range(len(indices_votos_vacios) - 1):
    inicio, fin = indices_votos_vacios[i], indices_votos_vacios[i + 1]
    suma = df.loc[inicio + 1:fin - 1, "votos"].sum()
    sumas_votos[inicio] = suma

print("Suma de votos entre índices consecutivos vacíos:", sumas_votos)

# Reemplazar en la columna "votos" el valor correspondiente del diccionario
for key, value in sumas_votos.items():
    df.at[key, "votos"] = value

#df.to_excel(ruta, index=False)
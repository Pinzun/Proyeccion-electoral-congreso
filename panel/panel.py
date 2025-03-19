import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from Calcula_integracion_dip import calcula_integracion as calcular

# Crear una lista con los valores para la columna 'Partido'
partidos = [
    'FA', 'FREVS', 'AH', 'PL', 'PCCH', 'PR', 'PDC', 'PPD', 'PS', 'UDI', 'DEMOCRATAS', 
    'AMARILLOS', 'RN', 'EVOPOLI', 'PSC', 'REPUBLICANO', 'POPULAR', 'PAVP', 'IGUALDAD', 
    'PH', 'PTR', 'PDG', 'IND'
]

# Crear un dataframe de ejemplo con columnas 'Partido' y 'Pacto'
data = {
    'Partido': partidos,
    'Pacto': ['' for _ in partidos]  # Inicia la columna 'Pacto' vacía
}

df = pd.DataFrame(data)

# Mostrar la tabla estilo Excel
st.title('Constructor de pactos')

# Configurar la tabla para permitir la edición
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("Pacto", editable=True)  # Hacer que la columna 'Pacto' sea editable
gridOptions = gb.build()

# Mostrar la tabla estilo Excel
# Mostrar la tabla interactiva con edición habilitada
grid_response = AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)

# Obtener los datos actualizados después de la edición
df_edited = grid_response['data']
# Mostrar la tabla actualizada

#st.dataframe(df_edited)'

# Crear el botón 'Calcular'
if st.button('Calcular'):
    calcular(df_edited)  # Llamar a la función cuando se presiona el botón

import pandas as pd
import numpy as np

ruta1=r"C:\Users\Ivan\Desktop\Ivan\Laboral\EstrategiaSur\Trabajo Bancada\resultados_proyectados_por_pacto_v1.csv"
ruta2=r"C:\Users\Ivan\Desktop\Ivan\Laboral\EstrategiaSur\Trabajo Bancada\resultados_proyectados_por_pacto_v2.csv"
ruta3=r"C:\Users\Ivan\Desktop\Ivan\Laboral\EstrategiaSur\Trabajo Bancada\resultados_proyectados_por_pacto_v3.csv"
ruta4=r"C:\Users\Ivan\Desktop\Ivan\Laboral\EstrategiaSur\Trabajo Bancada\resultados_proyectados_por_pacto_v4.csv"
ruta5=r"C:\Users\Ivan\Desktop\Ivan\Laboral\EstrategiaSur\Trabajo Bancada\resultados_proyectados_por_pacto_v5.csv"

df1=pd.read_csv(ruta1, sep=';', encoding='utf-8-sig')
df2=pd.read_csv(ruta2, sep=';', encoding='utf-8-sig')
df3=pd.read_csv(ruta3, sep=';', encoding='utf-8-sig')
df4=pd.read_csv(ruta4, sep=';', encoding='utf-8-sig')
df5=pd.read_csv(ruta5, sep=';', encoding='utf-8-sig')
# Asume que tienes los 5 DataFrames cargados en una lista
dataframes = [df1, df2, df3, df4, df5]  # Sustituye df2, df3, etc., con los otros DataFrames

# Paso 1: Consolidar datos
# Crear un DataFrame consolidado con el promedio, mediana, desviación estándar, rango
consolidated = pd.concat(dataframes, axis=0, keys=range(len(dataframes)))
grouped = consolidated.groupby(level=1)

# Calcular estadísticas
summary_stats = pd.DataFrame({
    'mean': grouped.mean().mean(axis=0),
    'median': grouped.median().mean(axis=0),
    'std_dev': grouped.std().mean(axis=0),
    'range': grouped.max().max(axis=0) - grouped.min().min(axis=0)
})

# Paso 2: Detectar diferencias extremas
# Crear un DataFrame para diferencias absolutas entre cada DataFrame y la media
differences = {f'diff_{i}': (df - summary_stats['mean']).abs() for i, df in enumerate(dataframes)}

# Identificar outliers (valores mayores a 2 desviaciones estándar)
outliers = {
    f'outliers_{i}': diff > (2 * summary_stats['std_dev'])
    for i, diff in differences.items()
}

# Paso 3: Resumen de valores extremos
# Calcular el número de celdas extremas por DataFrame
outlier_summary = {key: value.sum().sum() for key, value in outliers.items()}
outlier_summary_df = pd.DataFrame.from_dict(outlier_summary, orient='index', columns=['outlier_count'])

# Paso 4: Visualización (Ejemplo con Matplotlib)
import matplotlib.pyplot as plt

# Boxplot para comparar distribuciones de los DataFrames
plt.figure(figsize=(10, 6))
pd.concat(dataframes, axis=0).boxplot()
plt.title('Distribuciones de los DataFrames')
plt.xticks(rotation=90)
plt.show()

# Heatmap para mostrar la dispersión
import seaborn as sns
plt.figure(figsize=(12, 8))
sns.heatmap(summary_stats, annot=True, fmt=".2f", cmap="coolwarm")
plt.title('Resumen de Estadísticas Consolidadas')
plt.show()

# Guardar resultados
summary_stats.to_csv('summary_stats.csv')
outlier_summary_df.to_csv('outlier_summary.csv')

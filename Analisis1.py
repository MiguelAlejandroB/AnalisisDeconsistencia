import pandas as pd
import numpy as np
from scipy.stats import linregress

# Leer el CSV y asegurarse de que 'Fecha' es datetime
try:
    data = pd.read_csv('Alone.csv', parse_dates=['Fecha'], dayfirst=True)
except pd.errors.ParserError:
    print("Hubo un problema con el archivo Alone.csv.")
    sys.exit()

# Eliminar filas con valores nulos en 'Fecha' y 'Valor'
data.dropna(subset=['Fecha', 'Valor'], inplace=True)
# Asegurarse que Fecha esta en el formato que debe estar
data['Fecha'] = pd.to_datetime(data['Fecha'], errors='coerce', dayfirst=True)
# Asegurarse de que 'Valor' es numérico
data['Valor'] = pd.to_numeric(data['Valor'], errors='coerce')

# Filtrar datos con 'Fecha' válida
data = data[data['Fecha'].notnull()]

# Obtener los años únicos en la columna 'Fecha'
years = pd.to_datetime(data['Fecha'], errors='coerce').dt.year.unique()

# Inicializar una lista para almacenar los resultados
resultados = []

# Iterar a través de los años y realizar el análisis
for year in years:
    # Filtrar los datos para el año actual
    data_year = data[data['Fecha'].dt.year == year].copy()  # Copia para evitar SettingWithCopyWarning

    # Calcular datos acumulados de manera segura usando .loc
    data_year.loc[:, 'caudal_acumulado'] = data_year['Valor'].cumsum()

    # Aplicar regresión lineal
    slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(data_year)), data_year['caudal_acumulado'])

    # Almacenar los resultados en la lista
    resultados.append({
        'Año': year,
        'Slope': slope,
        'Std_Err': std_err,
        'R_Value': r_value
    })

# Convertir la lista de resultados en un DataFrame
df_resultados = pd.DataFrame(resultados)

# Definir el valor límite
valor_limite = 0.97

# Contar los datos por debajo del valor límite
num_datos_debajo_limite = (df_resultados['R_Value'] < valor_limite).sum()

# Calcular el porcentaje de datos inconsistentes
porcentaje_inconsistentes = (num_datos_debajo_limite / len(df_resultados)) * 100

# Determinar el resultado final
if porcentaje_inconsistentes < 10:
    resultado = 0  # Es consistente
else:
    resultado = 1  # No es consistente

print(f"Porcentaje de datos inconsistentes: {porcentaje_inconsistentes:.2f}%")
print(f"Resultado final: {resultado}")

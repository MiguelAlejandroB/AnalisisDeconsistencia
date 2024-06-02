import pandas as pd
import numpy as np
from scipy.stats import linregress


def analisis_consistencia(csv_file1,csv_file2, valor_limite=0.97):
    try:
        # Leer el CSV y asegurarse de que 'Fecha' es datetime
        data1 = pd.read_csv(csv_file1, parse_dates=['Fecha'], dayfirst=True)
        data2 = pd.read_csv(csv_file2, parse_dates=['Fecha'], dayfirst=True)
    except pd.errors.ParserError:
        print(f"Hubo un problema con el archivo {csv_file}.")
        return None

    # Eliminar filas con valores nulos en 'Fecha' y 'Valor'
    data1.dropna(subset=['Fecha', 'Valor'], inplace=True)
    # Asegurarse que Fecha esta en el formato que debe estar
    data1['Fecha'] = pd.to_datetime(data1['Fecha'], errors='coerce', dayfirst=True)
    # Asegurarse de que 'Valor' es numérico
    data1['Valor'] = pd.to_numeric(data1['Valor'], errors='coerce')

    # Eliminar filas con valores nulos en 'Fecha' y 'Valor'
    data2.dropna(subset=['Fecha', 'Valor'], inplace=True)
    # Asegurarse que Fecha esta en el formato que debe estar
    data2['Fecha'] = pd.to_datetime(data2['Fecha'], errors='coerce', dayfirst=True)
    # Asegurarse de que 'Valor' es numérico
    data2['Valor'] = pd.to_numeric(data2['Valor'], errors='coerce')

    # Filtrar datos con 'Fecha' válida
    data1 = data1[data1['Fecha'].notnull()]

    # Filtrar datos con 'Fecha' válida
    data2 = data2[data2['Fecha'].notnull()]

    # Obtener los años únicos en la columna 'Fecha'
    years1 = pd.to_datetime(data1['Fecha'], errors='coerce').dt.year.unique()
    years2 = pd.to_datetime(data2['Fecha'], errors='coerce').dt.year.unique()
    if len(years1) > len(years2):
        years = years2
    else:
        years = years1
    # Inicializar una lista para almacenar los resultados
    resultados = []

    # Iterar a través de los años y realizar el análisis
    for year in years:
        # Filtrar los datos para el año actual
        data_year1 = data1[data1['Fecha'].dt.year == year].copy()  # Copia para evitar SettingWithCopyWarning
        data_year2 = data2[data2['Fecha'].dt.year == year].copy()  # Copia para evitar SettingWithCopyWarning

        # Calcular datos acumulados de manera segura usando .loc
        data_year1.loc[:, 'caudal_acumulado'] = data_year1['Valor'].cumsum()
        data_year2.loc[:, 'caudal_acumulado'] = data_year2['Valor'].cumsum()

        # Aplicar regresión lineal
        slope, intercept, r_value, p_value, std_err = linregress(data_year2['caudal_acumulado'],
                                                                 data_year1['caudal_acumulado'])

        # Almacenar los resultados en la lista
        resultados.append({
            'Año': year,
            'Slope': slope,
            'Std_Err': std_err,
            'R_Value': r_value
        })

    # Convertir la lista de resultados en un DataFrame
    df_resultados = pd.DataFrame(resultados)

    # Contar los datos por debajo del valor límite
    num_datos_debajo_limite = (df_resultados['R_Value'] < valor_limite).sum()

    # Calcular el porcentaje de datos inconsistentes
    porcentaje_inconsistentes = (num_datos_debajo_limite / len(df_resultados)) * 100

    # Determinar el resultado final
    if porcentaje_inconsistentes < 10:
        return true  # Es consistente
    else:
        return false  # No es consistente

# Ejemplo de uso de la función
archivo_csv1 = 'Incon.csv'
archivo_csv2 = 'Alone.csv'
resultado_final = analisis_consistencia(archivo_csv1,archivo_csv2)
print(f"Resultado final: {resultado_final}")



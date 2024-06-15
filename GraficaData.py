import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os
# Carpeta que contiene los archivos CSV
csv_folder = 'estaciones_consistencia_csv'
output_dir = 'GraficasPendientes'

# Verificar y crear el directorio de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Listar todos los archivos CSV en la carpeta
for file_name in os.listdir(csv_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_folder, file_name)
        # Leer el csv
        data = pd.read_csv(file_path, parse_dates=['Fecha'], dayfirst=True)
        # Obtener el nombre base del archivo sin la extensión
        base_name = os.path.splitext(file_name)[0]
        # Crear la ruta del directorio donde se guardarán las gráficas
        output_dir = 'GraficasPendientes'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Asegurarse de que 'Fecha' es datetime
        data['Fecha'] = pd.to_datetime(data['Fecha'], errors='coerce', dayfirst=True)
        # Verificar si hay valores nulos en 'Fecha' y 'Valor' después de la conversión y eliminarlos
        data = data.dropna(subset=['Fecha', 'Valor'])
        # Asegurarse de que 'Valor' es numérico
        data['Valor'] = pd.to_numeric(data['Valor'], errors='coerce')
        df = pd.DataFrame()
        df = df.assign(Fecha=None, slope=None, std_err=None, r_values=None)
        # Obtener los años únicos en la columna 'Fecha'
        years = data['Fecha'].dt.year.unique()
        datos = pd.DataFrame()
        array = []

        # Crear el DataFrame dfAcumu
        dfAcumu = pd.DataFrame({
            'Fecha': data['Fecha'],
            'Valor': data['Valor'].cumsum()
        })
        # Iterar a través de los años y hacer lo que necesites con los datos de cada año
        for year in years:
            # Filtrar los datos para el año actual
            data_year = data[data['Fecha'].dt.year == year]
            # Datos acumulados
            datos['caudal_acumulado'] = data_year['Valor'].cumsum()
            # Regresion lineal
            slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(datos)), datos['caudal_acumulado'])
            array.append((slope, std_err, year, r_value,))
            datos = pd.DataFrame()
        for i in array:
            row = [i[2], i[0], i[1], i[3]]
            df.loc[len(df)] = row

        # Configurar las gráficas para el primer DataFrame
        fig, axs = plt.subplots(3, 1, figsize=(10, 15), sharex=True)
        fig.suptitle(f'Gráficas del archivo: {file_name}', fontsize=16)
        # Gráfica de slope
        axs[0].plot(df['Fecha'], df['slope'], marker='o', linestyle='-')
        axs[0].set_title('Slope vs Tiempo')
        axs[0].set_ylabel('Slope')
        axs[0].grid(True)

        # Gráfica de std_err
        axs[1].plot(df['Fecha'], df['std_err'], marker='o', linestyle='-')
        axs[1].set_title('Error estandar vs Tiempo')
        axs[1].set_ylabel('Error estandar')
        axs[1].grid(True)

        # Gráfica de r_values
        axs[2].plot(df['Fecha'], df['r_values'], marker='o', linestyle='-')
        axs[2].set_title('R Valores vs Tiempo')
        axs[2].set_xlabel('Fecha')
        axs[2].set_ylabel('R Valores')
        axs[2].grid(True)

        # Asegurarse de que los años se muestren correctamente en el eje x
        plt.xticks(df['Fecha'].astype(int))
        # Rotar las etiquetas del eje x para que no se amontonen
        plt.setp(axs[2].get_xticklabels(), rotation=45, ha='right')
        # Mostrar las gráficas
        plt.tight_layout()

        # Guardar la primera figura como PNG con el nombre del archivo y sufijo _slope
        fig.savefig(os.path.join(output_dir, f'{base_name}_slope.png'))

        plt.show()

        # Configurar la gráfica para dfAcumu
        # plt.figure(figsize=(10, 6))
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        plt.plot(dfAcumu['Fecha'], dfAcumu['Valor'], marker='o', linestyle='-')
        plt.title('Caudal Acumulado vs Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Caudal Acumulado')
        plt.grid(True)

        # Rotar las etiquetas del eje x para que no se amontonen
        plt.xticks(rotation=45, ha='right')

        # Mostrar la gráfica
        plt.tight_layout()

        # Guardar la segunda figura como PNG con el nombre del archivo y sufijo _CauAcum
        fig2.savefig(os.path.join(output_dir, f'{base_name}_CauAcum.png'))

        plt.show()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import os
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
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
        # Extraer el año de la fecha
        dfAcumu['Año'] = dfAcumu['Fecha'].dt.year
        # Calcular el caudal acumulado acumulativo por año en dfAcumu
        dfAcumu['Caudal_Acumulado'] = dfAcumu.groupby('Año')['Valor'].cumsum()

        # Calcular el caudal acumulado acumulativo por año en dfAcumu_anual
        dfAcumu_anual = dfAcumu.groupby('Año')['Valor'].max().reset_index()

        # Carpeta donde se guardará el archivo
        carpeta_salida = "Acumulado"
        # Nombre completo del archivo CSV
        archivo_salida = os.path.join(carpeta_salida, f"{base_name}_CauAcum.csv")
        # Guardar el DataFrame en un archivo CSV
        dfAcumu_anual.to_csv(archivo_salida, index=False)
        if base_name=='Datos84Consis':
            print(dfAcumu_anual)
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
        # Calcular el promedio y la desviación estándar de las pendientes
        mean_slope = df['slope'].mean()
        std_slope = df['slope'].std()
        # Calcular el promedio y la desviación estándar de las stderror
        mean_std = df['std_err'].mean()
        std_std = df['std_err'].std()
        # Calcular el promedio y la desviación estándar del r value
        mean_r = df['r_values'].mean()
        std_r = df['r_values'].std()


        # Configurar las gráficas para el primer DataFrame
        fig, axs = plt.subplots(3, 1, figsize=(25, 15), sharex=True)  # Aumentar el tamaño de la figura horizontalmente
        fig.suptitle(f'Gráficas del archivo: {file_name}', fontsize=16)
        # Gráfica de slope
        axs[0].plot(df['Fecha'], df['slope'], marker='o', linestyle='-')
        axs[0].axhline(mean_slope, color='r', linestyle='--', label='Promedio')
        axs[0].axhline(mean_slope + std_slope, color='g', linestyle='--', label='Promedio + Desv. Estándar')
        axs[0].axhline(mean_slope - std_slope, color='b', linestyle='--', label='Promedio - Desv. Estándar')
        axs[0].set_title('Slope vs Tiempo')
        axs[0].set_ylabel('Slope')
        axs[0].grid(True)
        axs[0].legend()
        # Gráfica de std_err
        axs[1].plot(df['Fecha'], df['std_err'], marker='o', linestyle='-')
        axs[1].axhline(mean_std, color='r', linestyle='--', label='Promedio')
        axs[1].axhline(mean_std + std_std, color='g', linestyle='--', label='Promedio + Desv. Estándar')
        axs[1].axhline(mean_std - std_std, color='b', linestyle='--', label='Promedio - Desv. Estándar')
        axs[1].set_title('Error estandar vs Tiempo')
        axs[1].set_ylabel('Error estandar')
        axs[1].grid(True)

        # Gráfica de r_values
        axs[2].plot(df['Fecha'], df['r_values'], marker='o', linestyle='-')
        axs[2].axhline(mean_r, color='r', linestyle='--', label='Promedio')
        axs[2].axhline(mean_r + std_r, color='g', linestyle='--', label='Promedio + Desv. Estándar')
        axs[2].axhline(mean_r - std_r, color='b', linestyle='--', label='Promedio - Desv. Estándar')
        axs[2].set_title('R Valores vs Tiempo')
        axs[2].set_xlabel('Fecha')
        axs[2].set_ylabel('R Valores')
        axs[2].grid(True)

        # Asegurarse de que los años se muestren correctamente en el eje x
        plt.xticks(df['Fecha'].astype(int))
        # Ajustar los límites del eje x para mostrar todos los años disponibles
        #axs.set_xlim(df['fecha'].min() - 1, df['fecha'].max() + 1)

        # Rotar las etiquetas del eje x para que no se amontonen
        plt.setp(axs[2].get_xticklabels(), rotation=45, ha='right')
        # Mostrar las gráficas
        plt.tight_layout()

        # Guardar la primera figura como PNG con el nombre del archivo y sufijo _slope
        fig.savefig(os.path.join(output_dir, f'{base_name}_slope.png'))

        plt.show()

        # Configurar la gráfica para dfAcumu
        # plt.figure(figsize=(10, 6))
        fig2, ax2 = plt.subplots(figsize=(15, 6),sharex=True)
        ax2.plot(dfAcumu_anual['Año'], dfAcumu_anual['Valor'], marker='o', linestyle='-',
                 linewidth=1)  # Ajustar el grosor de la línea
        plt.title('Caudal Acumulado vs Tiempo')
        plt.xlabel('Fecha')
        plt.ylabel('Caudal Acumulado')
        plt.grid(True)

        # Configurar el eje x para mostrar cada año de manera explícita
        ax2.xaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Ajustar el localizador para enteros
        ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:d}'.format(int(x))))  # Formatear como enteros

        # Ajustar el tamaño de la fuente de los ticks del eje x
        plt.xticks(fontsize=10)
        # Rotar las etiquetas del eje x para que no se amontonen
        plt.xticks(rotation=45, ha='right')

        # Mostrar la gráfica
        plt.tight_layout()

        # Guardar la segunda figura como PNG con el nombre del archivo y sufijo _CauAcum
        fig2.savefig(os.path.join(output_dir, f'{base_name}_CauAcum.png'))

        plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
#Leer el csv
data = pd.read_csv('Alone.csv', parse_dates=['Fecha'],dayfirst=True)
# Asegurarse de que 'Fecha' es datetime
data['Fecha'] = pd.to_datetime(data['Fecha'], errors='coerce', dayfirst=True)
# Verificar si hay valores nulos en 'Fecha' y 'Valor' después de la conversión y eliminarlos
data = data.dropna(subset=['Fecha', 'Valor'])
# Asegurarse de que 'Valor' es numérico
data['Valor'] = pd.to_numeric(data['Valor'], errors='coerce')
df = pd.DataFrame()
df = df.assign(Fecha=None, slope=None, std_err=None,r_values=None)
# Obtener los años únicos en la columna 'Fecha'
years = data['Fecha'].dt.year.unique()
datos = pd.DataFrame()
array = []

# Iterar a través de los años y hacer lo que necesites con los datos de cada año
for year in years:
    # Filtrar los datos para el año actual
    data_year = data[data['Fecha'].dt.year == year]
    #Datos acumulados
    datos['caudal_acumulado'] = data_year['Valor'].cumsum()
    # Regresion lineal
    slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(datos)), datos['caudal_acumulado'])
    array.append((slope,std_err,year,r_value))
    datos = pd.DataFrame()
for i in array:
  row = [i[2], i[0], i[1],i[3]]
  df.loc[len(df)] = row

# Definir el valor límite
valor_limite = 0.97

# Contar los datos por debajo del valor límite
num_datos_debajo_limite = (df['r_values'] < valor_limite).sum()
Porcentaje = (num_datos_debajo_limite/(len(df))) * 100

if Porcentaje < 10:
    Resultado = 0 #Es consistente
else:
    resultado = 1 #No es consistente
print(Resultado)

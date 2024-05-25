import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
#Leer el csv
data = pd.read_csv('Alone.csv', parse_dates=['Fecha'],dayfirst=True)
#Datos acumulados
data['caudal_acumulado'] = data['Valor'].cumsum()
#Calcular estadisticas
media_caudal = data['caudal_acumulado'].mean()
desviacion_estandar = data['caudal_acumulado'].std()
RangoInferior = -desviacion_estandar
RangoSuperior = desviacion_estandar
#Regresión lineal
slope, intercept, r_value, p_value, std_err = linregress(np.arange(len(data)), data['caudal_acumulado'])
# Calcular la pendiente y la desviación estándar


if RangoInferior <= slope <= RangoSuperior:
    print("La pendiente es mayor que la desviación estándar, los datos pueden no ser consistentes.")
else:
    print("La pendiente es menor o igual a la desviación estándar, los datos son consistentes.")
print(slope)
print(RangoInferior)
print(RangoSuperior)
#  Visualizar los datos
plt.figure(figsize=(10, 6))
plt.plot(data['Fecha'], data['caudal_acumulado'], label='Caudal')
plt.xlabel('Fecha')
plt.ylabel('Caudal')
plt.title('Datos de Caudal')
plt.legend()
plt.show()
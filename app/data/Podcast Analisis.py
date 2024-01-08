import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('base_datos.csv')

media_precipitaciones = df[df['Región'] == "Oriente"]['Precipitaciones'].mean()

print(media_precipitaciones)

media_humedad = df[df['Región'] == "Centro"]['Humedad Relat'].mean()

print(media_humedad)

media_humedadd = df[df['Provincias'] == "Santiago de Cuba"]['Precipitaciones'].mean()
print(media_humedadd)
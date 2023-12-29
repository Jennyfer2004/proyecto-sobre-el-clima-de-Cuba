import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import folium
from folium.plugins import HeatMap
import streamlit.components.v1 as components

df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", "Humedad Relat", "Precipitaciones",
        "Nombres Estaciones", "Latitud", "Longitud", "Región", "Provincias"]]

df = df.rename(columns={"Temperatura max med": "Temperatura Maxima Media", "Temperatura min med": "Temperatura Minima Media", "Temperatura med": "Temperatura Media", "Humedad Relat": "Humedad Relativa",
        "Nombres Estaciones": "Nombre de Estacion"})

a = st.markdown("## Seleccione la region en la que quiere explorar datos")

opciones = ['General', 'Occidente', 'Centro', 'Oriente']
seleccion = st.selectbox('Selecciona una opción:', opciones)

if seleccion == "General":
    
################################################
#COEFICIENTE DE CORRELACION
################################################

        st.markdown("### Coeficiente de Correlacion entre las variables")
        df_corr = df[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        st.write('''Como es posible observar, en Cuba una Temperatura Maxima Media elevada esta directamente una Temperatura Minima Media tambien elevada. Esto nos indica que los lugares donde se registaron
         temperaturas altas, las temperaturas minimas fueron tambien mas altas si las comparamos con luagres donde se registraron menores temperaturas maximas. Asimismo, notamos que 
         las Precipitaciones estan mas relacionadas con el incremento de la humedad relativa que con otras variables. Resulta tambien intersante que, a pesar de que la relacion entre la Humedad 
         Relativa y las temperaturas maximas es pequena, estas variables son inversamente proporcionales.''')
        
#################################################
#Nubes de Puntos
#################################################
        
        st.markdown("### Graficos de Dispersion")

        inicio_año, fin_año = st.slider('Selecciona el rango de años', min_value=df['Año'].min(), max_value=df['Año'].max(), value=(df['Año'].min(), df['Año'].max()))
        inicio_mes, fin_mes = st.slider('Selecciona el rango de meses', min_value=df['Mes'].min(), max_value=df['Mes'].max(), value=(df['Mes'].min(), df['Mes'].max()))

        df_filtrado = df[(df['Año'] >= inicio_año) & (df['Año'] <= fin_año) & (df['Mes'] >= inicio_mes) & (df['Mes'] <= fin_mes)]

        variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']
        variable_x = st.selectbox('Selecciona la variable para el eje X', variables)
        variable_y = st.selectbox('Selecciona la variable para el eje Y', variables)

        col1,col2 = st.columns(2)
        plt.figure(figsize=(12, 8))
        plt.scatter(df_filtrado[variable_x], df_filtrado[variable_y], s=3)
        linea_media_x = plt.axvline(np.mean(df_filtrado[variable_x]), color="red", linestyle = "dashed")
        linea_media_y = plt.axhline(np.mean(df_filtrado[variable_y]), color="red", linestyle = "dashed")
        plt.title('Gráfico de dispersión')
        plt.xlabel(variable_x)
        plt.ylabel(variable_y)
        legend = plt.legend([linea_media_x, linea_media_y], [f'Media {variable_x}: {np.mean(df_filtrado[variable_x]):.2f}', f'Media {variable_y}: {np.mean(df_filtrado[variable_y]):.2f}'], loc='upper left')
        col1.pyplot(plt.gcf())
        
        plt.figure(figsize=(10, 6))
        sns.kdeplot(data=df_filtrado, x=variable_x, y=variable_y, fill=True)
        linea_media_x = plt.axvline(np.mean(df_filtrado[variable_x]), color="red", linestyle = "dashed")
        linea_media_y = plt.axhline(np.mean(df_filtrado[variable_y]), color="red", linestyle = "dashed")
        plt.title(f'Diagrama de densidad de {variable_x} vs {variable_y}')
        plt.xlabel(variable_x)
        plt.ylabel(variable_y)

        col2.pyplot(plt.gcf())

#################################################
#Mapas de Calor
#################################################
        
#         variable1 = st.selectbox('Selecciona la primera variable:', variables)
#         variable2 = st.selectbox('Selecciona la segunda variable:', [var for var in variables if var != variable1])

#         df_filtrado = df[df[variable1].notna() & df[variable2].notna()]

#         data1 = df_filtrado[['Latitud', 'Longitud', variable1]].values.tolist()
#         data2 = df_filtrado[['Latitud', 'Longitud', variable2]].values.tolist()

#         m = folium.Map(location=[21.5218, -79.5812], zoom_start=7)

#         HeatMap(data1).add_to(m)
#         HeatMap(data2).add_to(m)


#         # Muestra el mapa
#         m.save('mapa.html')

#         with open('mapa.html', 'r') as f:
#                 html_string = f.read()

#         components.html(html_string, width=1000, height=400)
        
        
#################################################
#Analisis por mes/ano
#################################################
        

import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
        df_corr = df[["Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        st.write('''Como es posible observar, en Cuba una Temperatura Maxima Media elevada esta directamente una Temperatura Minima Media tambien elevada. Esto nos indica que los lugares donde se registaron
         temperaturas altas, las temperaturas minimas fueron tambien mas altas si las comparamos con luagres donde se registraron menores temperaturas maximas. Asimismo, notamos que 
         las Precipitaciones estan mas relacionadas con el incremento de la humedad relativa que con otras variables. Resulta tambien intersante que, a pesar de que la relacion entre la Humedad 
         Relativa y las temperaturas maximas es pequena, estas variables son inversamente proporcionales.''')
        
#################################################
#Nubes de Puntos
#################################################
        
        inicio_año, fin_año = st.slider('Selecciona el rango de años', min_value=df['Año'].min(), max_value=df['Año'].max(), value=(df['Año'].min(), df['Año'].max()))
        inicio_mes, fin_mes = st.slider('Selecciona el rango de meses', min_value=df['Mes'].min(), max_value=df['Mes'].max(), value=(df['Mes'].min(), df['Mes'].max()))

        df_filtrado = df[(df['Año'] >= inicio_año) & (df['Año'] <= fin_año) & (df['Mes'] >= inicio_mes) & (df['Mes'] <= fin_mes)]

        variables = ['Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']
        variable_x = st.selectbox('Selecciona la variable para el eje X', variables)
        variable_y = st.selectbox('Selecciona la variable para el eje Y', variables)

        plt.figure(figsize=(15, 11))
        plt.scatter(df_filtrado[variable_x], df_filtrado[variable_y], s=3)
        plt.axvline(np.mean(df_filtrado[variable_x]), color="red", linestyle = "dashed")
        plt.axhline(np.mean(df_filtrado[variable_y]), color="red", linestyle = "dashed")
        plt.title('Gráfico de dispersión')
        plt.xlabel(variable_x)
        plt.ylabel(variable_y)
        st.pyplot(plt.gcf())


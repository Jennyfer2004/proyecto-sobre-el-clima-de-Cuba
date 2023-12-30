import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
import datetime
import sys
import os
ruta = os.getcwd()
ruta = ruta.replace("\\", "/")
sys.path.append(f'{ruta}' + '/Analisis Multivariado')
import mvLogic



df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Estacion", "Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", "Humedad Relat", "Precipitaciones",
        "Nombres Estaciones", "Latitud", "Longitud", "Región", "Provincias"]]

df = df.rename(columns={"Temperatura max med": "Temperatura Maxima Media", "Temperatura min med": "Temperatura Minima Media", "Temperatura med": "Temperatura Media", "Humedad Relat": "Humedad Relativa",
        "Nombres Estaciones": "Nombre de Estacion"})
df_Occidente = df.loc[df['Región'] == 'Occidente']
df_Centro = df.loc[df['Región'] == 'Centro']
df_Oriente = df.loc[df['Región'] == 'Oriente']

variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']

a = st.markdown("## Seleccione la region en la que quiere explorar datos")

opciones = ['General', 'Occidente', 'Centro', 'Oriente']
seleccion = st.selectbox('Selecciona una opción:', opciones)

#############################################################################################################################
#Analisis Multivariado General
#############################################################################################################################

if seleccion == "General":
    
################################################
#COEFICIENTE DE CORRELACION
################################################

        st.markdown("### Coeficiente de Correlacion entre las variables")
        df_corr = df[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        
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

        col1.write(mvLogic.ScatterPlot(df_filtrado, variable_x, variable_y, inicio_año, fin_año, inicio_mes, fin_mes))

        col2.write(mvLogic.Dispersion(df_filtrado, variable_x, variable_y))

        
        
#################################################
#Regresiones
#################################################
        
        st.markdown("### Graficos de Regresion Lineal")
        
        variables.append("Año")
        variables.append("Longitud")

        variable_independiente = st.selectbox('Seleccione la variable independiente:', variables)

        dependientes = [var for var in df.columns if var not in ["Mes", "Año", "Longitud", "Estacion", "Nombre de Estacion", "Latitud", "Región", "Provincias"]] # Todas las variables excepto "Año" y "Longitud" pueden ser dependientes
        variable_dependiente = st.selectbox('Seleccione la variable dependiente:', dependientes)

        REWORKED_df = df.dropna(subset=[variable_independiente, variable_dependiente, 'Mes'])

        st.write(mvLogic.Regresion(REWORKED_df, variable_independiente, variable_dependiente))




############################################################################################################################
#Analisis Multivariado Occidente
############################################################################################################################
    
if seleccion == "Occidente":

################################################
#COEFICIENTE DE CORRELACION
################################################

        st.markdown("### Coeficiente de Correlacion entre las variables")
        df_corr = df_Occidente[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        
#################################################
#Nubes de Puntos
#################################################
        
        st.markdown("### Graficos de Dispersion")

        inicio_año, fin_año = st.slider('Selecciona el rango de años', min_value=df_Occidente['Año'].min(), max_value=df_Occidente['Año'].max(), value=(df_Occidente['Año'].min(), df_Occidente['Año'].max()))
        inicio_mes, fin_mes = st.slider('Selecciona el rango de meses', min_value=df_Occidente['Mes'].min(), max_value=df_Occidente['Mes'].max(), value=(df_Occidente['Mes'].min(), df_Occidente['Mes'].max()))

        df_filtrado = df_Occidente[(df_Occidente['Año'] >= inicio_año) & (df_Occidente['Año'] <= fin_año) & (df_Occidente['Mes'] >= inicio_mes) & (df_Occidente['Mes'] <= fin_mes)]

        variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']
        variable_x = st.selectbox('Selecciona la variable para el eje X', variables)
        variable_y = st.selectbox('Selecciona la variable para el eje Y', variables)

        col1,col2 = st.columns(2)

        col1.write(mvLogic.ScatterPlot(df_filtrado, variable_x, variable_y, inicio_año, fin_año, inicio_mes, fin_mes))

        col2.write(mvLogic.Dispersion(df_filtrado, variable_x, variable_y))

        
        
#################################################
#Regresiones
#################################################
        
        st.markdown("### Graficos de Regresion Lineal")
        
        variables.append("Año")
        variables.append("Longitud")

        variable_independiente = st.selectbox('Seleccione la variable independiente:', variables)

        dependientes = [var for var in df_Occidente.columns if var not in ["Mes", "Año", "Longitud", "Estacion", "Nombre de Estacion", "Latitud", "Región", "Provincias"]] # Todas las variables excepto "Año" y "Longitud" pueden ser dependientes
        variable_dependiente = st.selectbox('Seleccione la variable dependiente:', dependientes)

        REWORKED_df = df_Occidente.dropna(subset=[variable_independiente, variable_dependiente, 'Mes'])

        st.write(mvLogic.Regresion(REWORKED_df, variable_independiente, variable_dependiente))



##################################################################################################################################
#Analisis Multivariado Centro
##################################################################################################################################
    
if seleccion == "Centro":

################################################
#COEFICIENTE DE CORRELACION
################################################

        st.markdown("### Coeficiente de Correlacion entre las variables")
        df_corr = df_Centro[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        
#################################################
#Nubes de Puntos
#################################################
        
        st.markdown("### Graficos de Dispersion")

        inicio_año, fin_año = st.slider('Selecciona el rango de años', min_value=df_Centro['Año'].min(), max_value=df_Centro['Año'].max(), value=(df_Centro['Año'].min(), df_Centro['Año'].max()))
        inicio_mes, fin_mes = st.slider('Selecciona el rango de meses', min_value=df_Centro['Mes'].min(), max_value=df_Centro['Mes'].max(), value=(df_Centro['Mes'].min(), df_Centro['Mes'].max()))

        df_filtrado = df_Centro[(df_Centro['Año'] >= inicio_año) & (df_Centro['Año'] <= fin_año) & (df_Centro['Mes'] >= inicio_mes) & (df_Centro['Mes'] <= fin_mes)]

        variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']
        variable_x = st.selectbox('Selecciona la variable para el eje X', variables)
        variable_y = st.selectbox('Selecciona la variable para el eje Y', variables)

        col1,col2 = st.columns(2)

        col1.write(mvLogic.ScatterPlot(df_filtrado, variable_x, variable_y, inicio_año, fin_año, inicio_mes, fin_mes))

        col2.write(mvLogic.Dispersion(df_filtrado, variable_x, variable_y))

        
        
#################################################
#Regresiones
#################################################
        
        st.markdown("### Graficos de Regresion Lineal")
        
        variables.append("Año")
        variables.append("Longitud")

        variable_independiente = st.selectbox('Seleccione la variable independiente:', variables)

        dependientes = [var for var in df_Centro.columns if var not in ["Mes", "Año", "Longitud", "Estacion", "Nombre de Estacion", "Latitud", "Región", "Provincias"]] # Todas las variables excepto "Año" y "Longitud" pueden ser dependientes
        variable_dependiente = st.selectbox('Seleccione la variable dependiente:', dependientes)

        REWORKED_df = df_Centro.dropna(subset=[variable_independiente, variable_dependiente, 'Mes'])

        st.write(mvLogic.Regresion(REWORKED_df, variable_independiente, variable_dependiente))

##################################################################################################################################
#Analisis Multivariado Oriente
##################################################################################################################################
    
if seleccion == "Oriente":

################################################
#COEFICIENTE DE CORRELACION
################################################

        st.markdown("### Coeficiente de Correlacion entre las variables")
        df_corr = df_Oriente[["Temperatura Media", "Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
        st.write(df_corr.corr()) 

        
#################################################
#Nubes de Puntos
#################################################
        
        st.markdown("### Graficos de Dispersion")

        inicio_año, fin_año = st.slider('Selecciona el rango de años', min_value=df_Oriente['Año'].min(), max_value=df_Oriente['Año'].max(), value=(df_Oriente['Año'].min(), df_Oriente['Año'].max()))
        inicio_mes, fin_mes = st.slider('Selecciona el rango de meses', min_value=df_Oriente['Mes'].min(), max_value=df_Oriente['Mes'].max(), value=(df_Oriente['Mes'].min(), df_Oriente['Mes'].max()))

        df_filtrado = df_Oriente[(df_Oriente['Año'] >= inicio_año) & (df_Oriente['Año'] <= fin_año) & (df_Oriente['Mes'] >= inicio_mes) & (df_Oriente['Mes'] <= fin_mes)]

        variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']
        variable_x = st.selectbox('Selecciona la variable para el eje X', variables)
        variable_y = st.selectbox('Selecciona la variable para el eje Y', variables)

        col1,col2 = st.columns(2)

        col1.write(mvLogic.ScatterPlot(df_filtrado, variable_x, variable_y, inicio_año, fin_año, inicio_mes, fin_mes))

        col2.write(mvLogic.Dispersion(df_filtrado, variable_x, variable_y))

        
        
#################################################
#Regresiones
#################################################
        
        st.markdown("### Graficos de Regresion Lineal")
        
        variables.append("Año")
        variables.append("Longitud")

        variable_independiente = st.selectbox('Seleccione la variable independiente:', variables)

        dependientes = [var for var in df_Oriente.columns if var not in ["Mes", "Año", "Longitud", "Estacion", "Nombre de Estacion", "Latitud", "Región", "Provincias"]] # Todas las variables excepto "Año" y "Longitud" pueden ser dependientes
        variable_dependiente = st.selectbox('Seleccione la variable dependiente:', dependientes)

        REWORKED_df = df_Oriente.dropna(subset=[variable_independiente, variable_dependiente, 'Mes'])

        st.write(mvLogic.Regresion(REWORKED_df, variable_independiente, variable_dependiente))
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
import datetime
import streamlit as st


###################################
#COEFICIENTE DE RELACION
###################################

def CoeficienteRelacion (df):

    crtable = df.corr() 
    return crtable

###################################
#Nube de Puntos
###################################

def ScatterPlot(df, variable_x, variable_y, inicio_año, fin_año, inicio_mes, fin_mes):

    
    df_filtrado = df[(df['Año'] >= inicio_año) & (df['Año'] <= fin_año) & (df['Mes'] >= inicio_mes) & (df['Mes'] <= fin_mes)]

    plt.figure(figsize=(12, 8))
    plt.scatter(df_filtrado[variable_x], df_filtrado[variable_y], s=3)
    linea_media_x = plt.axvline(np.mean(df_filtrado[variable_x]), color="red", linestyle = "dashed")
    linea_media_y = plt.axhline(np.mean(df_filtrado[variable_y]), color="red", linestyle = "dashed")
    plt.title('Gráfico de dispersión')
    plt.xlabel(variable_x)
    plt.ylabel(variable_y)
    legend = plt.legend([linea_media_x, linea_media_y], [f'Media {variable_x}: {np.mean(df_filtrado[variable_x]):.2f}', f'Media {variable_y}: {np.mean(df_filtrado[variable_y]):.2f}'], loc='upper left')
    
    a = plt.gcf()

    return a
    

###################################
#Diagrama de Dispersion
###################################

def Dispersion(df, variable_x, variable_y):

    plt.figure(figsize=(11, 7))
    sns.kdeplot(data=df, x=variable_x, y=variable_y, fill=True)
    linea_media_x = plt.axvline(np.mean(df[variable_x]), color="red", linestyle = "dashed")
    linea_media_y = plt.axhline(np.mean(df[variable_y]), color="red", linestyle = "dashed")
    plt.title(f'Diagrama de densidad de {variable_x} vs {variable_y}')
    plt.xlabel(variable_x)
    plt.ylabel(variable_y)

    grafico = plt.gcf()

    return grafico


#################################################
#Regresiones
#################################################
    
def Regresion(df, variable_independiente, variable_dependiente):

    plt.figure(figsize=(12, 8))

    REWORKED_df = df.dropna(subset=[variable_independiente, variable_dependiente, 'Mes'])

    if variable_independiente in ['Año']:

            grouped_df = REWORKED_df.groupby(['Año', 'Mes'])[variable_dependiente].mean().reset_index()
            grouped_df['Fecha'] = grouped_df['Año'].astype(str) + '-' + grouped_df['Mes'].astype(str)
            grouped_df['Fecha'] = pd.to_datetime(grouped_df['Fecha'])
            grouped_df = grouped_df.sort_values('Fecha')
    
            X = grouped_df['Fecha'].map(datetime.datetime.toordinal).values.reshape(-1, 1)
            y = grouped_df[variable_dependiente]
            modelo = LinearRegression()
            modelo.fit(X, y)
            regression_line = modelo.predict(X)
    
            plt.plot(grouped_df['Fecha'], grouped_df[variable_dependiente], marker='o')
            plt.plot(grouped_df['Fecha'], regression_line, color='red')
            plt.title(f'Regresion de {variable_dependiente} a lo largo del tiempo')

    elif variable_independiente in ["Longitud"]:

            grouped_df = REWORKED_df.groupby(['Longitud'])[variable_dependiente].mean().reset_index()
            grouped_df = grouped_df.sort_values('Longitud')
            X = grouped_df['Longitud'].values.reshape(-1, 1)
            y = grouped_df[variable_dependiente]
            modelo = LinearRegression()
            modelo.fit(X, y)
            regression_line = modelo.predict(X)
    
            plt.plot(grouped_df['Longitud'], grouped_df[variable_dependiente], marker='o')
            plt.plot(grouped_df['Longitud'], regression_line, color='red') 
            plt.title(f'Regresion de {variable_dependiente} a lo largo de la Isla')

    else:
            X = REWORKED_df[variable_independiente].values.reshape(-1, 1)
            y = REWORKED_df[variable_dependiente]
            modelo = LinearRegression()
            modelo.fit(X, y)
            regression_line = modelo.predict(X)
    
            plt.scatter(REWORKED_df[variable_independiente], REWORKED_df[variable_dependiente], s=3)
            plt.plot(REWORKED_df[variable_independiente], regression_line, color='red') 
            plt.title(f'Regresión lineal de {variable_dependiente} vs {variable_independiente}')

    plt.xlabel(variable_independiente)
    plt.ylabel(variable_dependiente)

    a = plt.gcf()

    return a




def ScatLogic(df):

    inicio_año, fin_año = st.slider('Selecciona el rango de años', min_value=df['Año'].min(), max_value=df['Año'].max(), value=(df['Año'].min(), df['Año'].max()))
    inicio_mes, fin_mes = st.slider('Selecciona el rango de meses', min_value=df['Mes'].min(), max_value=df['Mes'].max(), value=(df['Mes'].min(), df['Mes'].max()))

    df_filtrado = df[(df['Año'] >= inicio_año) & (df['Año'] <= fin_año) & (df['Mes'] >= inicio_mes) & (df['Mes'] <= fin_mes)]

    variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa']
    variable_x = st.selectbox('Selecciona la variable para el eje X', variables)
    variable_y = st.selectbox('Selecciona la variable para el eje Y', variables)

    col1,col2 = st.columns(2)

    col1.write(ScatterPlot(df_filtrado, variable_x, variable_y, inicio_año, fin_año, inicio_mes, fin_mes))

    col2.write(Dispersion(df_filtrado, variable_x, variable_y))


def RegLogic(df):

    variables = ["Temperatura Media",'Temperatura Maxima Media', 'Temperatura Minima Media', 'Precipitaciones', 'Humedad Relativa',"Año","Longitud"]

    variable_independiente = st.selectbox('Seleccione la variable independiente:', variables)

    dependientes = [var for var in df.columns if var not in ["Mes", "Año", "Longitud", "Estacion", "Nombre de Estacion", "Latitud", "Región", "Provincias"]] # Todas las variables excepto "Año" y "Longitud" pueden ser dependientes
    variable_dependiente = st.selectbox('Seleccione la variable dependiente:', dependientes)

    REWORKED_df = df.dropna(subset=[variable_independiente, variable_dependiente, 'Mes'])

    st.write(Regresion(REWORKED_df, variable_independiente, variable_dependiente))
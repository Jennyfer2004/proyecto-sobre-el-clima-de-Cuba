import streamlit as st 
import matplotlib as plt
import folium as fl
import streamlit_folium as stf
import PIL as pl
import os
import io
import sklearn.cluster as sk
import sklearn.impute as im
import pandas as pd
import seaborn as sb

df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", "Humedad Relat", "Precipitaciones",
        "Nombres Estaciones", "Latitud", "Longitud", "Región", "Provincias"]]

df = df.rename(columns={"Temperatura max med": "Temperatura Maxima Media", "Temperatura min med": "Temperatura Minima Media", "Temperatura med": "Temperatura Media", "Humedad Relat": "Humedad Relativa",
        "Nombres Estaciones": "Nombre de Estacion"})

################################################
#COEFICIENTE DE CORRELACION
################################################


st.markdown("## Coeficiente de Correlacion entre las variables")
df_corr = df[["Temperatura Maxima Media", "Temperatura Minima Media", "Humedad Relativa", "Precipitaciones"]]
st.write(df_corr.corr()) 

st.write('''Como es posible observar, una Temperatura Maxima Media elevada esta directamente una Temperatura Minima Media tambien elevada. Esto nos indica que los lugares donde se registaron
         temperaturas altas, las temperaturas minimas fueron tambien mas altas si las comparamos con luagres donde se registraron menores temperaturas maximas. Asimismo, notamos que 
         las Precipitaciones estan mas relacionadas con el incremento de la humedad relativa que con otras variables. Resulta tambien intersante que, a pesar de que la relacion entre la Humedad 
         Relativa y las temperaturas maximas es pequena, estas variables son inversamente proporcionales.''')


################################################
#
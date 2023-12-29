import streamlit as st 
import pandas as pd
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA


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



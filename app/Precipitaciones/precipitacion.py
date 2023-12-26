import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import folium_static
from collections import OrderedDict
from folium.plugins import HeatMap
df = pd.read_csv("base_datos.csv")

df=df.dropna(subset=["Precipitaciones"]) 
df["fecha"] = df.apply(lambda row: str(row['Año']) + '-' + str(row['Mes']), axis=1)

df_mean =df.groupby(["Año","Mes"]).mean("Precipitaciones").reset_index()

fig = px.scatter(df_mean, x='Año', y='Precipitaciones', color='Mes', 
title='Precipitación por Mes y Año')
st.plotly_chart(fig)


#Paleta de colores
colores = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4", "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]

anos_seleccionados = st.multiselect('Selecciona los años que quieres visualizar:',options=df["Año"].unique(), default=[])  

df_filtrado = df_mean[df_mean["Año"].isin(anos_seleccionados) | (anos_seleccionados == [])]  

fig = px.line(df_filtrado, x="Mes", y="Precipitaciones", color="Año", color_discrete_sequence=colores, title='Precipitaciones por mes y año',labels={"Año": "Años"}, markers=True)
st.plotly_chart(fig)


time={1:"seco",2:"seco",3:"seco",4:"seco",5:"lluviosa",6:"lluviosa",7:"lluviosa",
8:"lluviosa",9:"lluviosa",10:"lluviosa",11:"seco",12:"seco"}
df_month=df
df_month["Tiempos"]=df["Mes"].replace(time)

df_month_sum=df.groupby(["Año","Tiempos"]).sum("Precipitaciones").reset_index()
# Crear el gráfico de dispersión interactivo
fig = px.line(df_month_sum, x="Año", y="Precipitaciones", color="Tiempos", 
                 title='Precipitación por Mes y Estacion',
                 color_discrete_sequence=[ 'Blue', 'Green'])
# Mostrar el gráfico en la aplicación de Streamlit
st.plotly_chart(fig)

selected_stations = st.multiselect("Selecciona las estaciones:", [''] + df["Nombres Estaciones"].unique().tolist())
if selected_stations:
    filtered_data = df.loc[ df["Nombres Estaciones"].isin(selected_stations)]
filtered_data = df[ df["Nombres Estaciones"]=="Cabo Cruz.Granma"]

fig = px.line(filtered_data, x='fecha', y='Precipitaciones', color='Nombres Estaciones', title='Comparación diferentes años y estaciones')
st.plotly_chart(fig)


df_promedio_años = df.groupby(["Año","Nombres Estaciones"])["Precipitaciones"].sum()

estacion_elegida = st.selectbox('Selecciona la estación a analizar', df["Nombres Estaciones"].unique())
if estacion_elegida:
    df_filtrado = df[df["Nombres Estaciones"] == estacion_elegida]
df_filtrado=df[df["Nombres Estaciones"] == "Cabo Cruz.Granma"]
df_promedio_años_estacion = df_filtrado.groupby(df_filtrado[("Año")])["Precipitaciones"].sum().reset_index()

fig = px.bar(df_promedio_años_estacion, x="Año", y="Precipitaciones", color="Año",color_discrete_sequence=colores,
             labels={"Húmedad Relat": "Promedio de Humedad Relativa", "Año": "Año"},
             title=f"Promedios por año para la estación {estacion_elegida}")

st.plotly_chart(fig)




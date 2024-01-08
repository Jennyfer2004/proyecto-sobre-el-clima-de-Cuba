# import various libraries
import streamlit as st 
import pandas as pd 
import plotly.express as px
from collections import OrderedDict
import matplotlib.pyplot as plt
import PIL as pl
import altair as alt
import plotly.graph_objs as go
import plotly.express as px
df = pd.read_csv("../app/data/base_datos.csv")
##################################################################################################
#Analisis
##################################################################################################
st.write("## Interactúe con los gráficos, y haga sus propios análisis")
df2=df
selected_default = df["Provincias"].unique()[:3].tolist()
df =df.groupby(["Año","Mes","Provincias"]).mean("Precipitaciones").reset_index()
selected = st.multiselect("Selecciona las provincias:", df["Provincias"].unique().tolist(), default=selected_default)
year = st.selectbox("Selecciona el año ",df["Año"].unique().tolist())
df['Media_Mensual'] = df.groupby('Mes')['Precipitaciones'].transform('mean')

filtered = df[(df["Año"] == year) & (df['Provincias'].isin(selected))]
filtered_df  = filtered.groupby(["Mes"]).mean().reset_index()

bars = alt.Chart(filtered_df).mark_bar().encode(
    x='Mes',
    y='Precipitaciones',
    color=alt.value('blue')
)

line = alt.Chart(filtered_df).mark_line(color='red').encode(
    x='Mes',
    y='Media_Mensual'
)

chart = bars + line
st.write("### Gráfico de precipitaciones promedio de las provincias seleccionadas")
st.altair_chart(chart, use_container_width=True)
#################################################################

media_mensual_total = df.groupby('Mes')['Precipitaciones'].mean()
selected1 = filtered.groupby('Mes')['Precipitaciones'].mean()

fig = go.Figure()
fig.add_trace(go.Bar(x=selected1.index, y=selected1, name='2022'))
fig.add_trace(go.Scatter(x=media_mensual_total.index, y=media_mensual_total, mode='lines', name='Media Mensual',line=dict(color='red')))

fig.update_layout(title='Precipitaciones Mensuales en el año seleccionado y la Media Mensual', xaxis_title='Meses', yaxis_title='Precipitaciones')

st.plotly_chart(fig)


filtered=filtered.groupby(["Provincias"]).mean().reset_index()
df3=df2[df2["Provincias"].isin(selected)]
media_mensual_total = df3.groupby("Provincias")['Precipitaciones'].mean()
selected2 = filtered.groupby("Provincias")['Precipitaciones'].mean()

media_mensual_total = df2['Precipitaciones'].mean()
media_mensual_por_provincia = df3.groupby('Provincias')['Precipitaciones'].mean().reset_index()

# Crear el gráfico interactivo con Altair
bar_chart = alt.Chart(filtered).mark_bar().encode(
    x='Provincias',
    y='Precipitaciones'
).properties(
    width=alt.Step(80)
)

line_chart = alt.Chart(media_mensual_por_provincia).mark_line(color='green').encode(
    x='Provincias',
    y=alt.Y('Precipitaciones', title='Media Mensual'),
)

st.write("### Gráfico de precipitaciones por provincia")
st.altair_chart(bar_chart + line_chart, use_container_width=True)



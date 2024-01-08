import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import io
import PIL as pl

st.markdown("# Podcast Interactivo")

with open(f'./images/mosquito.png', 'rb') as f:
    datos_imagen = f.read()
imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))
st.image(imagen)

df = pd.read_csv("./data/base_datos.csv")

def actualizar_grafico(segundo: float) -> None:
    if segundo <= 28:
        pass
    elif segundo > 28 and segundo < 35:
        pass
    else:
        st.empty()

st.title('Visualización de gráfico basado en el tiempo de audio')


##################
# Med Temperatures
##################
year_monthly = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value = 2022, key = "year_monthly")

def filter_data(dataframe: pd.DataFrame, year: int, indicator: str) -> pd.DataFrame:
    data = dataframe.loc[df["Año"] == year]
    data = data.groupby(["Provincias", "Año"])[indicator].mean().reset_index()
    return data
    
if year_monthly:
    data = filter_data(df, year_monthly, "Temperatura med")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = data["Provincias"], y = data["Temperatura med"]))
    st.plotly_chart(fig)

##################
# Rain
##################

    
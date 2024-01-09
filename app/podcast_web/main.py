import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import io
import PIL as pl
from typing import List
import time
from pydub import AudioSegment

st.markdown("# Podcast Interactivo")

def upload_image(name: str) -> pl.Image:
    with open(f'./images/{name}', 'rb') as f:
        datos_imagen = f.read()
    imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))
    return imagen

st.image(upload_image("mosquito.png"))

df = pd.read_csv("./data/base_datos.csv")
df = df.dropna()

def update_graphics(segundo: float) -> None:
    if segundo <= 28:
        pass
    elif segundo > 28 and segundo < 35:
        pass
    else:
        st.empty()

st.title('Visualización de gráfico basado en el tiempo de audio')


with open("./podcast_web/audio.mp3", "rb") as audio_file:
    audio_bytes = audio_file.read()

audio = st.audio(audio_bytes, format='audio/mp3', start_time = 0)

##################
# Med Temperatures
##################
year_monthly = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value = 2022, key = "year_monthly")

def filter_data_temperature(dataframe: pd.DataFrame, year: int, indicator: str) -> pd.DataFrame:
    data = dataframe.loc[df["Año"] == year]
    data = data.groupby(["Provincias", "Año"])[indicator].mean().reset_index()
    return data
    
if year_monthly:
    data = filter_data_temperature(df, year_monthly, "Temperatura med")
    
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x = data["Provincias"], y = data["Temperatura med"]))
    fig_temp.update_layout(title = f"Gráfico de línea de la Temperatura por provincias en el año de {year_monthly}",
                             xaxis_title="Provincias",
     
                            yaxis_title="Valor de Temperatura")
    # 
    st.plotly_chart(fig_temp)

##################
# Rain
##################

year_rain = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value = 2022, key = "year_rain")

months = ['Septiembre', 'Octubre', 'Noviembre']

month_rain = st.select_slider('Selecciona un mes' , options = months, value = "Septiembre", key = "month_rain")

def filter_data_rain(dataframe: pd.DataFrame, year: int, indicator: str, month: str) -> pd.DataFrame:
    data = dataframe.loc[(df["Año"] == year) & (df["Mes"].isin([9, 10, 11]))]
    data = data.groupby(["Provincias", "Mes"])[indicator].mean().reset_index()
    data['Mes'] = data['Mes'].replace({9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre'})
    return data.loc[data["Mes"] == month]

if year_rain:
    data = filter_data_rain(df, year_rain, "Humedad Relat", month_rain)
    
    fig_rain = go.Figure()
    fig_rain.add_trace(go.Bar(x = data["Provincias"], y = data["Humedad Relat"], showlegend = False))
    fig_rain.add_trace(go.Scatter(x = data["Provincias"], y = data["Humedad Relat"], showlegend = False))    
    fig_rain.update_layout(title = f"Gráfico de barras de Humedad Relativa por provincias en el mes de {month_rain}",
                             xaxis_title="Provincias",
                             yaxis_title="Porcentaje de Humedad")
    # 
    st.plotly_chart(fig_rain)

#  
st.image(upload_image("dengue.jpg"))


# 
st.image(upload_image("santiago.png"))
st.title("Santiango de Cuba - 1992 :chart_with_upwards_trend: 🚗")

# 
st.image(upload_image("la_habana.png"))
st.title("La Habana - 2000 🦟 :x:")

# 
st.image(upload_image("ninos_santiago.jpg"))
st.title("En 2006, el 10,3\% de los casos que ocurrieron en Santiango de Cuba fueron niños :boy: :girl:")

# 
st.image(upload_image("dengue_cuba.png"))


##########################
# RH and precipitation
##########################
yaer_rh_pre = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value = 2022, key = "yaer_rh_pre")

def filter_data_rh_prec(dataframe: pd.DataFrame, year: int, indicator: str) -> pd.DataFrame:
    data = dataframe.loc[df["Año"] == year]
    data = data.groupby(["Provincias"])[indicator].mean().reset_index()
    return data

if yaer_rh_pre:
    col1, col2, = st.columns(2)
    data = filter_data_rh_prec(df, yaer_rh_pre, "Humedad Relat")
    data = data.sort_values(by = "Humedad Relat", ascending = True)
    
    fig_rh = go.Figure()
    fig_rh.add_trace(go.Bar(y=data["Provincias"], x=data["Humedad Relat"], orientation='h', showlegend=False))
    fig_rh.update_layout(title = f"Gráfico de barras de Humedad Relativa por provincias en el año de {yaer_rh_pre}",
                             yaxis_title="Provincias",
                             xaxis_title="Porcentaje de Humedad")
    # 
    col1.plotly_chart(fig_rh)
    fig_prec = go.Figure()
    data = filter_data_rh_prec(df, yaer_rh_pre, "Precipitaciones")
    data = data.sort_values(by = "Precipitaciones", ascending = False)
    fig_prec.add_trace(go.Bar(x = data["Provincias"], y = data["Precipitaciones"], showlegend=False))
    fig_prec.update_layout(title = f"Gráfico de barras de Precipitaciones por provincias en el año de {yaer_rh_pre}",
                             xaxis_title="Provincias",
                             yaxis_title="Valor de Precipitaciones")
    # 
    col2.plotly_chart(fig_prec)
    
    
    data = filter_data_temperature(df, yaer_rh_pre, "Temperatura med")
    data = data.sort_values(by = "Temperatura med", ascending = False)
    
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(x = data["Provincias"], y = data["Temperatura med"]))
    fig_temp.update_layout(title = f"Gráfico de línea de la Temperatura por provincias en el año de {yaer_rh_pre}",
                             xaxis_title="Provincias",
                            yaxis_title="Valor de Temperatura")
    #
    col1.plotly_chart(fig_temp)
    
############################
# RH and precipitation months
############################
yaer_rh_pre_months = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value = 2022, key = "yaer_rh_pre_months")
months = ['Septiembre', 'Octubre', 'Noviembre']

def filter_data_rh_prec_months(dataframe: pd.DataFrame, months: List[str], year: int, indicator: str) -> pd.DataFrame:
    data = dataframe.loc[(df["Año"] == year)  & (df["Mes"].isin(months))]
    data = data.groupby(["Provincias", "Mes"])[indicator].mean().reset_index()
    return data

if yaer_rh_pre_months:
    col1, col2, = st.columns(2)
    # HR
    data_rh_months = filter_data_rh_prec_months(df, [9 ,10, 11], yaer_rh_pre_months, "Humedad Relat")
    data_rh_months['Mes'] = data_rh_months['Mes'].replace({9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre'})
    
    fig_rh_months = go.Figure()
    color_mapping = {
        'Septiembre': 'blue', 
        'Octubre': 'green',    
        'Noviembre': 'orange'  
    }
    fig_rh_months.add_trace(go.Scatter(
    x=data_rh_months["Provincias"],
    y=data_rh_months["Humedad Relat"],
    text=data_rh_months['Mes'],
    mode='markers',
    marker=dict(
        color=[color_mapping[month] for month in data_rh_months['Mes']], 
        size=8, 
        line=dict(
            width=2, 
        )
    ),
    name="Humedad Relativa"
    ))
    fig_rh_months.update_layout(title = f"Gráfico de Puntos de la Humedad Relativa en el año {yaer_rh_pre_months} de Septiembre-Noviembre",
                                xaxis_title="Provincias",
                                yaxis_title="Porcentaje de Humedad Relativa")
    col1.plotly_chart(fig_rh_months)
    
    # Prec
    data_prec_months = filter_data_rh_prec_months(df, [9 ,10, 11], yaer_rh_pre_months, "Precipitaciones")
    data_prec_months['Mes'] = data_prec_months['Mes'].replace({9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre'})
    
    fig_prec_months = go.Figure()
    color_mapping = {
        'Septiembre': 'blue', 
        'Octubre': 'green',    
        'Noviembre': 'orange'  
    }
    fig_prec_months.add_trace(go.Scatter(
    x=data_prec_months["Provincias"],
    y=data_prec_months["Precipitaciones"],
    text=data_prec_months['Mes'],
    mode='markers',
    marker=dict(
        color=[color_mapping[month] for month in data_prec_months['Mes']], 
        size=8, 
        line=dict(
            width=2, 
        )
    ),
    name="Humedad Relativa"
    ))
    fig_prec_months.update_layout(title = f"Gráfico de Puntos de las Precipitaciones en el año {yaer_rh_pre_months} de Septiembre-Noviembre",
                                xaxis_title="Provincias",
                                yaxis_title="Valor de Precipitaciones")
    col2.plotly_chart(fig_prec_months)

#####################
# Med Temperatures 2
#####################
year_monthly_2 = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value = 2022, key = "year_monthly_2")

def filter_data_temperature(dataframe: pd.DataFrame, year: int, indicator: str) -> pd.DataFrame:
    data = dataframe.loc[df["Año"] == year]
    data = data.groupby(["Provincias", "Año"])[indicator].mean().reset_index()
    return data
    
if year_monthly_2:
    data = filter_data_temperature(df, year_monthly_2, "Temperatura med")
    data = data.sort_values(by = "Temperatura med", ascending = False)
    
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Bar(x = data["Provincias"], y = data["Temperatura med"], showlegend = False))
    fig_temp.add_trace(go.Scatter(x = data["Provincias"], y = data["Temperatura med"], showlegend = False))
    fig_temp.update_layout(title = f"Gráfico de línea de la Temperatura por provincias en el año de {year_monthly_2}",
                             xaxis_title="Provincias",
     
                            yaxis_title="Valor de Temperatura")
    # 
    st.plotly_chart(fig_temp)

# 
st.image(upload_image("condiciones_climaticas.jpg"))

#################
# Anual
################
col1, col2, = st.columns(2)
def filter_data_country(dataframe: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
    data = dataframe.groupby(["Año"])[indicators].mean().reset_index()
    return data

ind_temp = ["Temperatura min med", "Temperatura med", "Temperatura max med"]
country_data_temp = filter_data_country(df, ind_temp)

fig_temp_ind = go.Figure()
for ind in ind_temp:
    fig_temp_ind.add_trace(go.Scatter(x=country_data_temp["Año"], 
                                      y=country_data_temp[ind], mode="markers+lines", name=ind))
    
fig_temp_ind.update_layout(title = f"Gráfico de línea de la Temperatura anual",
                             xaxis_title="Provincias",
                            yaxis_title="Valor de Temperatura")
# 
col1.plotly_chart(fig_temp_ind)

country_data_prec = filter_data_country(df, "Precipitaciones")
fig_prec_ind = go.Figure()
fig_prec_ind.add_trace(go.Scatter(x = country_data_prec["Año"], y = country_data_prec["Precipitaciones"], mode="markers+lines",))
fig_prec_ind.update_layout(title = f"Gráfico de línea de la Precipitaciones Anual",
                             xaxis_title="Provincias",
                            yaxis_title="Valor de Precipitaciones")
# 
col2.plotly_chart(fig_prec_ind)


country_data_hr = filter_data_country(df, "Humedad Relat")
fig_prec_hr = go.Figure()
fig_prec_hr.add_trace(go.Scatter(x = country_data_hr["Año"], y = country_data_hr["Humedad Relat"], mode="markers+lines",))
fig_prec_hr.update_layout(title = f"Gráfico de línea de la Humedad Relativa Anual",
                             xaxis_title="Provincias",
                            yaxis_title="Procentaje de Humedad Relativa")
# 
col1.plotly_chart(fig_prec_hr)


##########


# 
st.image(upload_image("prevencion.jpg"))

st.image(upload_image("signos.jpg"))
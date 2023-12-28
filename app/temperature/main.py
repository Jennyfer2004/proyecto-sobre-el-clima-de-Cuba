import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from typing import List, Dict

st.title("Comportamiento de las Temperaturas en Cuba 1990-2022")

df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", 
        "Nombres Estaciones", "Latitud", "Longitud", "Región", "Provincias"]]

##########################################
# Comparación de la temperatura anual
###########################################
st.write("Comparación de la temperatura anual")

# Station Multiselect 
selected_state_annual = st.multiselect(label = 'Selecciona una provincia', options = df["Provincias"].unique(),
                                placeholder ="Provincias", key = "annual")
disabled_year = not bool(selected_state_annual)

# Year slider
year_range = st.slider('Selecciona un rango de años', min_value = 1990, max_value = 2022, value = (1990, 2022), disabled = disabled_year)

start_year, end_year = year_range

# Checkboxes
selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled_year, value = not disabled_year)
        if option:
            selected_values.append(value)

def filter_data_by_year(database: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    return database[(database["Año"] >= start_year) & (database["Año"] <= end_year)]

def filter_data_by_state(database: pd.DataFrame, states: List[str]) -> pd.DataFrame:
    return database[database["Provincias"].isin(states)]

def separate_by_states(database: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    states = database.Provincias.unique()
    return {state : database[database["Provincias"] == state] for state in states}

def average_temperature(databases: Dict[str, pd.DataFrame], indicators: List[str]) -> Dict[str, pd.DataFrame]:
    return {name: database.groupby("Año")[indicators].mean().reset_index() for name, database in databases.items()}

def filter_data_annual(database: pd.DataFrame, start_year: int, 
                       end_year: int, states: List[str], indicators: List[str]) -> Dict[str, pd.DataFrame]:
    years = filter_data_by_year(database, start_year, end_year)
    states = filter_data_by_state(years, states)
    separate = separate_by_states(states)
    temperatures = average_temperature(separate, indicators)
    return temperatures

if selected_state_annual and selected_values:
    df_filtered = filter_data_annual(df, start_year, end_year, selected_state_annual, selected_values)
    fig_annual = go.Figure()
    
    for name, data in df_filtered.items():
        for indicator in selected_values:
            data['Name'] = name
            fig_annual.add_trace(go.Scatter(x = data['Año'], y = data[indicator], mode='lines',
                                            name = f"{indicator} de {name}", text = data['Name'],
                                            hoverinfo= "text+x+y"))
        
    st.plotly_chart(fig_annual)

##########################################
# Comparación de la temperatura mensual
###########################################
st.write("Comparación de la temperatura mensual")

selected_state_monthly = st.multiselect(label = 'Selecciona una provincia', options = df["Provincias"].unique(),
                                placeholder ="Provincias", key = "monthly")
disabled_monthly = not bool(selected_state_monthly)

# Month slider
months = { "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}

year_monthly = st.slider('Selecciona un rango de años', min_value = 1990, max_value = 2022,
                         value = (1990, 2022), disabled = disabled_monthly, key = "year_monthly")
start_year, end_year = year_monthly

selected_month_name = st.select_slider('Selecciona rango de meses', options= list(months.keys()),
                      value=("Enero", "Diciembre"), disabled = disabled_monthly)
start_month, end_month = selected_month_name

selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled_monthly, value = not disabled_monthly, key = f"check monthly {i}")
        if option:
            selected_values.append(value)

def separate_by_states_and_months(database: pd.DataFrame, start_month: str, end_month: str):
    states = database.Provincias.unique()
    return {state : database[(database["Provincias"] == state) & (database["Mes"] >= months[start_month])
                             & (database["Mes"] <= months[end_month])] for state in states}

def average_temperature_also_by_month(databases: Dict[str, pd.DataFrame], indicators: List[str]) -> Dict[str, pd.DataFrame]:
    return {name: database.groupby(["Año", "Mes"])[indicators].mean().reset_index() for name, database in databases.items()}

def filter_data_monthly(database: pd.DataFrame, start_year: int, 
                       end_year: int, states: List[str], start_month: str, end_month: str,
                       indicators: List[str]) -> Dict[str, pd.DataFrame]:
    years = filter_data_by_year(database, start_year, end_year)
    states = filter_data_by_state(years, states)
    separate = separate_by_states_and_months(states, start_month, end_month)
    temperatures = average_temperature_also_by_month(separate, indicators)
    return temperatures

if selected_state_monthly:
    filtered_monthly = filter_data_monthly(df, start_year, end_year,
                                           selected_state_monthly, start_month, end_month, selected_values)
    fig_monthly = go.Figure()
    for name, data in filtered_monthly.items():
        for indicator in selected_values:
            data['Mes'] = data['Mes'].replace({1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                                   5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 
                                   9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'})
            data['Popup'] = data['Mes'].astype(str)  + '-' + data['Año'].astype(str) + '-' + name 
            
            fig_monthly.add_trace(go.Scatter(x = data['Año'], y = data[indicator],
                                             mode='markers', name = f"{indicator} de {name}",
                                             text = data['Popup'], hoverinfo = 'text+y',
                                             marker=dict(size=8)))

            # Crear un gráfico adicional con mode='lines' para unificar los puntos según el mes
            unique_meses = data['Mes'].unique()
            for mes in unique_meses:
                mes_data = data[data['Mes'] == mes]
                fig_monthly.add_trace(go.Scatter(
                x=mes_data['Año'],
                y=mes_data[indicator],
                mode='lines',
                showlegend=True,
                name= f"{indicator} {mes}"
                ))
    
    st.plotly_chart(fig_monthly)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict

st.title("Comportamiento de las Temperaturas en Cuba 1990-2022")

df = pd.read_csv("../data/base_datos.csv")

colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", 
          "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4",
          "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]

##########################################
# Comparación de la temperatura anual
###########################################
st.write("Comparación de la temperatura anual")

# Station Multiselect 
selected_state = st.multiselect(label = 'Selecciona una provincia', options = df["Provincias"].unique(),
                                  placeholder ="Provincias")
disabled = not bool(selected_state)

# Year slider
year_range = st.slider('Selecciona un rango de años', min_value = 1990, max_value = 2022, value = (1990, 2022), disabled = disabled)

start_year, end_year = year_range

# Checkboxes
selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled, value = not disabled)
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
    return {name: database.groupby('Año')[indicators].mean().reset_index() for name, database in databases.items()}

def filter_data(database: pd.DataFrame, start_year: int, end_year: int, states: List[str], indicators: List[str]):
    years = filter_data_by_year(database, start_year, end_year)
    states = filter_data_by_state(years, states)
    separate = separate_by_states(states)
    temperatures = average_temperature(separate, indicators)
    return temperatures

if selected_state and selected_values:
    df_filtered = filter_data(df, start_year, end_year, selected_state, selected_values)
    fig = go.Figure()
    
    for name, data in df_filtered.items():
        for indicator in selected_values:
            fig.add_trace(go.Scatter(x = data['Año'], y = data[indicator], mode='lines', name = f"{indicator} de {name}"))
        
    st.plotly_chart(fig)

##########################################
# Comparación de la temperatura mensual
###########################################


# Month slider
#months ={ "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
#        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}

#selected_month_name = st.select_slider('Selecciona rango de meses', options= list(months.keys()),
#                      value=("Enero", "Diciembre"), disabled = disabled)
#start_month, end_month = selected_month_name
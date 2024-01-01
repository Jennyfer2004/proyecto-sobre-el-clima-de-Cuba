import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import numpy as np

st.title("Temperatura")

df = pd.read_csv("./data/base_datos.csv")
df = df.loc[:, ["Año", "Mes", "Temperatura max med", "Temperatura min med", "Temperatura med", 
        "Nombres Estaciones", "Latitud", "Longitud", "Región", "Provincias"]]

##########################################
# Comparación de la temperatura anual
###########################################
st.write("Comparación de la temperatura anual por provincias")

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

def filter_data_by_state(database: pd.DataFrame, states: List[str], variable: str = "Provincias") -> pd.DataFrame:
    return database[database[variable].isin(states)]

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
    
    table = pd.concat([j for i, j in df_filtered.items()])
    
    provinces = []
    for i in selected_state_annual:
        for _ in range(start_year, end_year + 1):
            provinces.append(i)
    
    table["Provincias"] = provinces
    
    fig_annual = go.Figure()
    for name, data in df_filtered.items():
        for indicator in selected_values:
            data['Name'] = name
            fig_annual.add_trace(go.Scatter(x = data['Año'], y = data[indicator], mode='lines',
                                            name = f"{indicator} de {name}", text = data['Name'],
                                            hoverinfo= "text+x+y"))
        
    fig_annual.update_layout(title="Gráfico de línea de las temperaturas de cada año por provincias",
                             xaxis_title="Años",
                             yaxis_title="Valor de Temperatura")
   
    st.plotly_chart(fig_annual)
    st.write(table.reset_index(drop= True))

##########################################
# Comparación de la temperatura mensual
###########################################
st.write("Comparación de la temperatura mensual por provincias")

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
        option = st.checkbox(label = label, disabled = disabled_monthly, 
                             value = not disabled_monthly, key = f"check monthly {i}")
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
    
    table = filtered_monthly
    for i, d in table.items(): 
        d['Provincias'] = np.nan
        d['Provincias'] = d['Provincias'].fillna(i)
    
    table = pd.concat([j for i, j in table.items()])
    
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
    
    fig_monthly.update_layout(title="Scatterplot de temperatura de los mes de cada año por provincias",
                             xaxis_title="Años",
                             yaxis_title="Valor de Temperatura") 
    
    st.plotly_chart(fig_monthly)
    st.write(table)

##################################################
# Comparación de la temperatura anual por region
##################################################
st.write("Comparación de la temperatura anual por región")

selected_region_annual = st.multiselect(label = 'Selecciona una región', options = df["Región"].unique(),
                                placeholder ="Región", key = "annual_region")

disabled_region_year = not bool(selected_region_annual)

year_range_region = st.slider('Selecciona un rango de años', min_value = 1990, max_value = 2022, disabled = disabled_region_year)

selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled_region_year, 
                             value = not disabled_region_year, key = f"region {i}")
        if option:
            selected_values.append(value)

def filter_data_by_one_year(database: pd.DataFrame, year: int) -> pd.DataFrame:
    return database[database["Año"] == year]

def separate_by_region(database: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    states = database.Región.unique()
    return {state : database[database["Región"] == state] for state in states}

def filter_data_by_region(database: pd.DataFrame, year: int, indicators: List[str]) -> Dict[str, pd.DataFrame]:
    year = filter_data_by_one_year(database, year)
    states = filter_data_by_state(year, selected_region_annual, "Región")
    separate = separate_by_region(states)
    temperature = average_temperature(separate, indicators)
    return temperature

if selected_region_annual:
    filtered_region_data = filter_data_by_region(df, year_range_region, selected_values)

    table = pd.concat([j for i, j in filtered_region_data.items()])
    table["Región"] = selected_region_annual
    
    fig_region = go.Figure()
    for indicator in selected_values:
        for region, data in filtered_region_data.items():
            fig_region.add_trace(go.Bar(x=[region], y=data[indicator], name=f"{indicator} del {region}"))
           
        fig_region.add_trace(go.Scatter(x=table['Región'], y=table[indicator], mode='lines+markers', showlegend = False))
    
                  
    fig_region.update_layout(title="Gráfico de barras de temperatura por región",
                             xaxis_title="Región",
                             yaxis_title="Valor de Temperatura",
                             barmode='overlay')  
                             
    st.plotly_chart(fig_region)
    st.write(table.reset_index(drop= True))

##################################################
# Comparación de la temperatura mensual por region
##################################################
st.write("Comparación de la temperatura mensual por región")

selected_region_monthly = st.multiselect(label = 'Selecciona una región', options = df["Región"].unique(),
                                placeholder ="Región", key = "monthly_region")

disabled_region_monthly = not bool(selected_region_monthly)

monthly_year = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, disabled = disabled_region_monthly)

selected_month = st.select_slider('Selecciona un mes', options= list(months.keys()),
                      value=("Enero", "Diciembre"), disabled = disabled_region_monthly)

start_month, end_month = selected_month

selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled_region_monthly, 
                             value = not disabled_region_monthly, key = f"region_{i}")
        if option:
            selected_values.append(value)
      
def separate_by_region_and_months(database: pd.DataFrame, start_month: str, end_month: str):
    states = database.Región.unique()
    return {state : database[(database["Región"] == state) & (database["Mes"] >= months[start_month])
                             & (database["Mes"] <= months[end_month])] for state in states}      
          
def filter_data_monthly_by_region(database: pd.DataFrame,year: int ,
                                states: List[str], start_month: str, end_month: str,
                                indicators: List[str]) -> Dict[str, pd.DataFrame]:
    years = filter_data_by_one_year(database, year)
    states = filter_data_by_state(years, states, "Región")
    separate = separate_by_region_and_months(states, start_month, end_month)
    temperatures = average_temperature_also_by_month(separate, indicators)
    return temperatures

if selected_region_monthly:
    filtered_monthly_by_region = filter_data_monthly_by_region(df, monthly_year,
                            selected_region_monthly, start_month, end_month, selected_values)
    
    fig_monthly_region = go.Figure()
    for name, data in filtered_monthly_by_region.items():
        for indicator in selected_values:
            data['Mes'] = data['Mes'].replace({1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                                   5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 
                                   9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'})
            
            fig_monthly_region.add_trace(go.Bar(x=data['Mes'], y=data[indicator], 
                                                name=f"{indicator} de {name}", hoverinfo = f'y'))
            
            
            if len(selected_region_monthly) == 1 and len(selected_values) < 3:
                data['Popup'] = data['Mes'].astype(str)  + '-' + data['Año'].astype(str) + '-' + name 
            
                fig_monthly_region.add_trace(go.Scatter(x = data['Mes'], y = data[indicator], name = f"{indicator} de {name}",
                                                    text = data["Popup"], hoverinfo = 'text+y', 
                                                    marker=dict(size=8)))
            
    fig_monthly_region.update_layout(title="Gráfico de barras de temperatura por mes por región",
                             xaxis_title="Mes",
                             yaxis_title="Valor de Temperatura")
    
    st.plotly_chart(fig_monthly_region)
    
    table = filtered_monthly_by_region
    for i, d in table.items(): 
        d['Región'] = np.nan
        d['Región'] = d['Región'].fillna(i)
    
    table = pd.concat([j for i, j in table.items()])
    st.write(table)
    

#############################################################
# Comparación de la temperatura anual en las zonas turísticas
#############################################################
st.write("Comparación de la temperatura anual en las zona turísiticas")

zones = ['Cabo de San Antonio.Pinar del Río', 'Varadero.Matanzas', 'Playa Girón.Matanzas',
         'Cayo Coco.Ciego de Ávila','Cabo Lucrecia.Holguín', 'Cabo Cruz.Granma', 'Punta de Maisí.Guantánamo']

data_zone = df[df["Nombres Estaciones"].isin(zones)].copy()
data_zone["Zona"] = data_zone["Nombres Estaciones"].str.split(".").str[0]
data_zone["Zona"] = data_zone["Zona"].replace("Cabo Lucrecia", "Guardalavaca")
data_zone["Zona"] = data_zone["Zona"].replace("Playa Girón", "Ciénaga de Zapata")

data_zone = data_zone.loc[:, ["Año", "Mes","Temperatura max med","Temperatura med",
                    "Temperatura min med", "Zona"]]

selected_zone = st.multiselect(label = 'Selecciona una zona', options = data_zone["Zona"].unique(),
                                placeholder ="Zona", key = "annual_zone")

disabled_zone = not bool(selected_zone)

zone_year = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, disabled = disabled_zone, key= "year_zone")

selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled_zone, 
                             value = not disabled_zone, key = f"zone {i}")
        if option:
            selected_values.append(value)

def filter_data_by_zone(database: pd.DataFrame, year: int, indicators: List[str], zones: List[str]):
    years = filter_data_by_one_year(database, year)
    group = years.groupby(["Año", "Zona"])[indicators].mean().reset_index()
    separate = group[group["Zona"].isin(zones)]
    return separate

if selected_zone:
    filter_zones = filter_data_by_zone(data_zone, zone_year, selected_values, selected_zone)
    
    fig_zone = go.Figure()
    for indicator in selected_values:
        fig_zone.add_trace(go.Bar(x = filter_zones['Zona'], y=filter_zones[indicator],
                                  name = indicator, hoverinfo = 'x+y'))
        
        if len(selected_zone) > 1:
            fig_zone.add_trace(go.Scatter(x = filter_zones['Zona'], y =filter_zones[indicator],
                                   showlegend=False, hoverinfo = 'x+y'))
    
    fig_zone.update_layout(title="Gráfico de barras de temperatura por mes por zona turistica",
                             xaxis_title="Zona",
                             yaxis_title="Valor de Temperatura",
                             barmode='overlay')
    
    st.plotly_chart(fig_zone)
    st.write(filter_zones.reset_index(drop= True))

###############################################################
# Comparación de la temperatura mensual en las zonas turísticas
###############################################################
st.write("Comparación de la temperatura mensual en las zona turísiticas")

selected_zone_monthly = st.multiselect(label = 'Selecciona una zona', options = data_zone["Zona"].unique(),
                                placeholder ="Zona", key = "annual_zone_monthly")

disabled_zone_monthly = not bool(selected_zone_monthly)

monthly_year_zone = st.slider('Selecciona un año', min_value = 1990, max_value = 2022, value= (1990, 2022),
                              disabled = disabled_zone_monthly, key = "mon_zone")

start_year, end_year = monthly_year_zone

selected_month_zone = st.select_slider('Selecciona un rango de meses', options= list(months.keys()),
                      value=("Enero", "Diciembre"), disabled = disabled_zone_monthly)

start_month, end_month = selected_month_zone


selected_values = []
options = {"Temperatura máxima media" : "Temperatura max med", 
           "Temperatura media" : "Temperatura med",
           "Temperatura mínima media" : "Temperatura min med"}

cols = st.columns(len(options))  

for i, (label, value) in enumerate(options.items()):
    with cols[i]:
        option = st.checkbox(label = label, disabled = disabled_zone_monthly, 
                             value = not disabled_zone_monthly, key = f"zone_{i}")
        if option:
            selected_values.append(value) 
   
months = { "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
        "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
 
def filter_zones_monthly(database: pd.DataFrame, start_year: int, 
                       end_year: int, indicators: List[str], zones: List[str],
                       start_month: int, end_month: int):
    years = filter_data_by_year(database, start_year, end_year)
    fil = years[years["Zona"].isin(zones)]
    month = fil[(fil["Mes"] >= months[start_month]) & (fil["Mes"] <= months[end_month])]
    group = month.groupby(["Zona","Año", "Mes"])[indicators].mean().reset_index()
    return group
            
if selected_zone_monthly:
    filter_monthly_zones = filter_zones_monthly(data_zone, start_year, end_year, selected_values, 
                                                selected_zone_monthly, start_month, end_month)
    
    filter_monthly_zones['Mes'] = filter_monthly_zones['Mes'].replace({1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril',
                                   5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 
                                   9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'})
     
    colores_zonas = px.colors.qualitative.Set1  # Usamos una paleta de colores predefinida de Plotly Express

    fig_zone_monthly = go.Figure()

    color_por_zona = dict(zip(selected_zone_monthly, colores_zonas))
    added_to_legend = {} 
    for indicator in selected_values:
        for zona in selected_zone_monthly:
            zona_filtrada = filter_monthly_zones[filter_monthly_zones['Zona'] == zona]
            fig_zone_monthly.add_trace(go.Scatter(
            x=zona_filtrada['Año'],
            y=zona_filtrada[indicator],
            mode="markers",
            showlegend = False,
            hoverinfo='text+x+y', 
            marker=dict(size=8),  
            text=zona_filtrada['Mes'] + " - " + zona  
        ))

    fig_zone_monthly.update_layout(title="Comparación de la temperatura mensual en las zonas turísticas",
                               xaxis_title="Año",
                               yaxis_title="Temperatura")

    st.plotly_chart(fig_zone_monthly)
    st.write(filter_monthly_zones.reset_index(drop= True))
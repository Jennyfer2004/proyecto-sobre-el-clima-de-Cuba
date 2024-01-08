# import various libraries
import streamlit as st 
import pandas as pd 
import plotly.express as px
import folium
from streamlit_folium import folium_static
from collections import OrderedDict
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import PIL as pl
import os
import io

current_path = os.getcwd()
path= os.path.dirname(current_path)
path = path.replace("\\", "/") 

st.markdown("# Precipitaciones")

col1, col2 = st.columns(2)
with open(f'{path}' + '/app/images/CubaRain.jpg', 'rb') as f:
        datos_imagen = f.read()
imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))

col2.image(imagen)
col1.write("La precipitación es un factor fundamental en el estudio del clima y el entorno atmosférico. En Cuba, las lluvias tienen un impacto significativo en la vida cotidiana, la agricultura, la ecología y muchos otros aspectos de la sociedad. Con el objetivo de proporcionar una comprensión detallada de las precipitaciones en la isla caribeña, nuestra plataforma ofrece un análisis exhaustivo de los datos pluviométricos recopilados a lo largo de los últimos años")
col1.write("Al igual que la humedad relativa, la precipitación es una variable crucial que varía en función de la ubicación geográfica, las condiciónes atmosféricas y la época del año. Nuestra herramienta interactiva te permitirá explorar estos aspectos y comprender mejor las tendencias y variaciónes en las precipitaciones en Cuba. A través de gráficos intuitivos y datos precisos, podrás sumergirte en el fascinante mundo de las lluvias y su impacto en el clima cubano a partir de 1990.")

df = pd.read_csv("./data/base_datos.csv")

##################################################################################################
#Analisis
##################################################################################################

st.markdown("### Valores Globales:")

media = df['Precipitaciones'].mean()
mediana = df['Precipitaciones'].median()
desviacion_estandar = df['Precipitaciones'].std()
varianza = df['Precipitaciones'].var()
maximo = df['Precipitaciones'].max()
minimo = df['Precipitaciones'].min()
data = {'Estadísticas': ['Media', 'Mediana', 'Desviacion Estandar', 'Varianza', 'Maximo', 'Minimo'], 
        'Valor': [media, mediana, desviacion_estandar, varianza, maximo, minimo]}
nuevo_df = pd.DataFrame(data)
st.write(nuevo_df)


###########################################################################


st.write("### Precipitaciones promedios y totales de Cuba en los últimos 30 años:")
df=df.dropna(subset=["Precipitaciones"]) 
df["fecha"] = df.apply(lambda row: str(row['Año']) + '-' + str(row['Mes']), axis=1)
df_mean =df.groupby(["Año","Mes"]).mean("Precipitaciones").reset_index()

#############################################################################

colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4", "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]
st.write("Elige los años que desees, compáralos y saca tus propias conclusiones")
selected_years = st.multiselect('Selecciona los años que quieres visualizar:',options=df["Año"].unique(), default=[])  
df_filtered = df_mean[df_mean["Año"].isin(selected_years) | (selected_years == [])]  
fig = px.line(df_filtered, x="Mes", y="Precipitaciones", color="Año", color_discrete_sequence=colors, title='Comportamiento Anual de las Precipitaciones',labels={"Año": "Años"}, markers=True)
st.plotly_chart(fig)

#############################################################################
st.write("Cuba, una isla caribeña, se caracteriza por su clima tropical que se divide en dos estaciones principales: la temporada de lluvias y la temporada seca.")
st.write("Durante los meses secos en Cuba, que van de noviembre a abril, los días suelen ser soleados y las temperaturas son cálidas y agradables. Por otro lado, durante la temporada de lluvias, que generalmente abarca los meses de mayo a octubre, se experimentan fuertes precipitaciones, con un clima más húmedo y cálido. En este período las lluvias pueden ser intensas, provocando daños económicos y humanos.")

time={1:"seco",2:"seco",3:"seco",4:"seco",5:"lluviosa",6:"lluviosa",7:"lluviosa",
8:"lluviosa",9:"lluviosa",10:"lluviosa",11:"seco",12:"seco"}
df_month=df

df_month["Tiempos"]=df["Mes"].replace(time)

df_month_sum=df.groupby(["Año","Tiempos"]).sum("Precipitaciones").reset_index()

fig = px.line(df_month_sum, x="Año", y="Precipitaciones", color="Tiempos", 
                 title='Comparación de las precipitaciones en los períodos de sequía y períodos de lluvia:',
                 color_discrete_sequence=[ 'Blue', 'Green'])
st.plotly_chart(fig)

##############################################################################
st.markdown("### Comportamiento de las Precipitaciones por Estaciones Meteorológicas por rangos de tiempo:", unsafe_allow_html=True)

selected_stations_default = df["Nombres Estaciones"].unique()[:3].tolist()
selected_stations = st.multiselect("Selecciona las estaciones:", df["Nombres Estaciones"].unique().tolist(), default=selected_stations_default)
start_year_default  = min(df["fecha"].unique())
end_year_default  = max(df["fecha"].unique())

start_year = st.selectbox("Selecciona el año de inicio:", [start_year_default ] + df["fecha"].unique().tolist())
end_year = st.selectbox("Selecciona el año de fin:", [end_year_default ] + df["fecha"].unique().tolist())

filtered_data = df[(df["Nombres Estaciones"].isin(selected_stations)) & (df["fecha"] >= start_year) & (df["fecha"] <= end_year)]
# if an error occurs, it throws an exception,and if not, create a line graph
if filtered_data.empty:
    st.warning("No hay datos disponibles para la estación y el rango de años seleccionados o ha puesto la fecha inicial por encima de la final, vuelva a intentarlo")
else:
    fig = px.line(filtered_data, x='fecha', y='Precipitaciones', color='Nombres Estaciones', title='Comparación de las precipitaciones en diferentes rangos de tiempo y estaciones',)
    st.plotly_chart(fig)

##################################################################################
    
st.write("Comportamiento de las Precipitaciones anuales por Estaciones Meteorológicas")

df_mean_years = df.groupby(["Año","Nombres Estaciones"])["Precipitaciones"].sum()
chosen_station= st.selectbox('Selecciona la estación a analizar', df["Nombres Estaciones"].unique())

if chosen_station:
    df_filtered= df[df["Nombres Estaciones"] == chosen_station]
else :
    df_filtered=df[df["Nombres Estaciones"] == "Cabo Cruz en Granma"]
# groups selected data according to years
df_mean_years_estación = df_filtered.groupby(df_filtered[("Año")])["Precipitaciones"].sum().reset_index()
# create an interactive bar graph
fig = px.bar(df_mean_years_estación, x="Año", y="Precipitaciones", color="Precipitaciones",color_discrete_sequence=["#c61a09", "4194cb", "#235284"],
             title=f"Promedios por año para la estación {chosen_station}")
st.plotly_chart(fig)

#############################################################################################################################################
st.write("¿Cuáles son las estaciones donde se registraron mayores o menores precipitaciones?")

df_mean_years = df.groupby(["Nombres Estaciones", df["Año"]])["Precipitaciones"].sum()
promed = df_mean_years.reset_index()

año_seleccionado = st.slider('Selecciona un año', 1990, 2022, 1990)
mean_selected_year = promed[promed['Año'] == año_seleccionado]


# define the locations
coordinates = df[["Latitud","Longitud"]].apply(lambda x: ','.join(x.astype(str)), axis=1).values
coordinates_unique = list(OrderedDict.fromkeys(coordinates))
locations = [tuple(map(float, ubicación.split(','))) for ubicación in coordinates_unique]

# define the stations
station = df["Nombres Estaciones"].values
unique_station = list(OrderedDict.fromkeys(station))
stations_map = folium.Map(location=[21.93277,-80.41813], zoom_start=6)
# Loop through the locations and unique station names
for i, (ubicación, estación) in enumerate(zip(locations, unique_station)):
    mean = mean_selected_year[mean_selected_year["Nombres Estaciones"]==estación]
    if not mean.empty and not mean["Precipitaciones"].isnull().values.any():
        sum = mean["Precipitaciones"].values[0] 
        # Add a marker to the map with the station name and total precipitation as popup
        folium.Marker(ubicación, popup=f"{estación}: {sum}").add_to(stations_map)
# Create a list of heatmap data containing the location coordinates and precipitation values
datos_mapa_calor = [(ubicación[0], ubicación[1], mean) for ubicación, mean in zip(locations, mean_selected_year["Precipitaciones"]) if mean is not None]
# Add a heatmap layer to the map using the heatmap data
HeatMap(datos_mapa_calor).add_to(stations_map)
# Display the map with markers and heatmap
folium_static(stations_map)

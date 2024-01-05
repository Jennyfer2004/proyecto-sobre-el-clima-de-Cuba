import streamlit as st 
import pandas as pd 
import plotly.express as px
import folium
from streamlit_folium import folium_static
from collections import OrderedDict
from folium.plugins import HeatMap
import os
import io
import PIL as pl

df = pd.read_csv("./data/base_datos.csv")
 
df["Año-Mes"] = df.apply(lambda row: str(row['Año']) + '-' + str(row['Mes']), axis=1)

new_df = df.loc[:, ["Estación", "Año-Mes", "Humedad Relat"]]

#create station dictionary
nombres_estaciones = {
    78310:"Cabo de San Antonio en Pinar del Río",
    78315:"Ciudad de Pinar del Río",
    78318:"Bahía Honda.Artemisa",
    78320:"Güira de Melena en Artemisa",
    78321:"Santa Fé en Isla de la Juventud",
    78323:"Güines en Mayabeque",
    78328:"Varadero en Matanzas",
    78330:"Jovellanos en Matanzas",
    78333:"Playa Girón en Matanzas",
    78344:"Ciudad de Cienfuegos",
    78343:"El Yabú en Santa Clara",
    78349:"Sancti Spíritus Ciudad",
    78346:"Venezuela en Ciego de Ávila",
    78339:"Cayo Coco en Ciego de Ávila",
    78355:"Ciudad de Camagüey",
    78351:"Santa Cruz del Sur en Camagüey",
    78357:"Ciudad de Las Tunas",
    78372:"Pedagogico de Holguín",
    78365:"Cabo Lucrecia en Holguín",
    78377:"Veguitas en Granma",
    78360:"Cabo Cruz en Granma",
    78371:"Pinares de Mayarí en Holguín",
    78364:"Universidad de Santiago de Cuba",
    78368:"Ciudad de Guantánamo",
    78369:"Punta de Maisí en Guantánamo",
    78325:"Casablanca en La Habana"
}

new_df["Nombres Estaciones"] = new_df["Estación"].replace(nombres_estaciones)

new_df.dropna(inplace=True)

df_humedad = pd.DataFrame(new_df)


st.markdown("# Humedad Relativa")

ruta = os.getcwd()
ruta = ruta.replace("\\", "/")

col1,col2 = st.columns(2)
with open(f'{ruta}' + '/images/CubaDew.jpg', 'rb') as f:
    datos_imagen = f.read()
imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1200,800))

col1.image(imagen)

col2.write("La humedad relativa (H.R) es una variable importante en el estudio del clima y el entorno atmosférico, es la relación entre la presión parcial del vapor de agua y la presión de vapor de equilibrio del agua a una temperatura dada. Por ende, esta depende de la temperatura y la presión del sistema de interés. La misma se puede medir con un instrumento conocido como higrómetro, los resultados de las medidas del higrómetro se expresan en porcentajes, un valor de 100% de humedad relativa significa que el aire está totalmente saturado con vapor de agua y no puede contener más, creando la posibilidad de lluvia.")
col2.write("El análisis de la humedad relativa permite obtener una comprensión más profunda de cómo influye en el bienestar humano y de la biosfera, ya juega un papel importante en el confort térmico de los organismos. Los niveles de húmedad del aire pueden variar dependiendo de factores como la ubicación geográfica, la altitud, las condiciónes atmosféricas, la vegetación y la época del año.")
st.write("En esta aplicación se realiza un análisis detallado sobre la H.R en Cuba desde 1990 hasta 2022. Esta herramienta le proporcionará una visión profunda del comportamiento de la humedad en los diferentes meses, años y estaciones de nuestro país, permitiéndole comprender mejor su variación y tendencias a lo largo del tiempo.")


###########################################################
#COMO SE COMPORTO LA HUMEDAD RELATIVA A LO LARGO DEL TIEMPO 
###########################################################
  
st.markdown("### La Humedad Relativa a través del Tiempo")

hu_re = df.groupby(["Año","Mes"])["Humedad Relat"].mean()

h_r = hu_re.reset_index()

#Paleta de colores
colores = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4", "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]

lista_anos = h_r["Año"].unique()

anos_seleccionados = st.multiselect('Selecciona los años que quieres visualizar:',options=lista_anos, default=[])  

df_filtrado = h_r[h_r["Año"].isin(anos_seleccionados) | (anos_seleccionados == [])]  

fig = px.line(df_filtrado, x="Mes", y="Humedad Relat", color="Año", color_discrete_sequence=colores, title='Humedad Relativa por Mes y Año',labels={"Humedad Relat": "Humedad Relativa" , "Año": "Años"}, markers=True)
st.plotly_chart(fig)

################################################################
#CREAR GRÁFICO DE LINEAS A LO LARGO DEL TIEMPO DE CADA ESTACIÓN 
###############################################################
st.write(" ###### Comportamiento de la Humedad Relativa en las diferentes estaciones a través del Tiempo.")

estación_default = df_humedad["Nombres Estaciones"].unique()[0]
año_inicio_default = min(df_humedad["Año-Mes"].unique())
año_fin_default = max(df_humedad["Año-Mes"].unique())

estación = st.selectbox("Selecciona una estación:", [estación_default] + df_humedad["Nombres Estaciones"].unique().tolist())
año_inicio = st.selectbox("Selecciona el año de inicio:", [año_inicio_default] + df_humedad["Año-Mes"].unique().tolist())
año_fin = st.selectbox("Selecciona el año de fin:", [año_fin_default] + df_humedad["Año-Mes"].unique().tolist())

df_estación = df_humedad[(df_humedad["Nombres Estaciones"] == estación) & (df_humedad["Año-Mes"] >= año_inicio) & (df_humedad["Año-Mes"] <= año_fin)]
if df_estación.empty:
    st.warning("No hay datos disponibles para la estación y el rango de años seleccionados")
else:
    fig = px.line(df_estación, x="Año-Mes", y="Humedad Relat", title=f"Húmedad Relativa en la estación {estación}({año_inicio} - {año_fin})")
    st.plotly_chart(fig)

#####################################################################
#COMPARAR ESTACIONES EN UN INTERVALO DE TIEMPO RESPECTO A LA HUMEDAD 
####################################################################
st.write(" ###### Comportamiento de la humedad relativa en un intervalo de tiempo determinado en diferentes estaciones.")
st.write(" ###### Dato-La estación Bahía Honda desde 1990 hasta el mes 10 de 1992 no arrojo resultados de H.R.")

data = df_humedad
selected_stations_default = df_humedad["Nombres Estaciones"].unique()[:3].tolist()
selected_years_default = [year for year in df_humedad["Año-Mes"].unique() if '1990' in year]

selected_stations = st.multiselect("Selecciona las estaciones:", df_humedad["Nombres Estaciones"].unique().tolist(), default=selected_stations_default)
selected_years = st.multiselect('Selecciona los años', data["Año-Mes"].unique(), default=selected_years_default)

filtered_data = data.loc[(data["Año-Mes"].isin(selected_years)) & (data["Nombres Estaciones"].isin(selected_stations))]

fig = px.line(filtered_data, x='Año-Mes', y='Humedad Relat', color='Nombres Estaciones', title='Comparación respecto a la humedad en diferentes años y estaciones',category_orders={'Año-Mes': sorted(selected_years)})
st.plotly_chart(fig)

######################
#PROMEDIOS POR AÑOS 
######################
st.write(" ###### Humedad relativa promedio de cada estación en los últimos 30 años.")

df_humedad["Año"] = df_humedad["Año-Mes"].str.split('.').str[0]

df_humedad["Estación"] = df_humedad["Nombres Estaciones"]

df_promedio_años = df_humedad.groupby(["Año","Estación"])["Humedad Relat"].mean()

estación_elegida = st.selectbox('Selecciona la estación a analizar', df_humedad["Nombres Estaciones"].unique())

df_filtrado = df_humedad[df_humedad["Estación"] == estación_elegida]

df_promedio_años_estación = df_filtrado.groupby(df_filtrado[("Año")].str[:4])["Humedad Relat"].mean().reset_index()

st.write("Acerca el gráfico tanto como quieras y obtén una mejor visualización.")

fig = px.bar(df_promedio_años_estación, x="Año", y="Humedad Relat", color="Año",color_discrete_sequence=colores,
             labels={"Húmedad Relat": "Promedio de Humedad Relativa", "Año": "Año"},
             title=f"Promedios de humedad relativa por año para la estación {estación_elegida}")

st.plotly_chart(fig)


###############################################################################################################
#Analizar de regiónes más humedas o secas según el promedio general en los 30 años a traves de mapa iteractivo. 
###############################################################################################################
st.write(" ##### ¿Cúales son las estaciones más humedas ? ¿Cúales son las estaciones  más secas?")
st.write("Al observar los valores de humedad relativa promedio de cada estación en cada año de los últimos 30 años se podría conocer cual de estas estaciones es más humeda o más seca. En términos generales, se considera que un ambiente es húmedo cuando la humedad relativa es superior al 60%, por otro lado, si la humedad relativa es inferior al 30%, el ambiente se considera seco.")

# Extraer el año y convertirlo a int
df_humedad['Año'] = df_humedad['Año'].str.split('-').str[0].astype(int)

# Filtrar los datos desde 1990 hasta 2022
df_humedad = df_humedad[(df_humedad['Año'] >= 1990) & (df_humedad['Año'] <= 2022)]

# Calcular el promedio de humedad relativa por años
df_promedio_años = df_humedad.groupby(["Estación", df_humedad["Año"]])["Humedad Relat"].mean()

promed = df_promedio_años.reset_index()

# Agregar un slider para filtrar por el año seleccionado
año_seleccionado = st.slider('Selecciona un año', 1990, 2022, 1990)

promed_año_seleccionado = promed[promed['Año'] == año_seleccionado]

# En el popup aparecerá el promedio correspondiente de cada estación en ese año
dict = dict(zip(promed_año_seleccionado["Estación"], promed_año_seleccionado["Humedad Relat"]))

# Definir las ubicaciónes
coordenadas = df[["Latitud","Longitud"]].apply(lambda x: ','.join(x.astype(str)), axis=1).values
coordenadas_unicas = list(OrderedDict.fromkeys(coordenadas))
ubicaciónes = [tuple(map(float, ubicación.split(','))) for ubicación in coordenadas_unicas]

# Definir las estaciones únicas
estaciones = df["Nombres Estaciones"].values
estaciones_unicas = list(OrderedDict.fromkeys(estaciones))

mapa_estaciones = folium.Map(location=[21.93277,-80.41813], zoom_start=6)

for i ,(ubicación, estación) in  enumerate(zip(ubicaciónes, estaciones_unicas)):
    promedio = dict.get(estación)
    if promedio is not None:
        folium.Marker(ubicación, popup=f"{estación}: {promedio}").add_to(mapa_estaciones)
    
datos_mapa_calor = [(ubicación[0], ubicación[1], promedio) for ubicación, promedio in zip(ubicaciónes, promed_año_seleccionado["Humedad Relat"]) if promedio is not None]

HeatMap(datos_mapa_calor).add_to(mapa_estaciones)

folium_static(mapa_estaciones)


st.write(" ##### ¿Ha observado que todas las estaciones presentan un promedio de humedad relativa casi idéntico y superio al 60%?")
st.write("Cuba es un país que se distingue por su clima cálido y tropical, que por estaciones es considerablemente húmedo. La humedad ambiental se debe a la inevitable influencia del mar y los rasgos de la insularidad, cumpliéndose la prevalencia de constante humedad y lluvias.")

############################################################
#GRÁFICO COMPARATIVO DE PROMEDIOS GENERALES DE CADA ESTACIÓN 
############################################################
st.write(" ### ¡Comprueba por ti mismo la humedad de estas 26 estaciones según el promedio de cada una en los últimos 30 años!")

# # Calcular el promedio de humedad relativa por estación
# df_promedio_estaciones = df_humedad.groupby("Estación")["Humedad Relat"].mean()

# # Crear un DataFrame con los nombres de las estaciones y los promedios de humedad
# pro_est = pd.DataFrame({"Estaciones": df_promedio_estaciones.index, "Promedio de humedad": df_promedio_estaciones.values})

# # Crear el gráfico de dispersión
# fig = px.scatter(pro_est, x="Estaciones", y="Promedio de humedad", title="Promedio general de humedad por estación en los últimos 30 años",color = "Estaciones",color_discrete_sequence=colores)

# fig.update_layout(legend={
#     'title': 'Estaciones',
#     'traceorder': 'normal',
#     'font': {
#         'family': 'sans-serif',
#         'size': 12,
#         'color': 'black'
#     },
#     'bgcolor': 'LightSteelBlue',
#     'bordercolor': 'Black',
#     'borderwidth': 2
# })

# st.plotly_chart(fig)


if df_humedad['Año'].dtype == 'object':
    # Extraer el año y convertirlo a int
    df_humedad['Año'] = df_humedad['Año'].str.split('-').str[0].astype(int)

# Filtrar los datos desde 1990 hasta 2022
df_humedad = df_humedad[(df_humedad['Año'] >= 1990) & (df_humedad['Año'] <= 2022)]

# Calcular el promedio de humedad relativa por estaciones
df_promedio_estaciones = df_humedad.groupby("Estación")["Humedad Relat"].mean()

# Crear un DataFrame con los nombres de las estaciones y los promedios de humedad
pro_est = pd.DataFrame({"Estaciones": df_promedio_estaciones.index, "Promedio de humedad": df_promedio_estaciones.values})

# Definir las estaciones seleccionadas por defecto
estaciones_seleccionadas_default = pro_est['Estaciones'][:3]

# Permitir al usuario seleccionar las estaciones
estaciones_seleccionadas = st.multiselect('Selecciona las estaciones que quieres comparar :', pro_est['Estaciones'], default=estaciones_seleccionadas_default)

if estaciones_seleccionadas:
    pro_est_filtrado = pro_est[pro_est['Estaciones'].isin(estaciones_seleccionadas)]
    fig = px.scatter(pro_est_filtrado, x="Estaciones", y="Promedio de humedad", 
                     title="Comparación de humedad promedio por cada estación seleccionada",
                     color="Estaciones", color_discrete_sequence=colores)
    fig.update_layout(legend={
        'title': 'Estaciones',
        'traceorder': 'normal',
        'font': {
            'family': 'sans-serif',
            'size': 12,
            'color': 'black'
        },
        'bgcolor': 'LightSteelBlue',
        'bordercolor': 'Black',
        'borderwidth': 2
    })
    st.plotly_chart(fig)












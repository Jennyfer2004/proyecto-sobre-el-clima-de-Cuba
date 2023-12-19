 
import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
import geopandas as gpd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from collections import OrderedDict
from folium.plugins import HeatMap



#read the csv in dataframe 
df = pd.read_csv("D:/proyecto-sobre-el-clima-de-Cuba/base_datos.csv")
print(df)

#df = pd.read_excel("D:/proyecto-sobre-el-clima-de-Cuba/app/data/data.xlsx")
#print(df)




#Check with Head
#print(df.head())

#show database
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#print(df)

 
 
df["Año-Mes"] = df.apply(lambda row: str(row['Año']) + '-' + str(row['Mes']), axis=1)
#print(df["Año-Mes"])



new_df = df.loc[:, ["Estación", "Año-Mes", "Humedad Relat"]]
#print(new_df)
 
#delete missing data 
#new_df.dropna()
#print(new_df.dropna())

#check missing data 
#print(new_df.isnull().sum())


#create station dictionary


nombres_estaciones = {
    78310:"Cabo de San Antonio.Pinar del Río",
    78315:"Pinar del Río Ciudad",
    78318:"Bahía Honda.Artemisa",
    78320:"Güira de Melena.Artemisa",
    78321:"Santa Fe.Isla de la Juventud",
    78323:"Güines.Mayabeque",
    78328:"Varadero.Matanzas",
    78330:"Jovellanos.Matanzas",
    78333:"Playa Girón.Matanzas",
    78344:"Cienfuegos Ciudad",
    78343:"El Yabú.Santa Clara",
    78349:"Sancti Spirítus Ciudad",
    78346:"Venezuela.Ciego de Ávila",
    78339:"Cayo Coco.Ciego de Ávila",
    78355:"Camagüey Ciudad",
    78351:"Santa Cruz del Sur.Camagüey",
    78357:"Las Tunas Ciudad",
    78372:"Pedagogico.Holguín",
    78365:"Cabo Lucrecia.Holguín",
    78377:"Veguitas.Granma",
    78360:"Cabo Cruz.Granma",
    78371:"Pinares de Mayarí.Holguín",
    78364:"Universidad.Santiago de Cuba",
    78368:"Guantánamo Ciudad",
    78369:"Punta de Maisí.Guantánamo",
    78325:"Casablanca.La Habana"
}

#Reemplaza los valores en la columna "Nombres Estaciones" con los nombres de estación correspondientes
new_df["Nombres Estaciones"] = new_df["Estación"].replace(nombres_estaciones)


#delete missing data 
new_df.dropna(inplace=True)
#print(new_df.dropna(inplace=True))


#check missing data 
#print(new_df.isnull().sum())

#print(new_df) 



#convert new_df to Dataframe
df_humedad = pd.DataFrame(new_df)


#Personalizar el color de fondo utilizando CSS
st.markdown(
    """
    <style>
    body {
        background-color: lightblue;
    }
    </style>
    """,
    unsafe_allow_html=True
)


#add title to the web app
st.title("La Húmedad Relativa en Cuba")



st.write(" ###### La húmedad relativa(H.R) es una variable importante en el estudio del clima y el entorno atmosférico,es la relación entre la presión parcial del vapor de agua y la presión de vapor de equilibrio del agua a una temperatura dada,por ende esta depende de la temperatura y la presión del sistema de interés.La misma se puede medir con un instrumento conocido como higrómetro,los resultados de las medidas del higrómetro se expresan en porcentajes,un valor de 100% de humedad relativa significa que el aire está totalmente saturado con vapor de agua y no puede contener más,creando la posibilidad de lluvia.")
st.write(" ###### El análisis de la humedad relativa permite obtener una comprensión más profunda de cómo influye en el bienestar humano y en la propagación de enfermedades,en general juega un papel importante en el confort térmico de la humanidad.")
st.write(" ###### Los niveles de húmedad del aire pueden variar dependiendo de factores como la ubicación geográfica,la altitud,las condiciones atmosféricas,la vegetación y la época del año.")
st.write(" ###### En esta aplicación se realiza un análisis detallado sobre la H.R en Cuba desde 1990 hasta 2022.Esta herramienta le proporcionará una visión profunda del comportamiento de la humedad en los diferentes meses,años y estaciones de nuestro país,permitiéndole comprender mejor su variación y tendencias a lo largo del tiempo,con gráficos intuitivos y datos precisos.En general con esta app podrá obtener una visión clara y concisa de este aspecto crucial del medio ambiente.")
st.write(" ###### Sin más le invito a explorar la app web dedicada exclusivamente a:")
st.write(" ##### LA HUMEDAD RELATIVA EN CUBA EN CUBA DURANTE LOS ÚLTIMOS 30 AÑOS")

st.write(" ###### ¡No pierdas más tiempo y realiza tu propia investigación!")


user_name = st.text_input("Escribe tu nombre...")

if user_name:
    button_press = st.button("Bienvenid@ " + user_name + ".En esta app puedes encontrar información interesante sobre la húmedad relativa en Cuba en los últimos 30 años.")
    if button_press:
        st.write("Hola " + user_name + "! ¡Gracias por presionar el botón!")






#COMO SE COMPORTO LA HUMEDAD RELATIVA A LO LARGO DEL TIEMPO 

#print(df)

st.write(" ###### ¿Cómo se comportó la humedad relativa del país en cada mes desde 1990 hasta 2022?")
st.write(" ###### ¿Cuáles son los meses con humedad relativa más agradable o desagradable?")


#Calcular el promedio de humedad relativa por cada año en cada mes  
hu_re = df.groupby(["Año","Mes"])["Humedad Relat"].mean()
#print(hu_re)


#Colocar nombre a las columnas correctamente 
h_r = hu_re.reset_index()
#print(h_r)


#Paleta de colores
colores = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4", "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]

#colores_oscuros = ['#0B3D91', '#08415C', '#540B0E', '#2F1B25', '#2C3539','#464646', '#3C1414', '#3B1F2B', '#1B263B', '#0D1B2A','#1D1E33', '#5C3C6D', '#25342B', '#3E4C59', '#1F2833','#4C3F54', '#242325', '#3A3A3A', '#1C2321', '#2E4057','#2B2D42', '#343837', '#2F4538', '#FFD700', '#483C32','#534B4F', '#1B1B1B', '#2D4263', '#0B0C10', '#101820']
#colores_pastel = ['#FBB4AE', '#B3CDE3', '#CCEBC5', '#DECBE4', '#FED9A6','#FFFFCC', '#E5D8BD', '#FDDAEC', '#F2F2F2', '#B3E2CD','#FDCDAC', '#F4CAE4', '#E6F5C9', '#FFF2AE', '#F1E2CC','#CCCCCC', '#88B378', '#D5A6BD', '#AEC6CF', '#FFD1DC','#B39EB5', '#B19CD9', '#CFCFC4', '#CB99C9', '#77DD77','#836953', '#C23B22', '#F49AC2', '#BDB2FF', '#FF6961','#000000' ]


#Obtener una lista de años únicos del DataFrame
lista_anos = h_r["Año"].unique()


#Casilla de selección para que el usuario elija los años a visualizar
anos_seleccionados = st.multiselect('Selecciona los años que quieres visualizar:',options=lista_anos, default=[])  #lista vacía por defecto


#Filtrar el DataFrame para incluir solo los años seleccionados
df_filtrado = h_r[h_r["Año"].isin(anos_seleccionados) | (anos_seleccionados == [])]  #incluye todos los años si la selección está vacía


#Crear el gráfico de líneas con marcadores
fig = px.line(df_filtrado, x="Mes", y="Humedad Relat", color="Año", color_discrete_sequence=colores, title='Humedad Relativa por mes y año',labels={"Humedad Relat": "Humedad Relativa" , "Año": "Años"}, markers=True)


#Mostrar grafico 
st.plotly_chart(fig)
























#CREAR GRÁFICO DE LINEAS A LO LARGO DEL TIEMPO DE CADA ESTACIÓN 

st.write(" ###### ¿Te interesaría saber cómo se han comportado las diferentes estaciones respecto a la humedad relativa a lo largo del tiempo desde 1990 hasta 2022?")

#Inicializar la variable estación con None
estacion = pd.DataFrame()


#Crear un widget de selección de estación
estacion = st.selectbox("Selecciona una estación:", [''] + df_humedad["Nombres Estaciones"].unique().tolist())


#Verificar si se ha seleccionado una estación
if not  estacion:
    df_estacion = None 
else:
    #Crear dos widgets de selección de año
    año_inicio = st.selectbox("Selecciona el año de inicio:", df_humedad["Año-Mes"].unique().tolist())
    año_fin = st.selectbox("Selecciona el año de fin:", df_humedad["Año-Mes"].unique().tolist())
    #Verificar si se han seleccionado un año de inicio y un año de fin
    if not  año_inicio or not año_fin:
        df_estacion = None 
    else:
    #Filtrar los datos por la estación y el rango de años seleccionados
        df_estacion = df_humedad[(df_humedad["Nombres Estaciones"] == estacion) & (df_humedad["Año-Mes"] >= año_inicio) & (df_humedad["Año-Mes"] <= año_fin)]
        # Verificar si hay datos filtrados
        if df_estacion.empty:
            st.warning("No hay datos disponibles para la estación y el rango de años seleccionados")
        else:
            # Crear un gráfico interactivo de líneas
            fig = px.line(df_estacion, x="Año-Mes", y="Humedad Relat", title=f"Húmedad Relativa en la estación {estacion}({año_inicio} - {año_fin})")
            st.plotly_chart(fig)







#COMPARAR ESTACIONES EN UN INTERVALO DE TIEMPO RESPECTO A LA HUMEDAD 

st.write(" ###### ¿Cómo se comportó la humedad relativa en un intervalo de tiempo determinado en diferentes estaciones?")
st.write("Dato-La estación Bahía Honda desde 1990 hasta el mes 10 de 1992 no arrojo resultados de H.R.")


# Crear datos de ejemplo
data = df_humedad
#print(data)


#Obtener años y estaciones seleccionadas por el usuario
selected_years = st.multiselect('Selecciona los años', data["Año-Mes"].unique())
selected_stations = st.multiselect("Selecciona las estaciones:", [''] + df_humedad["Nombres Estaciones"].unique().tolist())



#Filtrar el DataFrame según la selección del usuario utilizando la función loc[]
filtered_data = data.loc[(data["Año-Mes"].isin(selected_years)) & (data["Nombres Estaciones"].isin(selected_stations))]
#print(filtered_data)



#Crear el gráfico de líneas interactivo utilizando Plotly Express
fig = px.line(filtered_data, x='Año-Mes', y='Humedad Relat', color='Nombres Estaciones', title='Comparación respecto a la humedad en diferentes años y estaciones',category_orders={'Año-Mes': sorted(selected_years)})

#Mostrar el gráfico en la aplicación de Streamlit
st.plotly_chart(fig)












#PROMEDIOS POR AÑOS 

st.write(" ###### ¿Cómo se comportó la humedad relativa promedio en los últimos 30 años?")

#Extraer el año de la columna 'Año-Mes'
df_humedad["Año"] = df_humedad["Año-Mes"].str.split('.').str[0]
#print(df_humedad["Año"])



#Extraer la estación de la columna 'Nombres Estaciones'
df_humedad["Estación"] = df_humedad["Nombres Estaciones"]
#print(df_humedad["Estación"])


#Calcular el promedio de humedad relativa por años
df_promedio_años = df_humedad.groupby(["Año","Estación"])["Humedad Relat"].mean()
#print(df_promedio_años)



#seleccion del usuario
estacion_elegida = st.selectbox('Selecciona la estación a analizar', df_humedad["Nombres Estaciones"].unique())


# Filtrar el DataFrame por la estación seleccionada
df_filtrado = df_humedad[df_humedad["Estación"] == estacion_elegida]


# Calcular el promedio de humedad relativa por años para la estación seleccionada
df_promedio_años_estacion = df_filtrado.groupby(df_filtrado[("Año")].str[:4])["Humedad Relat"].mean().reset_index()
#print(df_promedio_años_estacion)


st.write("Acerca el gráfico tanto como quieras y obtén una mejor visualización.")

#colores
colores = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4", "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]


# Crear un gráfico de barras interactivo con Plotly Express
fig = px.bar(df_promedio_años_estacion, x="Año", y="Humedad Relat", color="Año",color_discrete_sequence=colores,
             labels={"Húmedad Relat": "Promedio de Humedad Relativa", "Año": "Año"},
             title=f"Promedios de humedad relativa por año para la estación {estacion_elegida}")

# Mostrar el gráfico interactivo en Streamlit
st.plotly_chart(fig)















#Analizar de regiones más humedas o secas según el promedio general en los 30 años a traves de mapa iteractivo


#Calcular el promedio de humedad relativa por años
df_promedio_años = df_humedad.groupby(["Estación", df_humedad["Año"].str[:4]])["Humedad Relat"].mean()
#print(df_promedio_años)


#que el dataframe tome los nombres de las columnas correctamente 
promed = df_promedio_años.reset_index()
#print(promed)


#Sumar los promedios de humedad de los últimos 30 años para cada estación y dividirlos entre el total para obtener el promedio general por estación en los últimos 30 años
df_promedio_estaciones = promed.groupby(["Estación"])["Humedad Relat"].mean()
#print(df_promedio_estaciones)


#Poner correctamente los nombres a las columnas 
df_new_promedios_estaciones = df_promedio_estaciones.reset_index()
#print(df_new_promedios_estaciones)




st.write(" ##### ¿Cúales son las estaciones más humedas ?¿Cúales son las estaciones  más secas?")
st.write(" ###### Al observar los valores de humedad relativa promedio de cada estación en los últimos 30 años se podría conocer cual de estas estaciones es más humeda o más seca.En términos generales,se considera que un ambiente es húmedo cuando la humedad relativa es superior al 60%,por otro lado, si la humedad relativa es inferior al 30%,el ambiente se considera seco.")


#Almacenar las localizaciones , la latitud y longitud separadas por comas 
coordenadas = df[["Latitud","Longitud"]].apply(lambda x: ','.join(x.astype(str)), axis=1).values
#print(coordenadas) 


#from collections import OrderedDict
#Eliminar duplicados y mantener el orden original
coordenadas_unicas = list(OrderedDict.fromkeys(coordenadas))
#print(coordenadas_unicas)


#crear lista de tuplas de dos valores que representan la latitud y longitud de cada ubicación en coordenadas 
ubicaciones = [tuple(map(float, ubicacion.split(','))) for ubicacion in coordenadas_unicas]
#print(ubicaciones) 



#Almacenar las estaciones 
estaciones = df["Nombres Estaciones"].values
#print(estaciones)


#Eliminar duplicados y mantener el orden original
estaciones_unicas = list(OrderedDict.fromkeys(estaciones))
#print(estaciones_unicas)


#Promedios de cada estación 
promedios = df_new_promedios_estaciones["Humedad Relat"]
#print(promedios)


#Crear un diccionario que mapea el nombre de la región con su promedio de humedad relativa
dict = dict(zip(df_new_promedios_estaciones["Estación"],df_new_promedios_estaciones["Humedad Relat"]))
#print(dict)


#Crear mapa centrado en una ubicación inicial
mapa_estaciones = folium.Map(location=[21.93277,-80.41813], zoom_start=6)



#Iterar sobre las ubicaciones y estaciones
for i ,(ubicacion, estacion) in  enumerate(zip(ubicaciones, estaciones_unicas)):
    # Obtener el promedio de humedad de dict_promedios
    promedio = dict.get(estacion)
    
    # Crear un marcador en la ubicación con un popup que muestra el nombre de la estación y su promedio
    folium.Marker(ubicacion, popup=f"{estaciones_unicas[i]}: {promedio}").add_to(mapa_estaciones)




#Crear una lista de datos que incluya la latitud, longitud y el valor de humedad para el mapa de calor
datos_mapa_calor = [(ubicacion[0], ubicacion[1], promedio) for ubicacion, promedio in zip(ubicaciones, promedios)]


#Añadir la capa de mapa de calor al mapa existente
HeatMap(datos_mapa_calor).add_to(mapa_estaciones)


#Usar folium_static para mostrar el mapa en Streamlit
folium_static(mapa_estaciones)




st.write(" ##### ¿Ha observado que todas las estaciones presentan un promedio de humedad relativa casi idéntico y superio al 60%?")
st.write(" ###### Cuba es un país que se distingue por su clima cálido y tropical,que por estaciones es considerablemente húmedo.La humedad ambiental se debe a la inevitable influencia del mar y los rasgos de la insularidad,cumpliéndose la prevalencia de constante humedad y lluvias.")
st.write("El rol del Citma en asegurar la sostenibilidad ambiental en el desarrollo económico y social del país,el Citma da coherencia a la política medioambiental.")
st.write("Día Mundial del Medio Ambiente se celebra cada año el 5 de junio?")


#Crear grafico comparativo con los promedios generales de cada estacion 

st.write(" ###### Comprueba tu mism@ la humedad de estas 26 estaciones según el promedio de cada una en los últimos 30 años.")

#print(df_new_promedios_estaciones)


#Crear una lista de los promedios generales de humedad de cada estación en los últimos 30 años
prome =df_new_promedios_estaciones["Humedad Relat"]
#print(prome)


#Crear una lista de los nombres de las estaciones
nombres_estaciones = df_new_promedios_estaciones["Estación"]
#print(nombres_estaciones)


#Crear df con los datos 
pro_est = pd.DataFrame({"Estaciones": nombres_estaciones, "Promedio de humedad": prome})
#print(pro_est)


#Crear una paleta de colores personalizada
colores = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#000000", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#FFA07A", "#FFD700", "#ADFF2F", "#7FFFD4", "#00BFFF", "#1E90FF", "#8A2BE2", "#FF69B4", "#FF1493", "#9400D3", "#4B0082", "#FF4500"]


# Crear el gráfico de áreas
fig = px.scatter(pro_est, x="Estaciones", y="Promedio de humedad", title="Promedio general de humedad por estación en los últimos 30 años",color = "Estaciones",color_discrete_sequence=colores)


# Ajustar la leyenda para mostrar todas las estaciones
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


#Mostrar el gráfico 
st.plotly_chart(fig)




st.write(" ###### Realiza tu propia comparación con las estaciones deseadas.")

#Solicitar al usuario que seleccione las estaciones que desea comparar (opcional)
estaciones_seleccionadas = st.multiselect('Selecciona las estaciones que quieres comparar :', nombres_estaciones)

#Si el usuario selecciona estaciones, actualizar el gráfico para mostrar solo esas estaciones
if estaciones_seleccionadas:
    #Filtrar el DataFrame basado en las estaciones seleccionadas por el usuario
    pro_est_filtrado = pro_est[pro_est['Estaciones'].isin(estaciones_seleccionadas)]
    
    #Actualizar el gráfico con las estaciones seleccionadas
    fig = px.scatter(pro_est_filtrado, x="Estaciones", y="Promedio de humedad", 
                     title="Comparación de humedad por estación seleccionada",
                     color="Estaciones", color_discrete_sequence=colores)
    
    #Ajustar la leyenda para mostrar solo las estaciones seleccionadas
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
    
    #Mostrar el gráfico actualizado
    st.plotly_chart(fig)
    
    













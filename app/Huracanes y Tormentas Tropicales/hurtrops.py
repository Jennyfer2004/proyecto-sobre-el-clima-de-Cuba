import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import PIL as pl
import folium
from streamlit_folium import folium_static


current_path = os.getcwd()
path= os.path.dirname(current_path)
path = path.replace("\\", "/") 
df = pd.read_csv("./data/huracanes.csv")
df_storms = pd.read_csv("./data/tstorms.csv")

st.markdown("# Huracanes y Tormentas Tropicales")

opciones = ["Huracanes", "Tormentas Tropicales"]
selección = st.selectbox('Selecciona una opción:', opciones)

#######################################################################################################################
#HURACANES
#######################################################################################################################

if selección == "Huracanes":

    df_temp = df
    df_temp['Fecha'] = pd.to_datetime(df['Fecha'], format='%m/%d/%Y')
    df_temp['Año'] = df['Fecha'].dt.year
    media_huracanes = df_temp.groupby('Año').size().mean()


    col1, col2 = st.columns(2)
    with open(f'{path}' + '/app/images/HurricaneAI.jpg', 'rb') as f:
        datos_imagen = f.read()
    imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))

    col1.image(imagen)

    col2.write('''Los huracanes son fenómenos meteorológicos extremos que pueden tener un impacto significativo en las regiónes donde ocurren. En particular, Cuba, una isla en el Caribe, es una región que a menúdo se ve afectada por estos eventos. El estudio de los huracanes en Cuba es de vital importancia por varias razones:
    
Los huracanes pueden causar daños significativos a la infraestructura y a la economía. Los fuertes vientos y las lluvias intensas pueden destruir edificios, carreteras y otras infraestructuras, lo que puede costar millones de dólares en reparaciónes. Además, pueden interrumpir las actividades económicas, como el turismo, que es una fuente importante de ingresos para Cuba.

Tambien pueden tener un impacto significativo en el medio ambiente, pues pueden causar erosión en las playas y en las zonas costeras, dañar los arrecifes de coral y alterar los ecosistemas marinos y terrestres.''')
    
    st.write('''Además, impactan directamente la vida y la seguridad de las personas. Pueden causar lesiones o incluso la muerte, y pueden desplazar a las personas de sus hogares. El estudio de los huracanes puede ayudar a predecir su trayectoria y su intensidad, lo que puede permitir una mejor preparación y respuesta a estos eventos.

Por último, el estudio de los huracanes puede proporcionar información valiosa para entender los efectos del cambio climático. Se espera que la intensidad y la frecuencia de los huracanes aumenten como resultado del calentamiento global, por lo que entender estos fenómenos puede ayudar a predecir y prepararse para los efectos futuros del cambio climático.

En resumen, el estudio de los huracanes en Cuba es crucial para proteger la economía, el medio ambiente y la vida de las personas. A través de la investigación y la educación, podemos mejorar nuestra capacidad para predecir, prepararnos y responder a estos eventos extremos.''')

    st.markdown("### Huracanes en Cuba en el período 1996-2022")
    
    df_show = df[["Nombre","Fecha","Vientos Máximos", "Presion Central", "Categoría", "Región"]]
    df_show['Fecha'] = pd.to_datetime(df_show['Fecha']).dt.date
    st.write(df_show)
    st.write(f"La media de huracanes por año fue de {media_huracanes}")


###########################################################################################################
#Cantidad de Huracanes por Mes Categoría y Ano
###########################################################################################################
    st.markdown("### Cantidad de Huracanes en Cuba por Mes, Año, Categoría y Región de Entrada")

    col1, col2 = st.columns(2)

    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%m/%d/%Y')

    df['Mes'] = df['Fecha'].dt.month
    df['Año'] = df['Fecha'].dt.year

    data = df.groupby('Año').size().reset_index(name='Huracanes')

    fig, ax = plt.subplots()
    ax.bar(data['Año'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Número de Huracanes')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col2.pyplot(fig)

    data = df.groupby('Mes').size().reset_index(name='Huracanes')
    fig, ax = plt.subplots()
    ax.bar(data['Mes'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Mes')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Número de Huracanes')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col1.pyplot(fig)

    data = df.groupby('Categoría').size().reset_index(name='Huracanes')
    fig, ax = plt.subplots()
    ax.bar(data['Categoría'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Categoría')
    ax.set_xlabel('Categoría')
    ax.set_ylabel('Número de Huracanes')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col1.pyplot(fig)

    data = df.groupby('Región').size().reset_index(name='Huracanes')
    fig, ax = plt.subplots()
    ax.bar(data['Región'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Región')
    ax.set_xlabel('Región')
    ax.set_ylabel('Número de Huracanes')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col2.pyplot(fig)

###########################################################################################################
#Información General de los Huracanes
###########################################################################################################
    
    st.markdown("### Visualización Comparativa de la información sobre Huracanes")

    hurricane_names = df['Nombre'].unique().tolist()

    selected_hurricanes = st.multiselect('Elige los Huracanes que quieres visualizar:', hurricane_names)

    col1, col2 = st.columns(2)

    for i, hurricane in enumerate(selected_hurricanes):
        
        col = col1 if i % 2 == 0 else col2

        hurricane_data = df[df['Nombre'] == hurricane].drop(['Mes', 'Año'], axis=1)
        hurricane_data = hurricane_data[["Nombre","Fecha","Vientos Máximos", "Presion Central", "Categoría", "Región"]]
        hurricane_data['Fecha'] = pd.to_datetime(hurricane_data['Fecha']).dt.date

        col.write(hurricane_data)

        if os.path.exists(f'{path}' + "/app/images/" + f"{hurricane}" + ".jpg"):
            with open(f'{path}' + "/app/images/" + f"{hurricane}" + ".jpg", 'rb') as f:
                datos_imagen = f.read()
            imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))
            col.image(imagen, caption=hurricane, use_column_width=True)
        else:
            col.warning(f"No se encontró la trayectoria para el huracán {hurricane}")


#############################################################################################################################
#TORMENTAS TROPICALES
#############################################################################################################################


if selección == "Tormentas Tropicales":

    col1, col2 = st.columns(2)
    with open(f'{path}' + '/app/images/tropstorm.jpg', 'rb') as f:
        datos_imagen = f.read()
    imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))

    col2.image(imagen)

    col1.write('''Conocer los datos sobre las tormentas tropicales es de vital importancia para Cuba debido a la alta frecuencia con la que este país es afectado por estos fenómenos. Los datos precisos sobre estos sistemas meteorológicos permiten a los expertos predecir su trayectoria, intensidad y posibles efectos, lo que a su vez permite a las autoridades y a la población prepararse de manera adecuada.

Además, el análisis de estos datos a lo largo del tiempo puede revelar patrones y tendencias que podrían ser útiles para entender cómo estos fenómenos podrían cambiar en el futuro debido al cambio climático y otros factores. Esto es especialmente relevante para un país como Cuba, que se encuentra en una región propensa a las tormentas tropicales.

Finalmente, estos datos también son fundamentales para la planificación urbana y el desarrollo de infraestructuras resistentes al clima en Cuba. Por ejemplo, los datos sobre las zonas más afectadas por las tormentas tropicales pueden informar las decisiones sobre dónde construir nuevas viviendas o infraestructuras, o cómo mejorar las existentes para resistir mejor a estos eventos.''')
    
    st.markdown("### Tormentas Tropicales en Cuba en el período 1992-2022")

    st.markdown('')
    st.markdown('')
    
    col1,col2 = st.columns([1.75,2.5])
    col1.write(df_storms)


    df_storms['lat'] = pd.to_numeric(df_storms['lat'])
    df_storms['lon'] = pd.to_numeric(df_storms['lon'])

    m = folium.Map(location=[df_storms['lat'].mean(), df_storms['lon'].mean()], zoom_start=6)

    for idx, row in df_storms.iterrows():
        row_as_str = ', '.join(row.map(str))
        folium.Marker(location=[row['lat'], row['lon']], 
                    popup=row_as_str).add_to(m)
        
    with col2: folium_static(m)



###########################################################################################################
#Cantidad de Tormentas Tropicales por Mes Categoría y Ano
###########################################################################################################
    


    st.markdown("### Cantidad de Tormentas Tropicales en Cuba por Mes, Año, Categoría y Región de Entrada")

    col1, col2 = st.columns(2)

    df_storms['Fecha'] = pd.to_datetime(df_storms['Fecha'], format='%m/%d/%Y')

    df_storms['Mes'] = df_storms['Fecha'].dt.month
    df_storms['Año'] = df_storms['Fecha'].dt.year

    data = df_storms.groupby('Año').size().reset_index(name='Tormentas Tropicales')
###########################################
    fig, ax = plt.subplots()
    ax.bar(data['Año'], data['Tormentas Tropicales'])
    ax.set_title('Número de Tormentas Tropicales por Año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Número de Tormentas Tropicales')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col2.pyplot(fig)
#############################################
    data = df_storms.groupby('Mes').size().reset_index(name='Tormentas Tropicales')
    fig, ax = plt.subplots()
    ax.bar(data['Mes'], data['Tormentas Tropicales'])
    ax.set_title('Número de Tormentas Tropicales por Mes')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Número de Tormentas Tropicales')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col1.pyplot(fig)
#################################################

    data = df_storms.groupby('Vientos Máximos').size().reset_index(name='Tormentas Tropicales')
    fig, ax = plt.subplots()
    ax.bar(data['Vientos Máximos'], data['Tormentas Tropicales'])
    ax.set_title('Número de Tormentas Tropicales por Vientos Máximos')
    ax.set_xlabel('Vientos Máximos')
    ax.set_ylabel('Número de Tormentas Tropicales')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col1.pyplot(fig)

#####################################################
    data = df.groupby('Región').size().reset_index(name='Tormentas Tropicales')
    fig, ax = plt.subplots()
    ax.bar(data['Región'], data['Tormentas Tropicales'])
    ax.set_title('Número de Tormentas Tropicales por Región')
    ax.set_xlabel('Región')
    ax.set_ylabel('Número de Tormentas Tropicales')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col2.pyplot(fig)



    
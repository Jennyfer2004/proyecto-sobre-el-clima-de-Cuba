import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import os
import io
import PIL as pl
import seaborn as sns

current_path = os.getcwd()
path= os.path.dirname(current_path)
path = path.replace("\\", "/") 
df = pd.read_csv("./data/huracanes.csv")
df_storms = pd.read_csv("./data/tstorms.csv")

st.title("Huracanes y Tormentas Tropicales")

opciones = ["Huracanes", "Tormentas Tropicales"]
seleccion = st.selectbox('Selecciona una opción:', opciones)

#######################################################################################################################
#HURACANES
#######################################################################################################################

if seleccion == "Huracanes":

    col1, col2 = st.columns(2)
    with open(f'{path}' + '/app/images/HurricaneAI.jpg', 'rb') as f:
        datos_imagen = f.read()
    imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))

    col1.image(imagen)

    col2.write('''Los huracanes son fenómenos meteorológicos extremos que pueden tener un impacto significativo en las regiones donde ocurren. En particular, Cuba, una isla en el Caribe, es una región que a menudo se ve afectada por estos eventos. El estudio de los huracanes en Cuba es de vital importancia por varias razones.
    
Los huracanes pueden causar daños significativos a la infraestructura y a la economía. Los fuertes vientos y las lluvias intensas pueden destruir edificios, carreteras y otras infraestructuras, lo que puede costar millones de dólares en reparaciones. Además, los huracanes pueden interrumpir las actividades económicas, como el turismo, que es una fuente importante de ingresos para Cuba.

Tambien, los huracanes también pueden tener un impacto significativo en el medio ambiente. Pueden causar erosión en las playas y en las zonas costeras, dañar los arrecifes de coral y alterar los ecosistemas marinos y terrestres.''')
    
    st.write('''Ademas, los huracanes pueden tener un impacto directo en la vida y la seguridad de las personas. Pueden causar lesiones o incluso la muerte, y pueden desplazar a las personas de sus hogares. El estudio de los huracanes puede ayudar a predecir su trayectoria y su intensidad, lo que puede permitir una mejor preparación y respuesta a estos eventos.

Por último, el estudio de los huracanes puede proporcionar información valiosa para entender los efectos del cambio climático. Se espera que la intensidad y la frecuencia de los huracanes aumenten como resultado del calentamiento global, por lo que entender estos fenómenos puede ayudar a predecir y prepararse para los efectos futuros del cambio climático.

En resumen, el estudio de los huracanes en Cuba es crucial para proteger la economía, el medio ambiente y la vida de las personas. A través de la investigación y la educación, podemos mejorar nuestra capacidad para predecir, prepararnos y responder a estos eventos extremos.''')



###########################################################################################################
#Cantidad de Huracanes por Mes Categoria y Ano
###########################################################################################################
    st.markdown("### Cantidad de Huracanes en Cuba por Mes, Año, Categoria y Region de Entrada")

    col1, col2 = st.columns(2)

    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%m/%d/%Y')

    df['Mes'] = df['Fecha'].dt.month
    df['Año'] = df['Fecha'].dt.year

    data = df.groupby('Año').size().reset_index(name='Huracanes')

    fig, ax = plt.subplots()
    ax.bar(data['Año'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Año')
    ax.set_xlabel('Año')
    ax.set_ylabel('Número de huracanes')
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

    data = df.groupby('Categoria').size().reset_index(name='Huracanes')
    fig, ax = plt.subplots()
    ax.bar(data['Categoria'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Categoria')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Número de Huracanes')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col1.pyplot(fig)

    data = df.groupby('Region').size().reset_index(name='Huracanes')
    fig, ax = plt.subplots()
    ax.bar(data['Region'], data['Huracanes'])
    ax.set_title('Número de Huracanes por Region')
    ax.set_xlabel('Region')
    ax.set_ylabel('Número de Huracanes')
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    plt.xticks(rotation='horizontal')
    col2.pyplot(fig)

###########################################################################################################
#Informacion General de los Huracanes
###########################################################################################################
    
    st.markdown("### Visualizacion Comparativa de la informacion sobre Huracanes")

    hurricane_names = df['Nombre'].unique().tolist()

    selected_hurricanes = st.multiselect('Elige los Huracanes que quieres visualizar:', hurricane_names)

    col1, col2 = st.columns(2)

    for i, hurricane in enumerate(selected_hurricanes):
        
        col = col1 if i % 2 == 0 else col2

        hurricane_data = df[df['Nombre'] == hurricane].drop(['Latitud', 'Longitud', 'Mes', 'Año'], axis=1)

        col.write(hurricane_data)

        if os.path.exists(f'{path}' + "/app/images/" + f"{hurricane}" + ".jpg"):
            with open(f'{path}' + "/app/images/" + f"{hurricane}" + ".jpg", 'rb') as f:
                datos_imagen = f.read()
            imagen = pl.Image.open(io.BytesIO(datos_imagen)).resize((1000,700))
            col.image(imagen, caption=hurricane, use_column_width=True)
        else:
            col.warning(f"No se encontró la imagen para el huracán {hurricane}")

###########################################################################################################
#Informacion General de los Huracanes
###########################################################################################################

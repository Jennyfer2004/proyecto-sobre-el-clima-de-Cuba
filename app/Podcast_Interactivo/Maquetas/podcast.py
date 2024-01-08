#PODCAST INTERACTIVO 

import streamlit as st 
import plotly_express as px 
import pandas as pd
import csv 
import os 


df = pd.read_csv("../app/data/base_datos.csv")

temp_med_anual = df.groupby(["Año","Mes"])["Temperatura med"].mean()

hum_anual = df.groupby(["Año","Mes"])["Humedad Relat"].mean()

prec_anual = df.groupby(["Año","Mes"])["Precipitaciones"].mean()

########################################
#filtrar los datos para obtener el 2019
########################################

df_new = pd.DataFrame({"Temperatura Media": temp_med_anual,"Humedad Relativa": hum_anual, "Precipitaciones": prec_anual})

años_específicos = [2019]

#Filtrar df por los meses de los años específicos
df_filtrado = df_new[df_new.index.get_level_values(0).isin(años_específicos)]

data = df_filtrado.reset_index()




st.title("Bajo el Clima")

###############
#AUDIOOOOOOOOOO
###############

#Pregunta a la audiencia.
st.write(" ###### ¿Alguna vez se han preguntado cómo un cambio en el clima puede afectar la propagación de enfermedades transmitidas por mosquitos como el dengue?")
opciones1 = ["Sí", "No", "No estoy segur@"]
respuesta1 = st.selectbox("Seleccione una opción:", opciones1,index=None)

#Pregunta y Encuesta.
st.write(" ###### ¿Saben cuáles son las condiciones climáticas que más favorecen la propagación de esta infección?")
opciones2 = ["Temperatura","Precipitaciones","Humedad","Radiación Solar","Vientos","Presión Atmosférica","Evaporación","No estoy segur@"]
respuesta2 = st.multiselect("Seleccione las opciones consideradas:", opciones2)


#Gráfico interactivo. 
fig = px.line(data, x='Mes', y=['Temperatura Media', 'Humedad Relativa', 'Precipitaciones'], 
              labels={'value': 'Valores', 'variable': 'Variables Climáticas'},
              color_discrete_map={'Temperatura Media': 'red', 'Humedad Relativa': 'blue', 'Precipitaciones': 'green'},
              title='Variación de las variables climáticas Temperatura,Humedad y Precipitaciones en el Año 2019',
              markers=True)

st.plotly_chart(fig)

#Pregunta a la audiencia.
st.write(" ###### ¿Sabían que un aumento en las precipitaciones puede crear más lugares de cría para los mosquitos que transmiten el dengue?")
opciones3 = ["Sí", "No", "No estoy segur@"]
respuesta3 = st.radio("Seleccione una opción:", opciones3)
#Manejo de las respuestas
if respuesta3 == "Sí":
    razon1 = st.text_input("Interesante,¿podrías compartir por qué piensas eso?")
elif respuesta3 == "No":
    razon2 = st.text_input("¿Podrías compartir por qué piensas que no es así?")
else:
    st.write("No te preocupes,es un tema complejo y es normal no estar seguro.A medida que avance el podcast comprenderás mejor")

#Pregunta a la audiencia.
st.write(" ###### Si alguno de nuestros oyentes reside o ha residido en una zona que ha experimentado un brote de dengue,¿podrían compartir su experiencia?")
experiencia = st.text_input("Escribe tu experiencia aquí:")

###################
#Link de la app web 
###################

#Pregunta de Reflexión Profunda.
st.write(" ###### Dado el impacto significativo del clima en tantos aspectos de nuestra vida,¿Cómo creen que podemos integrar de manera más efectiva el análisis climático en nuestras decisiones diarias para anticipar y mitigar estos efectos?,¿Qué acciones concretas podemos tomar hoy para utilizar mejor estos datos climáticos y prepararnos para los desafíos del mañana?.")
respuesta4 = st.text_input("Escribe tus respuestas aquí:")

#Sección para preguntas del usuario.
st.subheader(" ###### ¿Tienes alguna pregunta o comentario?")
user_question = st.text_input("Escribe tu pregunta o comentario aquí:")
if user_question:
    st.write(f"Gracias por tu pregunta o comentario. Responderemos lo antes posible.")
    
    


# Supongamos que las respuestas son las siguientes:
respuestas = {
    "pregunta1": respuesta1,
    "pregunta2": respuesta2,
    "pregunta3": respuesta3,
    "razon1": razon1,
    "experiencia": experiencia,
    "respuesta4": respuesta4,
    "user_question": user_question
}

# Convertimos las respuestas a un DataFrame de pandas
df_respuestas = pd.DataFrame([respuestas])

# Comprobamos si el archivo 'respuestas.csv' ya existe
if os.path.isfile('respuestas.csv'):
    # Si el archivo existe, leemos el archivo existente
    df_existente = pd.read_csv('respuestas.csv')
    # Añadimos las respuestas al final del DataFrame existente
    df_final = pd.concat([df_existente, df_respuestas],ignore_index=True)
else:
    #Si el archivo no existe, el DataFrame final es simplemente el DataFrame de respuestas
    df_final = df_respuestas

# Guardamos el DataFrame final en el archivo 'respuestas.csv'
df_final.to_csv('respuestas.csv', index=False)


